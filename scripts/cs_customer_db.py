#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — 客戶資料庫 (SQLite)
cs_customers.db: brands / customers / conversations / faq_entries
v1.0 — 2026-03-03
"""

import os
import json
import sqlite3
from datetime import datetime, timezone

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

DB_PATH = os.path.expanduser(
    os.environ.get("CS_CUSTOMER_DB", "~/.openclaw/memory/cs_customers.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS brands (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id             TEXT    NOT NULL UNIQUE,
    brand_name           TEXT    NOT NULL,
    fb_page_id           TEXT,
    fb_access_token      TEXT,
    tone_prompt          TEXT    DEFAULT '',
    faq_data             TEXT    DEFAULT '[]',
    auto_reply_enabled   INTEGER DEFAULT 1,
    confidence_threshold REAL    DEFAULT 0.70,
    escalate_to          TEXT    DEFAULT '8399476482',
    created_at           TEXT    DEFAULT (datetime('now')),
    updated_at           TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS customers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    platform        TEXT    NOT NULL,
    brand_id        TEXT    NOT NULL,
    sender_id       TEXT    NOT NULL,
    display_name    TEXT    DEFAULT '',
    first_seen      TEXT    DEFAULT (datetime('now')),
    last_seen       TEXT    DEFAULT (datetime('now')),
    total_messages  INTEGER DEFAULT 0,
    sentiment_score REAL    DEFAULT 0.0,
    vip_flag        INTEGER DEFAULT 0,
    tags            TEXT    DEFAULT '[]',
    notion_page_id  TEXT,
    synced_at       TEXT,
    UNIQUE (platform, brand_id, sender_id)
);
CREATE INDEX IF NOT EXISTS idx_cust_brand ON customers(brand_id);
CREATE INDEX IF NOT EXISTS idx_cust_sync  ON customers(synced_at);

CREATE TABLE IF NOT EXISTS conversations (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id      INTEGER NOT NULL REFERENCES customers(id),
    brand_id         TEXT    NOT NULL,
    platform         TEXT    NOT NULL,
    message_in       TEXT    NOT NULL,
    message_out      TEXT    DEFAULT '',
    intent           TEXT    DEFAULT 'unknown',
    confidence       REAL    DEFAULT 0.0,
    reply_source     TEXT    DEFAULT 'ai',
    response_time_ms INTEGER DEFAULT 0,
    created_at       TEXT    DEFAULT (datetime('now')),
    notion_synced    INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_conv_cust    ON conversations(customer_id);
CREATE INDEX IF NOT EXISTS idx_conv_brand   ON conversations(brand_id);
CREATE INDEX IF NOT EXISTS idx_conv_sync    ON conversations(notion_synced);
CREATE INDEX IF NOT EXISTS idx_conv_created ON conversations(created_at);

CREATE TABLE IF NOT EXISTS faq_entries (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id     TEXT    NOT NULL,
    question     TEXT    NOT NULL,
    answer       TEXT    NOT NULL,
    keywords     TEXT    DEFAULT '[]',
    match_count  INTEGER DEFAULT 0,
    last_matched TEXT,
    created_at   TEXT    DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_faq_brand ON faq_entries(brand_id);
"""


def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    return c


def init_db():
    """建立 schema（首次執行）"""
    with _conn() as c:
        c.executescript(SCHEMA)
    print(f"[cs_customer_db] DB initialised: {DB_PATH}")


# ─── Brands ────────────────────────────────────────────────────────────────────

def upsert_brand(brand_id, brand_name, **kwargs):
    """新增或更新品牌設定"""
    fields = ["brand_id", "brand_name"] + list(kwargs.keys())
    vals = [brand_id, brand_name] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    cols = ",".join(fields)
    update_cols = ",".join(f"{k}=excluded.{k}" for k in fields if k != "brand_id")
    sql = (f"INSERT INTO brands ({cols}) VALUES ({placeholders}) "
           f"ON CONFLICT(brand_id) DO UPDATE SET {update_cols}, "
           f"updated_at=datetime('now')")
    with _conn() as c:
        c.execute(sql, vals)


def get_brand_config(brand_id):
    """取得品牌設定 dict；不存在返回 None"""
    with _conn() as c:
        row = c.execute("SELECT * FROM brands WHERE brand_id=?", (brand_id,)).fetchone()
    if row is None:
        return None
    d = dict(row)
    d["faq_data"] = json.loads(d.get("faq_data") or "[]")
    return d


