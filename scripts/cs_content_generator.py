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
NOTION_DAILY_DB   = os.environ.get("NOTION_DB_DAILY", "30aa1238-f49d-8136-a813-fb759eb30e47")
NOTION_KEY        = os.environ.get("NOTION_API_KEY", "")


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


def _push_to_notion(title, content, brand_name, content_type):
    """推送到 Notion DAILY 索引目錄"""
    if not NOTION_KEY or NOTION_KEY == "REPLACE_WITH_NEW_KEY":
        return False
    import requests
    headers = {
        "Authorization":  f"Bearer {NOTION_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type":   "application/json",
    }
    # Split content into Notion blocks (max 1900 chars each)
    blocks = []
    for chunk in [content[i:i+1900] for i in range(0, len(content), 1900)][:50]:
        blocks.append({"paragraph": {"rich_text": [{"text": {"content": chunk}}]}})

    payload = {
        "parent":     {"database_id": NOTION_DAILY_DB},
        "properties": {
            "標題": {"title": [{"text": {"content": title}}]},
            "類型": {"select": {"name": "品牌文案"}},
            "標籤": {"multi_select": [{"name": brand_name}, {"name": content_type}]},
            "建立日期": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
            "狀態": {"select": {"name": "待發布"}},
        },
        "children": blocks,
    }
    resp = requests.post("https://api.notion.com/v1/pages",
                         json=payload, headers=headers, timeout=20)
    return resp.ok


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

        if content.get("short") or content.get("long"):
            # Push to Notion
            full_text = "\n\n".join(filter(None, [
                f"【短文】\n{content.get('short','')}",
                f"【長文】\n{content.get('long','')}",
                f"【圖說】\n{content.get('caption','')}",
            ]))
            today = datetime.now().strftime("%Y-%m-%d")
            title = f"{today} {brand_name} {ctype} 文案"
            pushed = _push_to_notion(title, full_text, brand_name, ctype)
            print(f"  Notion push: {'✅' if pushed else '⚠️ (key not set)'}")

        # Always save locally
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


if __name__ == "__main__":
    run()
