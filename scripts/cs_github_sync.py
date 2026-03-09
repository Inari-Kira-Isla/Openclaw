#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — GitHub 同步
SQLite cs_customers.db → openclaw-workspace/cs-data/
每 15 分鐘由 cron 觸發（取代 Notion 同步）
v1.0 — 2026-03-04
"""

import os
import json
import sqlite3
import subprocess
from datetime import datetime, timezone

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

DB_PATH   = os.path.expanduser(
    os.environ.get("CS_CUSTOMER_DB", "~/.openclaw/memory/cs_customers.db")
)
REPO_DIR  = os.path.expanduser(
    os.environ.get("CS_GITHUB_REPO", "~/.openclaw/github/openclaw-workspace")
)
DATA_DIR  = os.path.join(REPO_DIR, "cs-data")


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def _git(cmd, cwd=REPO_DIR):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()


# ─── Export functions ──────────────────────────────────────────────────────────

def export_brands():
    with _conn() as c:
        rows = c.execute(
            "SELECT brand_id, brand_name, auto_reply_enabled, "
            "confidence_threshold, created_at, updated_at FROM brands"
        ).fetchall()
    return [dict(r) for r in rows]


def export_customers():
    with _conn() as c:
        rows = c.execute("""
            SELECT id, platform, brand_id, sender_id, display_name,
                   first_seen, last_seen, total_messages,
                   ROUND(sentiment_score, 3) as sentiment_score,
                   vip_flag, tags
            FROM customers ORDER BY last_seen DESC
        """).fetchall()
    return [dict(r) for r in rows]


def export_conversations(limit=500):
    """最近 500 筆對話"""
    with _conn() as c:
        rows = c.execute("""
            SELECT c.id, c.customer_id, c.brand_id, c.platform,
                   c.message_in, c.message_out, c.intent,
                   ROUND(c.confidence, 3) as confidence,
                   c.reply_source, c.response_time_ms, c.created_at,
                   cu.display_name as customer_name
            FROM conversations c
            LEFT JOIN customers cu ON c.customer_id = cu.id
            ORDER BY c.created_at DESC LIMIT ?
        """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def export_faq(brand_id=None):
    with _conn() as c:
        if brand_id:
            rows = c.execute(
                "SELECT * FROM faq_entries WHERE brand_id=? ORDER BY match_count DESC",
                (brand_id,)
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT * FROM faq_entries ORDER BY brand_id, match_count DESC"
            ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["keywords"] = json.loads(d.get("keywords") or "[]")
        except Exception:
            d["keywords"] = []
        result.append(d)
    return result


def export_stats():
    """彙總統計"""
    with _conn() as c:
        total_customers = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        total_convs     = c.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        vip_count       = c.execute("SELECT COUNT(*) FROM customers WHERE vip_flag=1").fetchone()[0]
        faq_hits        = c.execute("SELECT SUM(match_count) FROM faq_entries").fetchone()[0] or 0

        # Per brand stats
        brand_stats = c.execute("""
            SELECT cu.brand_id,
                   COUNT(DISTINCT cu.id) as customers,
                   COUNT(cv.id) as conversations,
                   SUM(CASE WHEN cv.reply_source='faq' THEN 1 ELSE 0 END) as faq_replies,
                   SUM(CASE WHEN cv.reply_source='ai' THEN 1 ELSE 0 END) as ai_replies,
                   SUM(CASE WHEN cv.reply_source='human' THEN 1 ELSE 0 END) as human_replies,
                   ROUND(AVG(cu.sentiment_score), 3) as avg_sentiment
            FROM customers cu
            LEFT JOIN conversations cv ON cu.id = cv.customer_id
            GROUP BY cu.brand_id
        """).fetchall()

        # Weekly trend (last 7 days by day)
        daily_trend = c.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM conversations
            WHERE created_at >= datetime('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date
        """).fetchall()

    return {
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "total_customers": total_customers,
        "total_conversations": total_convs,
        "vip_customers":   vip_count,
        "faq_total_hits":  faq_hits,
        "brands":          [dict(r) for r in brand_stats],
        "daily_trend_7d":  [dict(r) for r in daily_trend],
    }


# ─── Markdown dashboard ────────────────────────────────────────────────────────

