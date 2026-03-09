#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEPRECATED] OpenClaw CS — Notion 同步
已被 cs_github_sync.py 取代 (2026-03-04)
SQLite → GitHub 同步，不再依賴 Notion API。
"""

import os
import json
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

NOTION_KEY      = os.environ.get("NOTION_API_KEY", "")
DB_CUSTOMERS    = os.environ.get("NOTION_DB_CS_CUSTOMERS",    "1044b83d7ccb486db5ed67f029bb313a")
DB_CONVS        = os.environ.get("NOTION_DB_CS_CONVERSATIONS", "b9ea4a60e8b046fcb7fd547bd48f6611")

NOTION_HEADERS  = {
    "Authorization":  f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type":   "application/json",
}
NOTION_BASE     = "https://api.notion.com/v1"

MAX_TEXT_LEN    = 1900   # Notion block limit


def _rt(text):
    """Create a rich_text object, truncated to Notion limit"""
    return [{"text": {"content": str(text or "")[:MAX_TEXT_LEN]}}]


def _notion_post(path, data):
    resp = requests.post(f"{NOTION_BASE}{path}",
                         json=data, headers=NOTION_HEADERS, timeout=20)
    if not resp.ok:
        print(f"  [Notion ERROR] {resp.status_code}: {resp.text[:200]}")
        return None
    return resp.json()


def _notion_patch(path, data):
    resp = requests.patch(f"{NOTION_BASE}{path}",
                          json=data, headers=NOTION_HEADERS, timeout=20)
    if not resp.ok:
        print(f"  [Notion PATCH ERROR] {resp.status_code}: {resp.text[:200]}")
        return None
    return resp.json()


# ─── Customer sync ─────────────────────────────────────────────────────────────

def _build_customer_properties(c):
    """Build Notion page properties for a customer row"""
    name = c.get("display_name") or c.get("sender_id") or "Unknown"
    props = {
        "姓名":    {"title": _rt(name)},
        "平台":    {"select": {"name": c.get("platform", "other")}},
        "品牌":    {"select": {"name": c.get("brand_id", "demo")}},
        "訊息總數": {"number": c.get("total_messages", 0)},
        "情緒分數": {"number": round(c.get("sentiment_score", 0.0), 3)},
        "VIP":     {"checkbox": bool(c.get("vip_flag", 0))},
        "Sender ID": {"rich_text": _rt(c.get("sender_id", ""))},
        "狀態":    {"select": {"name": _derive_status(c)}},
    }
    if c.get("first_seen"):
        props["首次聯繫"] = {"date": {"start": c["first_seen"][:10]}}
    if c.get("last_seen"):
        props["最後聯繫"] = {"date": {"start": c["last_seen"][:10]}}
    tags = json.loads(c.get("tags", "[]") or "[]")
    if tags:
        props["標籤"] = {"multi_select": [{"name": t} for t in tags]}
    return props


def _derive_status(c):
    from datetime import datetime, timezone, timedelta
    try:
        last = datetime.fromisoformat(c.get("last_seen", "2000-01-01"))
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - last).days
        if days < 7:
            return "活躍"
        elif days < 30:
            return "待跟進"
        return "休眠"
    except Exception:
        return "待跟進"


def sync_customers(limit=50):
    """Sync pending customers to Notion"""
    from cs_customer_db import (get_pending_notion_customers,
                                 mark_customer_notion_synced)
    if not NOTION_KEY or NOTION_KEY == "REPLACE_WITH_NEW_KEY":
        print("[cs_notion_sync] ⚠️  NOTION_API_KEY not set, skipping")
        return 0

    customers = get_pending_notion_customers(limit)
    if not customers:
        print("[cs_notion_sync] No pending customers")
        return 0

    synced = 0
    for c in customers:
        props = _build_customer_properties(c)
        result = _notion_post("/pages", {
            "parent": {"database_id": DB_CUSTOMERS},
            "properties": props,
        })
        if result:
            notion_id = result.get("id", "")
            mark_customer_notion_synced(c["id"], notion_id)
            synced += 1

    print(f"[cs_notion_sync] Customers synced: {synced}/{len(customers)}")
    return synced


# ─── Conversation sync ──────────────────────────────────────────────────────────

def sync_conversations(limit=100):
    """Sync pending conversations to Notion"""
    from cs_customer_db import (get_pending_notion_conversations,
                                 mark_conversations_synced)
    if not NOTION_KEY or NOTION_KEY == "REPLACE_WITH_NEW_KEY":
        return 0

    convs = get_pending_notion_conversations(limit)
    if not convs:
        print("[cs_notion_sync] No pending conversations")
        return 0

    synced_ids = []
    for cv in convs:
        # Title: "品牌 · intent · date"
        dt = cv.get("created_at", "")[:16]
        title = f"{cv.get('brand_id','')} · {cv.get('intent','')} · {dt}"
        intent_map = {
            "詢問優惠": "詢問優惠", "下訂諮詢": "下訂諮詢", "物流查詢": "物流查詢",
            "退換貨": "退換貨", "投訴": "投訴", "讚美": "讚美", "一般詢問": "一般詢問",
        }
        intent_val = intent_map.get(cv.get("intent", ""), "其他")
        props = {
            "標題":    {"title": _rt(title)},
            "品牌":    {"select": {"name": cv.get("brand_id", "demo")}},
            "平台":    {"select": {"name": cv.get("platform", "other")}},
            "用戶訊息": {"rich_text": _rt(cv.get("message_in", ""))},
            "AI回覆":  {"rich_text": _rt(cv.get("message_out", ""))},
            "意圖":    {"select": {"name": intent_val}},
            "回覆來源": {"select": {"name": cv.get("reply_source", "ai")}},
            "信心分數": {"number": round(cv.get("confidence", 0.0), 3)},
            "回覆時間ms": {"number": cv.get("response_time_ms", 0)},
            "Sender ID": {"rich_text": _rt(cv.get("sender_id", ""))},
        }
        if cv.get("created_at"):
            props["日期"] = {"date": {"start": cv["created_at"][:10]}}

        result = _notion_post("/pages", {
            "parent": {"database_id": DB_CONVS},
            "properties": props,
        })
        if result:
            synced_ids.append(cv["id"])

    if synced_ids:
        mark_conversations_synced(synced_ids)
    print(f"[cs_notion_sync] Conversations synced: {len(synced_ids)}/{len(convs)}")
    return len(synced_ids)


def run():
    print(f"[cs_notion_sync] Starting sync — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c_count = sync_customers()
    v_count = sync_conversations()
    print(f"[cs_notion_sync] Done: {c_count} customers, {v_count} conversations")


if __name__ == "__main__":
    run()
