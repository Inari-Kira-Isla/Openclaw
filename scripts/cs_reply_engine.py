#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — AI 回覆引擎
封裝 OpenClaw gateway 呼叫，支援品牌語氣注入與對話歷史
v1.0 — 2026-03-03
"""

import os
import json
import requests
from datetime import datetime

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

OC_GATEWAY  = os.environ.get("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789")
OC_TOKEN    = os.environ.get("OPENCLAW_TOKEN", "***REMOVED***")

HEADERS = {
    "X-Openclaw-Token": OC_TOKEN,
    "Content-Type": "application/json",
}

REPLY_AGENT   = "cs-reply-agent"
CONTENT_AGENT = "writing-master"
MAX_REPLY_LEN = 280    # FB Messenger friendly


def _gateway_chat(agent_id, message, system_prompt="", context="", timeout=25):
    """呼叫 OpenClaw gateway agent chat endpoint"""
    payload = {"message": message}
    if system_prompt:
        payload["system"] = system_prompt
    if context:
        payload["context"] = context
    try:
        resp = requests.post(
            f"{OC_GATEWAY}/api/agents/{agent_id}/chat",
            json=payload,
            headers=HEADERS,
            timeout=timeout,
        )
        if resp.ok:
            d = resp.json()
            # Normalize response field name
            return (d.get("reply") or d.get("message") or
                    d.get("content") or d.get("text") or "")
        return ""
    except Exception as e:
        print(f"[cs_reply_engine] gateway error: {e}")
        return ""


def generate_customer_reply(message, brand_config, customer_history=None):
    """
    生成品牌語氣客服回覆
    Returns: {reply, source, confidence}
    """
    tone = brand_config.get("tone_prompt", "你是客服代表，請親切專業地回覆客戶。")
    brand_name = brand_config.get("brand_name", "")

    # Build conversation context from history
    context = ""
    if customer_history:
        context_lines = []
        for h in customer_history[-5:]:   # last 5 turns
            if h.get("message_in"):
                context_lines.append(f"用戶: {h['message_in']}")
            if h.get("message_out"):
                context_lines.append(f"客服: {h['message_out']}")
        context = "\n".join(context_lines)

    reply = _gateway_chat(
        agent_id=REPLY_AGENT,
        message=message,
        system_prompt=tone,
        context=context,
    )

    if reply:
        # Trim to max length, preserve complete sentences
        if len(reply) > MAX_REPLY_LEN:
            # Cut at last sentence boundary within limit
            for sep in ["。", "！", "？", ".", "!", "?"]:
                last = reply[:MAX_REPLY_LEN].rfind(sep)
                if last > MAX_REPLY_LEN * 0.6:
                    reply = reply[:last + 1]
                    break
            else:
                reply = reply[:MAX_REPLY_LEN]

        return {"reply": reply, "source": "ai", "confidence": 0.72}

    return {"reply": "", "source": "none", "confidence": 0.0}


def generate_brand_content(brand_config, content_type="post", topic="", hot_topics=None):
    """
    生成品牌行銷文案
    content_type: 'post' | 'promo' | 'story' | 'caption'
    Returns: {short, long, caption} 三種格式
    """
    brand_name = brand_config.get("brand_name", "品牌")
    tone       = brand_config.get("tone_prompt", "")

    hot_str = ""
    if hot_topics:
        hot_str = f"\n近期客戶最常問的問題：{', '.join(hot_topics[:3])}"

    type_guide = {
        "post":    "教育性貼文，分享有用資訊",
        "promo":   "促銷文案，強調優惠和限時",
        "story":   "客戶見證，真實故事格式",
        "caption": "圖片說明文字，簡潔吸引人",
    }.get(content_type, "貼文")

    prompt = (
        f"請為品牌「{brand_name}」生成以下格式的{type_guide}。"
        f"{f'主題：{topic}' if topic else ''}"
        f"{hot_str}\n\n"
        "請生成：\n"
        "1. 短文（180字以內，適合Facebook貼文）\n"
        "2. 長文（500字，適合部落格或詳細說明）\n"
        "3. 圖說（50字以內，適合圖片配文）\n\n"
        "格式：\n【短文】\n...\n【長文】\n...\n【圖說】\n..."
    )

    response = _gateway_chat(
        agent_id=CONTENT_AGENT,
        message=prompt,
        system_prompt=tone,
        timeout=45,
    )

    result = {"short": "", "long": "", "caption": "", "raw": response}
    if response:
        import re
        short_m  = re.search(r"【短文】\s*(.*?)(?=【|$)", response, re.DOTALL)
        long_m   = re.search(r"【長文】\s*(.*?)(?=【|$)", response, re.DOTALL)
        caption_m = re.search(r"【圖說】\s*(.*?)(?=【|$)", response, re.DOTALL)
        if short_m:   result["short"]   = short_m.group(1).strip()
        if long_m:    result["long"]    = long_m.group(1).strip()
        if caption_m: result["caption"] = caption_m.group(1).strip()

    return result


if __name__ == "__main__":
    from cs_customer_db import get_brand_config
    brand = get_brand_config("demo") or {
        "brand_name": "Demo Brand",
        "tone_prompt": "你是 Demo Brand 的客服，語氣親切。",
    }
    print("=== Test: customer reply ===")
    result = generate_customer_reply("你們有什麼新品嗎？", brand)
    print(f"  reply: {result['reply'][:80]}..." if result['reply'] else "  (no gateway reply — OK in test)")

    print("\n=== Test: brand content ===")
    content = generate_brand_content(brand, content_type="post", topic="春季新品上市")
    print(f"  short: {content['short'][:60]}..." if content['short'] else "  (no gateway reply — OK in test)")
