#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — 每日品牌文案生成器
分析昨日對話熱點 → 呼叫 writing-master → 存入 Notion DAILY + 本地 content_queue/
每日 09:00 由 cron 觸發
v1.0 — 2026-03-03
"""

import os
import json
from datetime import datetime, timezone, timedelta

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

CONTENT_QUEUE_DIR = os.path.expanduser("~/.openclaw/workspace/content_queue")
TG_CHAT_ID = "8399476482"


def notify_telegram(msg: str):
    import subprocess
    try:
        result = subprocess.run(
            ["/usr/local/bin/openclaw", "message", "send",
             "--channel", "telegram", "--account", "kira",
             "--target", TG_CHAT_ID, "--message", msg],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0:
            print(f"[telegram] ✅ 通知已發送")
        else:
            print(f"[telegram] ❌ 發送失敗 (exit {result.returncode}): {result.stderr.strip()}")
    except Exception as e:
        print(f"[telegram] ❌ 例外: {e}")


def _get_hot_topics(brand_id, days=1):
    """取得最近 N 天的熱門意圖/FAQ 問題"""
    import sqlite3
    db_path = os.path.expanduser(os.environ.get("CS_CUSTOMER_DB", "~/.openclaw/memory/cs_customers.db"))
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
    rows = conn.execute(f"""
        SELECT intent, COUNT(*) cnt FROM conversations
        WHERE brand_id=? AND created_at >= datetime('now', '-{days} days')
        GROUP BY intent ORDER BY cnt DESC LIMIT 5
    """, (brand_id,)).fetchall()
    conn.close()
    return [r[0] for r in rows if r[0] not in ("一般詢問", "unknown")]


def _save_to_queue(brand_id, content_type, data):
    """儲存到本地 content_queue/ 資料夾"""
    os.makedirs(CONTENT_QUEUE_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    fname = f"{today}_{brand_id}_{content_type}.json"
    fpath = os.path.join(CONTENT_QUEUE_DIR, fname)
    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {fpath}")


def generate_for_brand(brand):
    """為單一品牌生成今日文案"""
    from cs_reply_engine import generate_brand_content

    brand_id   = brand["brand_id"]
    brand_name = brand.get("brand_name", brand_id)
    hot_topics = _get_hot_topics(brand_id, days=1)

    print(f"\n  Brand: {brand_name} | Hot topics: {hot_topics}")

    # Generate 2 types: educational post + promo
    results = {}
    for ctype in ["post", "promo"]:
        topic = hot_topics[0] if hot_topics else ""
        content = generate_brand_content(brand, content_type=ctype,
                                         topic=topic, hot_topics=hot_topics)
        results[ctype] = content

        # Save locally
        _save_to_queue(brand_id, ctype, {
            "brand_id":   brand_id,
            "brand_name": brand_name,
            "type":       ctype,
            "hot_topics": hot_topics,
            **content,
        })

    return results


def run():
    from cs_customer_db import list_brands
    print(f"[cs_content_generator] Starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    brands = list_brands(enabled_only=True)
    if not brands:
        print("[cs_content_generator] No enabled brands found")
        return

    for brand in brands:
        try:
            generate_for_brand(brand)
        except Exception as e:
            print(f"  [ERROR] {brand.get('brand_id')}: {e}")

    print(f"\n[cs_content_generator] Done. Content saved to: {CONTENT_QUEUE_DIR}")

    # Telegram 通知
    summaries = []
    for brand in brands:
        bid = brand.get("brand_id", "?")
        bname = brand.get("brand_name", bid)
        summaries.append(f"  · {bname}")
    if summaries:
        notify_telegram(
            f"📝 CS 每日文案已生成\n"
            f"🏢 {len(brands)} 個品牌\n\n"
            + "\n".join(summaries[:6])
            + (f"\n  ...及其他 {len(summaries) - 6} 個" if len(summaries) > 6 else "")
            + f"\n\n📂 已存入 content_queue/ 待審核"
        )


if __name__ == "__main__":
    run()