def build_dashboard_md(stats, brands, customers, convs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    vip_list = [c for c in customers if c.get("vip_flag")]

    brand_rows = "\n".join(
        f"| {b['brand_id']} | {b['customers']} | {b['conversations']} | "
        f"{b['faq_replies']} | {b['ai_replies']} | {b['human_replies']} | "
        f"{b.get('avg_sentiment', 0):.2f} |"
        for b in stats.get("brands", [])
    )

    recent_convs = "\n".join(
        f"| `{cv['brand_id']}` | {cv['customer_name'] or cv['customer_id']} | "
        f"{cv['message_in'][:40]}... | `{cv['reply_source']}` | "
        f"{cv['confidence']:.2f} | {cv['created_at'][:16]} |"
        for cv in convs[:10]
    )

    vip_rows = "\n".join(
        f"| {c['display_name'] or c['sender_id']} | {c['brand_id']} | "
        f"{c['platform']} | {c['total_messages']} | {c['sentiment_score']:.2f} |"
        for c in vip_list[:10]
    )

    return f"""# 📊 CS 客服系統 — 即時儀表板

> 最後更新: {now} | 自動同步自 OpenClaw CS System

## 總覽

| 指標 | 數值 |
|------|------|
| 總客戶數 | {stats['total_customers']} |
| 總對話數 | {stats['total_conversations']} |
| VIP 客戶 | {stats['vip_customers']} |
| FAQ 命中次數 | {stats['faq_total_hits']} |

## 品牌效能

| 品牌 | 客戶數 | 對話數 | FAQ回覆 | AI回覆 | 人工 | 平均情緒 |
|------|--------|--------|---------|--------|------|----------|
{brand_rows if brand_rows else "| (暫無資料) | | | | | | |"}

## 最近 10 筆對話

| 品牌 | 客戶 | 訊息 | 來源 | 信心 | 時間 |
|------|------|------|------|------|------|
{recent_convs if recent_convs else "| (暫無對話) | | | | | |"}

## ⭐ VIP 客戶

| 姓名 | 品牌 | 平台 | 訊息數 | 情緒分數 |
|------|------|------|--------|----------|
{vip_rows if vip_rows else "| (暫無 VIP) | | | | |"}

---
*Generated by OpenClaw CS System · [Source Data](./)*
"""


# ─── Sync pipeline ─────────────────────────────────────────────────────────────

def run():
    print(f"[cs_github_sync] Starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    if not os.path.exists(DB_PATH):
        print(f"[cs_github_sync] DB not found: {DB_PATH}")
        return False

    os.makedirs(DATA_DIR, exist_ok=True)

    # 1. Pull latest first
    ok, out, err = _git(["git", "pull", "--rebase", "--autostash"])
    print(f"  git pull: {'OK' if ok else 'WARN'} {out[:60]}")

    # 2. Export data
    brands    = export_brands()
    customers = export_customers()
    convs     = export_conversations(500)
    faqs      = export_faq()
    stats     = export_stats()

    # 3. Write JSON files
    files_written = []
    for fname, data in [
        ("brands.json",        brands),
        ("customers.json",     customers),
        ("conversations.json", convs),
        ("faq.json",           faqs),
        ("stats.json",         stats),
    ]:
        fpath = os.path.join(DATA_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        files_written.append(fname)

    # 4. Write Markdown dashboard
    dashboard = build_dashboard_md(stats, brands, customers, convs)
    dash_path = os.path.join(DATA_DIR, "README.md")
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(dashboard)
    files_written.append("README.md")

    print(f"  Files written: {', '.join(files_written)}")

    # 5. Git commit + push
    ok, out, err = _git(["git", "add", "cs-data/"])
    ok, out, err = _git(["git", "status", "--porcelain", "cs-data/"])
    if not out.strip():
        print("  No changes to commit")
        return True

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = (
        f"cs: sync {stats['total_customers']} customers, "
        f"{stats['total_conversations']} convs [{ts}]"
    )
    ok, out, err = _git(["git", "commit", "-m", commit_msg])
    if not ok:
        print(f"  Commit failed: {err[:100]}")
        return False

    ok, out, err = _git(["git", "push"])
    if ok:
        print(f"  ✅ Pushed: {commit_msg}")
    else:
        print(f"  Push failed: {err[:100]}")
        return False

    return True


if __name__ == "__main__":
    success = run()
    import sys
    sys.exit(0 if success else 1)