def list_brands(enabled_only=True):
    """列出品牌列表"""
    sql = "SELECT * FROM brands"
    if enabled_only:
        sql += " WHERE auto_reply_enabled=1"
    with _conn() as c:
        return [dict(r) for r in c.execute(sql).fetchall()]


# ─── Customers ─────────────────────────────────────────────────────────────────

def get_or_create_customer(platform, brand_id, sender_id, display_name=""):
    """取得或建立客戶記錄，返回 customer dict"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as c:
        c.execute("""
            INSERT INTO customers (platform, brand_id, sender_id, display_name)
            VALUES (?,?,?,?)
            ON CONFLICT(platform, brand_id, sender_id) DO UPDATE SET
                last_seen=?,
                display_name=CASE WHEN excluded.display_name!='' THEN excluded.display_name
                             ELSE display_name END
        """, (platform, brand_id, sender_id, display_name, now))
        row = c.execute(
            "SELECT * FROM customers WHERE platform=? AND brand_id=? AND sender_id=?",
            (platform, brand_id, sender_id)
        ).fetchone()
    return dict(row)


def increment_message_count(customer_id):
    with _conn() as c:
        c.execute("UPDATE customers SET total_messages=total_messages+1 WHERE id=?",
                  (customer_id,))


def update_sentiment(customer_id, score):
    """滾動更新情緒分數（移動平均 0.3 新 + 0.7 舊）"""
    with _conn() as c:
        c.execute("""
            UPDATE customers
            SET sentiment_score = ROUND(sentiment_score*0.7 + ?*0.3, 3)
            WHERE id=?
        """, (score, customer_id))


def mark_vip(customer_id, flag=1):
    with _conn() as c:
        c.execute("UPDATE customers SET vip_flag=? WHERE id=?", (flag, customer_id))


def get_customer_history(customer_id, limit=5):
    """取得最近 N 筆對話，供 AI 回覆用"""
    with _conn() as c:
        rows = c.execute("""
            SELECT message_in, message_out, intent, created_at
            FROM conversations WHERE customer_id=?
            ORDER BY created_at DESC LIMIT ?
        """, (customer_id, limit)).fetchall()
    return [dict(r) for r in reversed(rows)]


def get_pending_notion_customers(limit=50):
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM customers WHERE synced_at IS NULL LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def mark_customer_notion_synced(customer_id, notion_page_id):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as c:
        c.execute("UPDATE customers SET synced_at=?, notion_page_id=? WHERE id=?",
                  (now, notion_page_id, customer_id))


def get_pending_notion_conversations(limit=100):
    with _conn() as c:
        rows = c.execute(
            "SELECT c.*, cu.notion_page_id as customer_notion_id "
            "FROM conversations c "
            "JOIN customers cu ON c.customer_id=cu.id "
            "WHERE c.notion_synced=0 ORDER BY c.created_at LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def mark_conversations_synced(conv_ids):
    with _conn() as c:
        c.executemany("UPDATE conversations SET notion_synced=1 WHERE id=?",
                      [(i,) for i in conv_ids])


# ─── Conversations ─────────────────────────────────────────────────────────────

def log_conversation(customer_id, brand_id, platform,
                     message_in, message_out="", intent="unknown",
                     confidence=0.0, reply_source="ai", response_time_ms=0):
    """記錄一筆對話，返回 conversation id"""
    with _conn() as c:
        cur = c.execute("""
            INSERT INTO conversations
              (customer_id, brand_id, platform, message_in, message_out,
               intent, confidence, reply_source, response_time_ms)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (customer_id, brand_id, platform, message_in, message_out,
              intent, confidence, reply_source, response_time_ms))
        increment_message_count(customer_id)
        return cur.lastrowid


def update_reply(conv_id, message_out, reply_source="ai"):
    """回覆生成後更新 conversation"""
    with _conn() as c:
        c.execute("UPDATE conversations SET message_out=?, reply_source=? WHERE id=?",
                  (message_out, reply_source, conv_id))


# ─── FAQ Entries ───────────────────────────────────────────────────────────────

def add_faq(brand_id, question, answer, keywords=None):
    kw = json.dumps(keywords or [], ensure_ascii=False)
    with _conn() as c:
        c.execute("""
            INSERT INTO faq_entries (brand_id, question, answer, keywords)
            VALUES (?,?,?,?)
        """, (brand_id, question, answer, kw))


