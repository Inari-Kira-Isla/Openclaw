#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — 品牌優化閉環
每週一 10:00 執行:
  1. 生成週報 (效率、情緒、熱門問題)
  2. 自動優化品牌設定 (FAQ、語氣、VIP 標記)
  3. 成功回覆存入 success DB
  4. 推送 Telegram 週報
v1.0 — 2026-03-03
"""

import os
import json
import sqlite3
import requests
from datetime import datetime, timezone

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

OC_GATEWAY   = os.environ.get("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789")
OC_TOKEN     = os.environ.get("OPENCLAW_TOKEN", "***REMOVED***")
TG_CHAT_ID   = os.environ.get("TG_ESCALATE_CHAT", "8399476482")
SUCCESS_LOG_DIR = os.path.expanduser("~/.openclaw/workspace/success_log")


def _send_telegram(text):
    try:
        resp = requests.post(
            f"{OC_GATEWAY}/api/messages/telegram",
            json={"to": TG_CHAT_ID, "message": text},
            headers={"X-Openclaw-Token": OC_TOKEN},
            timeout=10,
        )
        return resp.ok
    except Exception:
        return False


def _push_to_success_db(title, content, tags):
    """存入本地 success_log/ (取代 Notion)"""
    os.makedirs(SUCCESS_LOG_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    fname = f"{today}_{title[:40].replace(' ','_').replace('/','_')}.json"
    fpath = os.path.join(SUCCESS_LOG_DIR, fname)
    data = {
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True


def build_weekly_report(brand_id=None):
    """生成週報數據"""
    from cs_customer_db import get_weekly_stats, get_top_intents, get_vip_candidates

    stats   = get_weekly_stats(brand_id, days=7)
    intents = get_top_intents(brand_id, days=7, limit=10)
    vip_cands = get_vip_candidates()

    total = stats.get("total", 0)
    if total == 0:
        return None

    faq_rate    = round(stats.get("faq_count", 0) / max(1, total) * 100, 1)
    ai_rate     = round(stats.get("ai_count", 0) / max(1, total) * 100, 1)
    human_rate  = round(stats.get("human_count", 0) / max(1, total) * 100, 1)
    avg_ms      = int(stats.get("avg_response_ms", 0) or 0)
    avg_conf    = round(stats.get("avg_confidence", 0) or 0, 2)

    return {
        "brand_id":      brand_id or "all",
        "period":        "last 7 days",
        "total":         total,
        "faq_rate":      faq_rate,
        "ai_rate":       ai_rate,
        "human_rate":    human_rate,
        "avg_response_ms": avg_ms,
        "avg_confidence": avg_conf,
        "top_intents":   intents,
        "vip_candidates": len(vip_cands),
    }


def format_report(report, brand_name="全品牌"):
    """格式化週報文字"""
    if not report:
        return f"{brand_name} 本週無對話記錄"

    top_intents_str = "\n".join(
        f"  {i+1}. {it['intent']} ({it['cnt']}次)"
        for i, it in enumerate(report["top_intents"][:5])
    ) or "  (無資料)"

    return (
        f"📊 {brand_name} 週報 — {datetime.now().strftime('%Y-%m-%d')}\n"
        f"─────────────────────\n"
        f"總對話數: {report['total']}\n"
        f"FAQ 自動回覆: {report['faq_rate']}%\n"
        f"AI 回覆: {report['ai_rate']}%\n"
        f"人工升級: {report['human_rate']}%\n"
        f"平均回覆: {report['avg_response_ms']}ms\n"
        f"平均信心: {report['avg_confidence']}\n"
        f"\n🔥 熱門意圖 Top 5:\n{top_intents_str}\n"
        f"\n⭐ 新 VIP 候選: {report['vip_candidates']} 位\n"
    )


def auto_optimize_brands():
    """自動優化所有品牌設定"""
    from cs_customer_db import (list_brands, get_faqs, get_vip_candidates,
                                 mark_vip, upsert_brand)

    brands = list_brands(enabled_only=False)
    optimizations = []

    for brand in brands:
        brand_id = brand["brand_id"]

        # 1. Mark VIP candidates
        vip_cands = get_vip_candidates(min_messages=5, min_sentiment=0.6)
        brand_vips = [c for c in vip_cands if c.get("brand_id") == brand_id]
        for v in brand_vips:
            mark_vip(v["id"])
        if brand_vips:
            optimizations.append(f"  {brand_id}: {len(brand_vips)} VIP 標記更新")

        # 2. FAQ hit analysis — high hit FAQs → promote
        faqs = get_faqs(brand_id)
        top_faqs = [f for f in faqs if f.get("match_count", 0) >= 10]
        if top_faqs:
            optimizations.append(
                f"  {brand_id}: {len(top_faqs)} 個 FAQ 命中率高 (建議加強品牌文案)"
            )

        # 3. Log optimization to success DB
        if brand_vips or top_faqs:
            report = build_weekly_report(brand_id)
            if report:
                summary = format_report(report, brand.get("brand_name", brand_id))
                _push_to_success_db(
                    title=f"{brand_id} 週報 {datetime.now().strftime('%Y-%m-%d')}",
                    content=summary,
                    tags=["週報", brand_id, "客服優化"],
                )

    return optimizations


def run():
    from cs_customer_db import list_brands

    print(f"[cs_brand_optimizer] Starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    brands = list_brands(enabled_only=False)
    all_reports = []

    for brand in brands:
        brand_id   = brand["brand_id"]
        brand_name = brand.get("brand_name", brand_id)
        report     = build_weekly_report(brand_id)
        text       = format_report(report, brand_name)
        all_reports.append(text)
        print(text)

    # Auto-optimize
    opts = auto_optimize_brands()
    if opts:
        print("\n🔧 自動優化:")
        for o in opts:
            print(o)

    # Send Telegram summary
    tg_text = "\n\n".join(all_reports)
    if opts:
        tg_text += "\n\n🔧 優化動作:\n" + "\n".join(opts)
    if len(tg_text) > 4000:
        tg_text = tg_text[:3900] + "\n...(截斷)"
    _send_telegram(tg_text)

    print("[cs_brand_optimizer] Done")


if __name__ == "__main__":
    run()
