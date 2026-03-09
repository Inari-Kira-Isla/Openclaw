#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — Webhook 接收器
接收自建 API Proxy 傳來的多品牌訊息，路由至 FAQ / AI 回覆 / 人工升級
Port: 18790 (可透過 CS_WEBHOOK_PORT env 覆蓋)
v1.0 — 2026-03-03
"""

import os
import json
import time
import sys
import logging
from datetime import datetime, timezone

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

PORT        = int(os.environ.get("CS_WEBHOOK_PORT", "18790"))
OC_TOKEN    = os.environ.get("OPENCLAW_TOKEN", "***REMOVED***")
OC_GATEWAY  = os.environ.get("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789")
TG_CHAT_ID  = os.environ.get("TG_ESCALATE_CHAT", "8399476482")

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("cs-webhook")

# ─── Lazy imports (avoid ImportError at startup if packages missing) ────────────
def _import_flask():
    try:
        from flask import Flask, request, jsonify
        return Flask, request, jsonify
    except ImportError:
        log.error("Flask not installed. Run: pip install flask")
        sys.exit(1)

def _import_requests():
    import requests as r
    return r


# ─── OpenClaw API helper ────────────────────────────────────────────────────────

def _oc_post(path, data):
    """POST to OpenClaw gateway"""
    r = _import_requests()
    try:
        resp = r.post(
            f"{OC_GATEWAY}{path}",
            json=data,
            headers={"X-Openclaw-Token": OC_TOKEN},
            timeout=25,
        )
        return resp.json() if resp.ok else {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}


def _send_telegram(chat_id, text):
    """透過 OpenClaw Gateway 發 Telegram 通知"""
    return _oc_post("/api/messages/telegram", {
        "to": chat_id,
        "message": text,
    })


def _ask_ai_agent(agent_id, message, system_prompt="", context=""):
    """請 OpenClaw agent 生成回覆"""
    payload = {"message": message}
    if system_prompt:
        payload["system"] = system_prompt
    if context:
        payload["context"] = context
    return _oc_post(f"/api/agents/{agent_id}/chat", payload)


# ─── Intent classifier (lightweight, no API needed) ─────────────────────────────

INTENT_RULES = [
    ("詢問優惠",  ["優惠", "折扣", "特價", "promotion", "discount", "coupon", "優惠碼"]),
    ("下訂諮詢",  ["下訂", "購買", "訂購", "order", "buy", "怎麼買", "如何購買", "想買"]),
    ("物流查詢",  ["出貨", "到貨", "幾天", "運費", "shipping", "delivery", "快遞", "物流"]),
    ("退換貨",    ["退貨", "換貨", "退款", "return", "refund", "瑕疵", "壞掉", "問題"]),
    ("投訴",      ["投訴", "complain", "不滿", "差評", "騙", "詐騙", "假貨", "爛"]),
    ("讚美",      ["謝謝", "讚", "好棒", "excellent", "great", "love", "喜歡", "滿意"]),
]

def classify_intent(text):
    t = text.lower()
    for intent, kws in INTENT_RULES:
        if any(k.lower() in t for k in kws):
            return intent
    return "一般詢問"


# ─── Core handler ───────────────────────────────────────────────────────────────

def handle_message(payload):
    """
    處理一條訊息，返回 {reply, source, confidence, intent, customer_id}
    payload: {platform, brand_id, sender_id, message, timestamp, metadata}
    """
    from cs_customer_db import (get_or_create_customer, get_brand_config,
                                 log_conversation, update_reply,
                                 get_customer_history, update_sentiment)
    from cs_faq_matcher import FAQMatcher

    t0 = time.time()

    platform   = payload.get("platform", "facebook")
    brand_id   = payload.get("brand_id", "demo")
    sender_id  = payload.get("sender_id", "")
    message    = payload.get("message", "").strip()
    metadata   = payload.get("metadata", {})
    display_name = metadata.get("sender_name", "")

    if not message:
        return {"reply": "", "source": "none", "confidence": 0.0, "intent": "none"}

    # 1. Get/create customer
    customer = get_or_create_customer(platform, brand_id, sender_id, display_name)
    customer_id = customer["id"]

    # 2. Get brand config
    brand = get_brand_config(brand_id)
    if brand is None:
        # Brand not configured — use defaults
        brand = {
            "brand_name": brand_id,
            "tone_prompt": "你是客服代表，請親切專業地回覆客戶。回覆限 200 字。",
            "confidence_threshold": 0.70,
            "escalate_to": TG_CHAT_ID,
            "auto_reply_enabled": 1,
        }

    threshold = brand.get("confidence_threshold", 0.70)
    tone      = brand.get("tone_prompt", "")
    escalate_to = brand.get("escalate_to") or TG_CHAT_ID

    # 3. Classify intent
    intent = classify_intent(message)

    # 4. Pre-log the incoming message (will update with reply later)
    conv_id = log_conversation(
        customer_id=customer_id,
        brand_id=brand_id,
        platform=platform,
        message_in=message,
        intent=intent,
    )

    reply = ""
    source = "human"
    confidence = 0.0

    # 5. FAQ matching
    if brand.get("auto_reply_enabled", 1):
        matcher = FAQMatcher()
        faq_result = matcher.match(message, brand_id, threshold)
        if faq_result:
            reply, confidence, _ = faq_result
            source = "faq"

    # 6. AI reply if no FAQ hit
    if not reply and brand.get("auto_reply_enabled", 1):
        history = get_customer_history(customer_id, limit=5)
        context = "\n".join(
            f"用戶: {h['message_in']}\n客服: {h['message_out']}"
            for h in history if h.get("message_out")
        )
        ai_resp = _ask_ai_agent(
            agent_id="cs-reply-agent",
            message=message,
            system_prompt=tone,
            context=context,
        )
        if ai_resp and not ai_resp.get("error"):
            reply_text = (ai_resp.get("reply") or
                          ai_resp.get("message") or
                          ai_resp.get("content") or "")
            if reply_text:
                reply = reply_text[:280]   # Messenger friendly length
                source = "ai"
                confidence = 0.70  # AI replies default confidence

    # 7. Escalate if still no reply (or low confidence)
    if not reply:
        source = "human"
        confidence = 0.0
        brand_name = brand.get("brand_name", brand_id)
        tg_msg = (
            f"⚠️ [{brand_name}] 客服升級通知\n"
            f"平台: {platform} | 客戶: {display_name or sender_id}\n"
            f"訊息: {message}\n"
            f"意圖: {intent}\n"
            f"時間: {datetime.now().strftime('%H:%M:%S')}"
        )
        _send_telegram(escalate_to, tg_msg)

    # 8. Update conversation record with reply, confidence, response time
    ms = int((time.time() - t0) * 1000)
    update_reply(conv_id, reply, source, confidence, ms)

    # 9. Simple sentiment update (positive words → +, negative → -)
    sentiment = 0.0
    pos_words = ["謝謝", "讚", "好", "棒", "滿意", "perfect", "great", "thanks"]
    neg_words = ["差", "爛", "投訴", "不滿", "詐騙", "假", "壞"]
    if any(w in message.lower() for w in pos_words):
        sentiment = 0.8
    elif any(w in message.lower() for w in neg_words):
        sentiment = 0.2
    if sentiment:
        update_sentiment(customer_id, sentiment)

    log.info(f"[{brand_id}] {sender_id} → {source} reply in {ms}ms (conf={confidence:.2f})")

    return {
        "reply":       reply,
        "source":      source,
        "confidence":  confidence,
        "intent":      intent,
        "customer_id": customer_id,
        "response_ms": ms,
    }


# ─── Flask App ──────────────────────────────────────────────────────────────────

def create_app():
    Flask, request, jsonify = _import_flask()
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "cs-webhook", "port": PORT})

    @app.route("/webhook", methods=["POST"])
    def webhook():
        # Auth check
        token = request.headers.get("X-Openclaw-Token", "")
        if token != OC_TOKEN:
            return jsonify({"error": "unauthorized"}), 401

        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "invalid JSON"}), 400

        # Required fields
        for field in ("platform", "brand_id", "sender_id", "message"):
            if not data.get(field):
                return jsonify({"error": f"missing field: {field}"}), 400

        try:
            result = handle_message(data)
        except Exception as e:
            log.exception("Error handling message")
            return jsonify({"error": str(e)}), 500

        return jsonify(result)

    @app.route("/brands", methods=["GET"])
    def list_brands_endpoint():
        from cs_customer_db import list_brands
        return jsonify(list_brands())

    @app.route("/brands/<brand_id>/faq", methods=["GET"])
    def list_faq(brand_id):
        from cs_customer_db import get_faqs
        return jsonify(get_faqs(brand_id))

    @app.route("/brands/<brand_id>/faq", methods=["POST"])
    def add_faq_endpoint(brand_id):
        data = request.get_json(force=True, silent=True) or {}
        from cs_customer_db import add_faq
        add_faq(brand_id, data.get("question",""), data.get("answer",""),
                data.get("keywords", []))
        return jsonify({"status": "created"})

    return app


if __name__ == "__main__":
    log.info(f"Starting CS Webhook Receiver on port {PORT}")
    app = create_app()
    app.run(host="0.0.0.0", port=PORT, debug=False)
