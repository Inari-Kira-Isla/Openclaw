#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw BNI — 會員與轉介紹資料庫 (SQLite)
bni.db: members / referrals / followups / checkin_log / meetings
v1.0 — 2026-03-04
"""

import os
import json
import sqlite3
from datetime import datetime, date, timedelta

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

DB_PATH = os.path.expanduser(
    os.environ.get("BNI_DB", "~/.openclaw/memory/bni.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT    NOT NULL,
    company           TEXT    NOT NULL,
    title             TEXT    NOT NULL DEFAULT '',
    industry          TEXT    NOT NULL DEFAULT '',
    phone             TEXT    DEFAULT '',
    email             TEXT    DEFAULT '',
    membership_expiry TEXT,
    tags              TEXT    DEFAULT '[]',
    status            TEXT    DEFAULT 'active'
                      CHECK(status IN ('active','paused','left')),
    notes             TEXT    DEFAULT '',
    created_at        TEXT    DEFAULT (datetime('now')),
    updated_at        TEXT    DEFAULT (datetime('now')),
    UNIQUE(name, company)
);
CREATE INDEX IF NOT EXISTS idx_members_industry ON members(industry);
CREATE INDEX IF NOT EXISTS idx_members_status   ON members(status);
CREATE INDEX IF NOT EXISTS idx_members_expiry   ON members(membership_expiry);

CREATE TABLE IF NOT EXISTS referrals (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    giver_id         INTEGER NOT NULL REFERENCES members(id),
    receiver_id      INTEGER NOT NULL REFERENCES members(id),
    client_name      TEXT    DEFAULT '',
    product_service  TEXT    NOT NULL,
    estimated_amount REAL    DEFAULT 0,
    actual_amount    REAL    DEFAULT 0,
    status           TEXT    DEFAULT 'received'
                     CHECK(status IN ('received','contacting','quoting',
                                      'closed_won','closed_lost')),
    status_note      TEXT    DEFAULT '',
    referral_date    TEXT    DEFAULT (date('now')),
    closed_date      TEXT,
    created_at       TEXT    DEFAULT (datetime('now')),
    updated_at       TEXT    DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_ref_giver    ON referrals(giver_id);
CREATE INDEX IF NOT EXISTS idx_ref_receiver ON referrals(receiver_id);
CREATE INDEX IF NOT EXISTS idx_ref_status   ON referrals(status);
CREATE INDEX IF NOT EXISTS idx_ref_date     ON referrals(referral_date);

CREATE TABLE IF NOT EXISTS followups (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name  TEXT    NOT NULL,
    reason       TEXT    NOT NULL,
    due_date     TEXT    NOT NULL,
    last_contact TEXT,
    priority     TEXT    DEFAULT 'normal'
                 CHECK(priority IN ('low','normal','high','urgent')),
    status       TEXT    DEFAULT 'pending'
                 CHECK(status IN ('pending','done','deferred')),
    notes        TEXT    DEFAULT '',
    member_id    INTEGER REFERENCES members(id),
    referral_id  INTEGER REFERENCES referrals(id),
    created_at   TEXT    DEFAULT (datetime('now')),
    updated_at   TEXT    DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_fu_due    ON followups(due_date);
CREATE INDEX IF NOT EXISTS idx_fu_status ON followups(status);

CREATE TABLE IF NOT EXISTS checkin_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date       TEXT    NOT NULL UNIQUE,
    checked_in INTEGER DEFAULT 0,
    checked_at TEXT,
    notes      TEXT    DEFAULT ''
);

CREATE TABLE IF NOT EXISTS meetings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_date TEXT    NOT NULL,
    meeting_type TEXT    DEFAULT 'regular',
    topic        TEXT    DEFAULT '',
    role         TEXT    DEFAULT '',
    attended     INTEGER DEFAULT 1,
    notes        TEXT    DEFAULT '',
    created_at   TEXT    DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_mtg_date ON meetings(meeting_date);
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
    print(f"[bni_db] DB initialised: {DB_PATH}")


# ─── Members ──────────────────────────────────────────────────────────────────

def upsert_member(name, company, title="", industry="", **kwargs):
    """新增或更新會員，返回 member dict"""
    fields = ["name", "company", "title", "industry"] + list(kwargs.keys())
    vals = [name, company, title, industry] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    cols = ",".join(fields)
    update_cols = ",".join(
        f"{k}=excluded.{k}" for k in fields if k not in ("name", "company")
    )
    sql = (f"INSERT INTO members ({cols}) VALUES ({placeholders}) "
           f"ON CONFLICT(name, company) DO UPDATE SET {update_cols}, "
           f"updated_at=datetime('now')")
    with _conn() as c:
        c.execute(sql, vals)
        row = c.execute(
            "SELECT * FROM members WHERE name=? AND company=?",
            (name, company)
        ).fetchone()
    return dict(row)


def get_member(member_id):
    """取得單一會員；不存在返回 None"""
    with _conn() as c:
        row = c.execute("SELECT * FROM members WHERE id=?",
                        (member_id,)).fetchone()
    return dict(row) if row else None


def find_members(query=None, industry=None, status="active"):
    """搜尋會員列表"""
    clauses, params = [], []
    if status:
        clauses.append("status=?")
        params.append(status)
    if industry:
        clauses.append("industry=?")
        params.append(industry)
    if query:
        clauses.append("(name LIKE ? OR company LIKE ? OR notes LIKE ?)")
        params.extend([f"%{query}%"] * 3)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    with _conn() as c:
        rows = c.execute(
            f"SELECT * FROM members {where} ORDER BY name", params
        ).fetchall()
    return [dict(r) for r in rows]


def update_member(member_id, **fields):
    """更新會員欄位"""
    if not fields:
        return get_member(member_id)
    sets = ",".join(f"{k}=?" for k in fields)
    vals = list(fields.values()) + [member_id]
    with _conn() as c:
        c.execute(
            f"UPDATE members SET {sets}, updated_at=datetime('now') WHERE id=?",
            vals
        )
    return get_member(member_id)


def get_expiring_members(days=30):
    """取得即將到期的會員"""
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM members WHERE status='active' "
            "AND membership_expiry IS NOT NULL AND membership_expiry <= ?",
            (cutoff,)
        ).fetchall()
    return [dict(r) for r in rows]


def count_members(status=None):
    """取得會員總數"""
    if status:
        with _conn() as c:
            return c.execute(
                "SELECT COUNT(*) FROM members WHERE status=?", (status,)
            ).fetchone()[0]
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM members").fetchone()[0]


# ─── Referrals ────────────────────────────────────────────────────────────────

def add_referral(giver_id, receiver_id, product_service, **kwargs):
    """新增轉介紹，返回 referral id"""
    fields = ["giver_id", "receiver_id", "product_service"] + list(kwargs.keys())
    vals = [giver_id, receiver_id, product_service] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    cols = ",".join(fields)
    with _conn() as c:
        cur = c.execute(
            f"INSERT INTO referrals ({cols}) VALUES ({placeholders})", vals
        )
        return cur.lastrowid


def update_referral_status(referral_id, status, **kwargs):
    """更新轉介紹狀態"""
    sets = ["status=?"]
    vals = [status]
    for k, v in kwargs.items():
        sets.append(f"{k}=?")
        vals.append(v)
    vals.append(referral_id)
    with _conn() as c:
        c.execute(
            f"UPDATE referrals SET {','.join(sets)}, updated_at=datetime('now') "
            f"WHERE id=?", vals
        )
        row = c.execute("SELECT * FROM referrals WHERE id=?",
                        (referral_id,)).fetchone()
    return dict(row) if row else None


def get_referrals(receiver_id=None, giver_id=None, status=None,
                  date_from=None, date_to=None):
    """查詢轉介紹列表"""
    clauses, params = [], []
    if receiver_id:
        clauses.append("receiver_id=?")
        params.append(receiver_id)
    if giver_id:
        clauses.append("giver_id=?")
        params.append(giver_id)
    if status:
        clauses.append("status=?")
        params.append(status)
    if date_from:
        clauses.append("referral_date>=?")
        params.append(date_from)
    if date_to:
        clauses.append("referral_date<=?")
        params.append(date_to)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    with _conn() as c:
        rows = c.execute(
            f"SELECT r.*, g.name as giver_name, v.name as receiver_name "
            f"FROM referrals r "
            f"JOIN members g ON r.giver_id=g.id "
            f"JOIN members v ON r.receiver_id=v.id "
            f"{where} ORDER BY referral_date DESC", params
        ).fetchall()
    return [dict(r) for r in rows]


def get_referral_stats(date_from=None, date_to=None):
    """取得轉介紹統計"""
    clauses, params = [], []
    if date_from:
        clauses.append("referral_date>=?")
        params.append(date_from)
    if date_to:
        clauses.append("referral_date<=?")
        params.append(date_to)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    with _conn() as c:
        row = c.execute(f"""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status='closed_won' THEN 1 ELSE 0 END) as won,
                SUM(CASE WHEN status='closed_lost' THEN 1 ELSE 0 END) as lost,
                SUM(CASE WHEN status NOT IN ('closed_won','closed_lost')
                    THEN 1 ELSE 0 END) as active,
                COALESCE(SUM(estimated_amount), 0) as total_estimated,
                COALESCE(SUM(CASE WHEN status='closed_won'
                    THEN actual_amount ELSE 0 END), 0) as total_actual
            FROM referrals {where}
        """, params).fetchone()
    return dict(row) if row else {}


# ─── Followups ────────────────────────────────────────────────────────────────

def add_followup(client_name, reason, due_date, **kwargs):
    """新增跟進事項，返回 followup id"""
    fields = ["client_name", "reason", "due_date"] + list(kwargs.keys())
    vals = [client_name, reason, due_date] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    cols = ",".join(fields)
    with _conn() as c:
        cur = c.execute(
            f"INSERT INTO followups ({cols}) VALUES ({placeholders})", vals
        )
        return cur.lastrowid


def get_due_followups(scope="due_today"):
    """取得待處理的跟進事項
    scope: due_today | overdue | upcoming_3d | all_pending
    """
    today = date.today().isoformat()
    upcoming = (date.today() + timedelta(days=3)).isoformat()
    scope_map = {
        "due_today": ("due_date=? AND status='pending'", [today]),
        "overdue": ("due_date<? AND status='pending'", [today]),
        "upcoming_3d": ("due_date<=? AND status='pending'", [upcoming]),
        "all_pending": ("status='pending'", []),
    }
    clause, params = scope_map.get(scope, scope_map["due_today"])
    with _conn() as c:
        rows = c.execute(
            f"SELECT * FROM followups WHERE {clause} ORDER BY due_date, priority DESC",
            params
        ).fetchall()
    return [dict(r) for r in rows]


def mark_followup_done(followup_id, notes=""):
    """標記跟進完成"""
    with _conn() as c:
        c.execute(
            "UPDATE followups SET status='done', notes=?, "
            "updated_at=datetime('now') WHERE id=?",
            (notes, followup_id)
        )


def defer_followup(followup_id, days=1):
    """延後跟進"""
    with _conn() as c:
        c.execute(
            "UPDATE followups SET due_date=date(due_date, ?), "
            "status='pending', updated_at=datetime('now') WHERE id=?",
            (f"+{days} days", followup_id)
        )


# ─── Check-in ────────────────────────────────────────────────────────────────

def log_checkin(date_str=None, notes=""):
    """記錄每日簽到"""
    d = date_str or date.today().isoformat()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as c:
        c.execute(
            "INSERT INTO checkin_log (date, checked_in, checked_at, notes) "
            "VALUES (?,1,?,?) ON CONFLICT(date) DO UPDATE SET "
            "checked_in=1, checked_at=excluded.checked_at, notes=excluded.notes",
            (d, now, notes)
        )


def get_checkin_streak():
    """取得連續簽到天數"""
    today = date.today()
    streak = 0
    with _conn() as c:
        for i in range(365):
            d = (today - timedelta(days=i)).isoformat()
            row = c.execute(
                "SELECT checked_in FROM checkin_log WHERE date=?", (d,)
            ).fetchone()
            if row and row[0]:
                streak += 1
            else:
                break
    return streak


def get_missed_checkins(days=7):
    """取得近 N 天未簽到天數"""
    today = date.today()
    missed = 0
    with _conn() as c:
        for i in range(days):
            d = (today - timedelta(days=i)).isoformat()
            row = c.execute(
                "SELECT checked_in FROM checkin_log WHERE date=?", (d,)
            ).fetchone()
            if not row or not row[0]:
                missed += 1
    return missed


# ─── Meetings ────────────────────────────────────────────────────────────────

def log_meeting(meeting_date, **kwargs):
    """記錄 BNI 會議"""
    fields = ["meeting_date"] + list(kwargs.keys())
    vals = [meeting_date] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    cols = ",".join(fields)
    with _conn() as c:
        cur = c.execute(
            f"INSERT INTO meetings ({cols}) VALUES ({placeholders})", vals
        )
        return cur.lastrowid


def get_next_meeting_date():
    """取得下一個 BNI 會議日期（預設每週二）"""
    today = date.today()
    days_until_tuesday = (1 - today.weekday()) % 7
    if days_until_tuesday == 0 and datetime.now().hour >= 12:
        days_until_tuesday = 7
    return (today + timedelta(days=days_until_tuesday)).isoformat()


def get_recent_meetings(limit=5):
    """取得最近會議紀錄"""
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM meetings ORDER BY meeting_date DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


# ─── Weekly Report Data ──────────────────────────────────────────────────────

def get_weekly_report_data(week_start=None):
    """取得本週報告數據"""
    if week_start is None:
        today = date.today()
        week_start = (today - timedelta(days=today.weekday())).isoformat()
    week_end = (date.fromisoformat(week_start) + timedelta(days=6)).isoformat()

    stats = get_referral_stats(date_from=week_start, date_to=week_end)
    with _conn() as c:
        new_members = c.execute(
            "SELECT COUNT(*) FROM members WHERE created_at>=? AND created_at<=?",
            (week_start, week_end + " 23:59:59")
        ).fetchone()[0]
        meetings_count = c.execute(
            "SELECT COUNT(*) FROM meetings WHERE meeting_date>=? AND meeting_date<=?",
            (week_start, week_end)
        ).fetchone()[0]
        followups_done = c.execute(
            "SELECT COUNT(*) FROM followups WHERE status='done' "
            "AND updated_at>=? AND updated_at<=?",
            (week_start, week_end + " 23:59:59")
        ).fetchone()[0]

    return {
        "week_start": week_start,
        "week_end": week_end,
        "referral_stats": stats,
        "new_members": new_members,
        "meetings_attended": meetings_count,
        "followups_completed": followups_done,
        "total_active_members": count_members(status="active"),
    }


# ─── Seed demo data ─────────────────────────────────────────────────────────

def seed_demo():
    """插入示範數據"""
    m1 = upsert_member("王大明", "ABC 科技", "技術總監", "資訊業",
                       phone="0912345678", email="wang@abc.com")
    m2 = upsert_member("李小華", "XYZ 保險", "業務經理", "保險業",
                       phone="0923456789", email="lee@xyz.com")
    m3 = upsert_member("張美玲", "設計工坊", "創意總監", "設計業",
                       phone="0934567890", email="chang@design.com")

    add_referral(m1["id"], m2["id"], "企業資安評估", estimated_amount=80000)
    add_referral(m2["id"], m3["id"], "公司團險方案", estimated_amount=120000)

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    add_followup("陳先生", "網站改版需求討論", date.today().isoformat(),
                 priority="high", member_id=m1["id"])
    add_followup("林小姐", "保險方案回覆", tomorrow,
                 priority="normal", member_id=m2["id"])

    print(f"[bni_db] Demo data seeded: {count_members()} members, "
          f"{len(get_referrals())} referrals, "
          f"{len(get_due_followups('all_pending'))} followups")


if __name__ == "__main__":
    init_db()
    seed_demo()
    print(f"[bni_db] Ready: {DB_PATH}")