def get_faqs(brand_id):
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM faq_entries WHERE brand_id=? ORDER BY match_count DESC",
            (brand_id,)
        ).fetchall()
    results = []
    for r in rows:
        d = dict(r)
        d["keywords"] = json.loads(d.get("keywords") or "[]")
        results.append(d)
    return results


def record_faq_hit(faq_id):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as c:
        c.execute("UPDATE faq_entries SET match_count=match_count+1, last_matched=? WHERE id=?",
                  (now, faq_id))


# ─── Analytics ─────────────────────────────────────────────────────────────────

def get_weekly_stats(brand_id=None, days=7):
    """取得近 N 天統計數據"""
    brand_filter = "AND brand_id=?" if brand_id else ""
    params = [days] + ([brand_id] if brand_id else [])
    with _conn() as c:
        rows = c.execute(f"""
            SELECT
                COUNT(*) as total,
                AVG(confidence) as avg_confidence,
                AVG(response_time_ms) as avg_response_ms,
                SUM(CASE WHEN reply_source='faq' THEN 1 ELSE 0 END) as faq_count,
                SUM(CASE WHEN reply_source='ai' THEN 1 ELSE 0 END) as ai_count,
                SUM(CASE WHEN reply_source='human' THEN 1 ELSE 0 END) as human_count
            FROM conversations
            WHERE created_at >= datetime('now', ?)
            {brand_filter}
        """, [f"-{days} days"] + ([brand_id] if brand_id else [])).fetchone()
    return dict(rows) if rows else {}


def get_top_intents(brand_id=None, days=7, limit=10):
    brand_filter = "AND brand_id=?" if brand_id else ""
    with _conn() as c:
        rows = c.execute(f"""
            SELECT intent, COUNT(*) as cnt
            FROM conversations
            WHERE created_at >= datetime('now', ?) {brand_filter}
            GROUP BY intent ORDER BY cnt DESC LIMIT ?
        """, [f"-{days} days"] + ([brand_id] if brand_id else []) + [limit]).fetchall()
    return [dict(r) for r in rows]


def get_vip_candidates(min_messages=5, min_sentiment=0.6):
    """識別 VIP 潛力客戶"""
    with _conn() as c:
        rows = c.execute("""
            SELECT * FROM customers
            WHERE total_messages>=? AND sentiment_score>=? AND vip_flag=0
        """, (min_messages, min_sentiment)).fetchall()
    return [dict(r) for r in rows]


# ─── Seed demo data ────────────────────────────────────────────────────────────

def seed_demo():
    """插入一個示範品牌 + FAQ"""
    upsert_brand(
        brand_id="demo",
        brand_name="Demo Brand",
        tone_prompt=(
            "你是 Demo Brand 的客服代表。語氣親切、專業。"
            "回覆限 200 字以內。結尾加上 🌟 Demo Brand"
        ),
        auto_reply_enabled=1,
        confidence_threshold=0.70,
    )
    faqs = [
        ("你們有優惠嗎",   "我們每月都有限時優惠！歡迎追蹤我們的官方頁面獲得最新消息 🎉",
         ["優惠", "折扣", "特價", "promotion", "discount"]),
        ("怎麼下訂單",     "您可以直接在官網或私訊我們下單，下單後 24 小時內確認出貨 📦",
         ["下訂", "購買", "訂購", "order", "buy"]),
        ("運費多少",       "滿 $500 免運費！未達免運門檻運費 $60 💰",
         ["運費", "shipping", "郵費", "寄送"]),
        ("退換貨政策",     "收到商品 7 天內可申請退換貨，商品需保持原包裝 ✅",
         ["退貨", "換貨", "退款", "return", "refund"]),
        ("出貨時間",       "一般 1-3 個工作天出貨，節慶期間可能延至 5 個工作天 🚀",
         ["出貨", "幾天", "到貨", "delivery", "shipping time"]),
    ]
    for q, a, kw in faqs:
        existing = get_faqs("demo")
        if not any(f["question"] == q for f in existing):
            add_faq("demo", q, a, kw)
    print("[cs_customer_db] Demo brand + FAQ seeded")


if __name__ == "__main__":
    init_db()
    seed_demo()
    print(f"[cs_customer_db] Ready: {DB_PATH}")
    brand = get_brand_config("demo")
    print(f"  Brand: {brand['brand_name']}, FAQs: {len(get_faqs('demo'))}")
