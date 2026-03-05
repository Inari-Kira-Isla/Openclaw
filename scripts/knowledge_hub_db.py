#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Knowledge Hub — 知識庫與學習追蹤資料庫 (SQLite + Google Sheets)
knowledge_hub.db: projects / learning / inbox / sync_log
v1.0 — 2026-03-04
"""

import os
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
    os.environ.get("KNOWLEDGE_HUB_DB", "~/.openclaw/memory/knowledge_hub.db")
)

GOOGLE_SA_FILE = os.path.expanduser(
    os.environ.get("GOOGLE_SA_FILE", "~/.openclaw/credentials/google-sa.json")
)

SHEET_ID = os.environ.get("KNOWLEDGE_HUB_SHEET_ID", "")

# Tab ↔ Table mapping
_TAB_MAP = {
    "Projects":  "projects",
    "Learning":  "learning",
    "Inbox":     "inbox",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    project_id          TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    status              TEXT DEFAULT 'Planning'
                        CHECK(status IN ('Planning','Active','On Hold','Done','Cancelled')),
    priority            TEXT DEFAULT 'P2-Medium',
    deadline            TEXT,
    progress            INTEGER DEFAULT 0,
    total_learning_hours REAL DEFAULT 0,
    description         TEXT DEFAULT '',
    tags                TEXT DEFAULT '',
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),
    notes               TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_proj_status   ON projects(status);
CREATE INDEX IF NOT EXISTS idx_proj_priority ON projects(priority);
CREATE INDEX IF NOT EXISTS idx_proj_deadline ON projects(deadline);

CREATE TABLE IF NOT EXISTS learning (
    learning_id         TEXT PRIMARY KEY,
    title               TEXT NOT NULL,
    category            TEXT DEFAULT 'Tech Insight'
                        CHECK(category IN ('Tech Insight','Error Log','Tutorial',
                                           'Concept','Tool','Pattern')),
    content             TEXT DEFAULT '',
    tags                TEXT DEFAULT '',
    project_id          TEXT,
    hours_spent         REAL DEFAULT 0,
    source              TEXT DEFAULT '',
    review_stage        INTEGER DEFAULT 0,
    next_review_date    TEXT,
    last_reviewed_at    TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),
    confidence          TEXT DEFAULT 'Low'
                        CHECK(confidence IN ('Low','Medium','High'))
);
CREATE INDEX IF NOT EXISTS idx_learn_category   ON learning(category);
CREATE INDEX IF NOT EXISTS idx_learn_project    ON learning(project_id);
CREATE INDEX IF NOT EXISTS idx_learn_review     ON learning(next_review_date);
CREATE INDEX IF NOT EXISTS idx_learn_confidence ON learning(confidence);

CREATE TABLE IF NOT EXISTS inbox (
    inbox_id            TEXT PRIMARY KEY,
    content             TEXT NOT NULL,
    source              TEXT DEFAULT 'manual',
    processed           INTEGER DEFAULT 0,
    moved_to            TEXT DEFAULT '',
    tags                TEXT DEFAULT '',
    created_at          TEXT DEFAULT (datetime('now')),
    priority            TEXT DEFAULT 'Medium'
);
CREATE INDEX IF NOT EXISTS idx_inbox_processed ON inbox(processed);
CREATE INDEX IF NOT EXISTS idx_inbox_priority  ON inbox(priority);

CREATE TABLE IF NOT EXISTS sync_log (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    direction           TEXT,
    tab_name            TEXT,
    rows_affected       INTEGER,
    synced_at           TEXT DEFAULT (datetime('now'))
);
"""

# Column order for each table (used for Sheets sync)
_PROJECTS_COLS = [
    "project_id", "name", "status", "priority", "deadline", "progress",
    "total_learning_hours", "description", "tags", "created_at", "updated_at", "notes",
]
_LEARNING_COLS = [
    "learning_id", "title", "category", "content", "tags", "project_id",
    "hours_spent", "source", "review_stage", "next_review_date",
    "last_reviewed_at", "created_at", "updated_at", "confidence",
]
_INBOX_COLS = [
    "inbox_id", "content", "source", "processed", "moved_to", "tags",
    "created_at", "priority",
]

_TABLE_COLS = {
    "projects": _PROJECTS_COLS,
    "learning": _LEARNING_COLS,
    "inbox":    _INBOX_COLS,
}

_TABLE_ID_COL = {
    "projects": "project_id",
    "learning": "learning_id",
    "inbox":    "inbox_id",
}

_TABLE_ID_PREFIX = {
    "projects": "P",
    "learning": "L",
    "inbox":    "I",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Connection & Init
# ═══════════════════════════════════════════════════════════════════════════════

def _conn():
    """取得 SQLite 連線 (WAL mode, Row factory)"""
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
    print(f"[knowledge_hub_db] DB initialised: {DB_PATH}")


def _next_id(prefix, table, id_col):
    """生成下一個 ID (e.g. P-001, L-042, I-007)"""
    with _conn() as c:
        row = c.execute(
            f"SELECT {id_col} FROM {table} ORDER BY {id_col} DESC LIMIT 1"
        ).fetchone()
    if row and row[0]:
        try:
            num = int(row[0].split("-", 1)[1]) + 1
        except (ValueError, IndexError):
            num = 1
    else:
        num = 1
    return f"{prefix}-{num:03d}"


# ═══════════════════════════════════════════════════════════════════════════════
# Google Sheets Integration
# ═══════════════════════════════════════════════════════════════════════════════

def _get_gspread_client():
    """取得 gspread client (Service Account)。若無憑證檔案則回傳 None"""
    if not os.path.exists(GOOGLE_SA_FILE):
        print(f"[knowledge_hub_db] WARNING: Google SA file not found: {GOOGLE_SA_FILE}")
        print("[knowledge_hub_db] Google Sheets sync disabled — SQLite-only mode")
        return None
    try:
        import gspread
        gc = gspread.service_account(filename=GOOGLE_SA_FILE)
        return gc
    except Exception as e:
        print(f"[knowledge_hub_db] WARNING: gspread init failed: {e}")
        return None


def pull_from_sheets():
    """從 Google Sheets 下載 3 個 tab 的資料到 SQLite (REPLACE INTO)
    Returns: dict with pull stats or None on failure
    """
    if not SHEET_ID:
        print("[knowledge_hub_db] KNOWLEDGE_HUB_SHEET_ID not set — skip pull")
        return None

    gc = _get_gspread_client()
    if gc is None:
        return None

    try:
        spreadsheet = gc.open_by_key(SHEET_ID)
    except Exception as e:
        print(f"[knowledge_hub_db] Cannot open spreadsheet: {e}")
        return None

    stats = {}
    with _conn() as c:
        for tab_name, table_name in _TAB_MAP.items():
            try:
                ws = spreadsheet.worksheet(tab_name)
                records = ws.get_all_records()
            except Exception as e:
                print(f"[knowledge_hub_db] Cannot read tab '{tab_name}': {e}")
                stats[tab_name] = 0
                continue

            cols = _TABLE_COLS[table_name]
            count = 0
            for record in records:
                # Map sheet headers to DB columns (use col name as-is)
                vals = []
                for col in cols:
                    val = record.get(col, "")
                    vals.append(val if val != "" else None)

                placeholders = ",".join("?" * len(cols))
                col_str = ",".join(cols)
                c.execute(
                    f"INSERT OR REPLACE INTO {table_name} ({col_str}) "
                    f"VALUES ({placeholders})",
                    vals,
                )
                count += 1

            # Log sync
            c.execute(
                "INSERT INTO sync_log (direction, tab_name, rows_affected) "
                "VALUES ('pull', ?, ?)",
                (tab_name, count),
            )
            stats[tab_name] = count
            print(f"[knowledge_hub_db] Pulled {count} rows from '{tab_name}'")

    return stats


def push_to_sheets(tab_name):
    """將 SQLite 資料推送到 Google Sheets 指定 tab
    Args:
        tab_name: Sheet tab 名稱 ('Projects', 'Learning', 'Inbox')
    Returns: rows pushed count or None on failure
    """
    if not SHEET_ID:
        print("[knowledge_hub_db] KNOWLEDGE_HUB_SHEET_ID not set — skip push")
        return None

    gc = _get_gspread_client()
    if gc is None:
        return None

    table_name = _TAB_MAP.get(tab_name)
    if table_name is None:
        print(f"[knowledge_hub_db] Unknown tab: {tab_name}")
        return None

    try:
        spreadsheet = gc.open_by_key(SHEET_ID)
        ws = spreadsheet.worksheet(tab_name)
    except Exception as e:
        print(f"[knowledge_hub_db] Cannot open tab '{tab_name}': {e}")
        return None

    cols = _TABLE_COLS[table_name]

    with _conn() as c:
        rows = c.execute(f"SELECT * FROM {table_name}").fetchall()
        data = []
        for row in rows:
            row_dict = dict(row)
            data.append([str(row_dict.get(col, "") or "") for col in cols])

    # Clear sheet and write
    try:
        ws.clear()
        # Write header row
        ws.update(range_name="A1", values=[cols])
        # Write data rows
        if data:
            ws.update(range_name="A2", values=data)

        count = len(data)

        # Log sync
        with _conn() as c:
            c.execute(
                "INSERT INTO sync_log (direction, tab_name, rows_affected) "
                "VALUES ('push', ?, ?)",
                (tab_name, count),
            )

        print(f"[knowledge_hub_db] Pushed {count} rows to '{tab_name}'")
        return count

    except Exception as e:
        print(f"[knowledge_hub_db] Push to '{tab_name}' failed: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# Projects CRUD
# ═══════════════════════════════════════════════════════════════════════════════

def add_project(name, **kwargs):
    """新增專案，返回 project dict
    可選 kwargs: status, priority, deadline, progress, description, tags, notes
    """
    pid = _next_id("P", "projects", "project_id")
    fields = ["project_id", "name"] + list(kwargs.keys())
    vals = [pid, name] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    col_str = ",".join(fields)
    with _conn() as c:
        c.execute(
            f"INSERT INTO projects ({col_str}) VALUES ({placeholders})", vals
        )
        row = c.execute(
            "SELECT * FROM projects WHERE project_id=?", (pid,)
        ).fetchone()
    return dict(row)


def get_project(project_id):
    """取得單一專案；不存在返回 None"""
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM projects WHERE project_id=?", (project_id,)
        ).fetchone()
    return dict(row) if row else None


def query_projects(status=None, priority=None):
    """查詢專案列表，可依 status / priority 過濾"""
    clauses, params = [], []
    if status:
        clauses.append("status=?")
        params.append(status)
    if priority:
        clauses.append("priority=?")
        params.append(priority)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    with _conn() as c:
        rows = c.execute(
            f"SELECT * FROM projects {where} ORDER BY priority, name", params
        ).fetchall()
    return [dict(r) for r in rows]


def update_project(project_id, **kwargs):
    """更新專案欄位"""
    if not kwargs:
        return get_project(project_id)
    sets = ",".join(f"{k}=?" for k in kwargs)
    vals = list(kwargs.values()) + [project_id]
    with _conn() as c:
        c.execute(
            f"UPDATE projects SET {sets}, updated_at=datetime('now') "
            f"WHERE project_id=?",
            vals,
        )
    return get_project(project_id)


def get_project_summary():
    """取得專案統計摘要：總數、各狀態數量、逾期數"""
    today = date.today().isoformat()
    with _conn() as c:
        total = c.execute("SELECT COUNT(*) FROM projects").fetchone()[0]

        status_rows = c.execute(
            "SELECT status, COUNT(*) as cnt FROM projects GROUP BY status"
        ).fetchall()
        by_status = {r["status"]: r["cnt"] for r in status_rows}

        overdue = c.execute(
            "SELECT COUNT(*) FROM projects "
            "WHERE deadline IS NOT NULL AND deadline < ? "
            "AND status NOT IN ('Done', 'Cancelled')",
            (today,),
        ).fetchone()[0]

    return {
        "total": total,
        "by_status": by_status,
        "overdue": overdue,
    }


def sync_learning_hours():
    """從 learning 表聚合 hours_spent，更新每個 project 的 total_learning_hours"""
    with _conn() as c:
        c.execute("""
            UPDATE projects SET total_learning_hours = COALESCE((
                SELECT SUM(hours_spent)
                FROM learning
                WHERE learning.project_id = projects.project_id
            ), 0),
            updated_at = datetime('now')
        """)
        affected = c.execute(
            "SELECT changes()"
        ).fetchone()[0]
    print(f"[knowledge_hub_db] Synced learning hours for {affected} projects")
    return affected


# ═══════════════════════════════════════════════════════════════════════════════
# Learning CRUD
# ═══════════════════════════════════════════════════════════════════════════════

def add_learning(title, category="Tech Insight", content="", **kwargs):
    """新增學習紀錄，返回 learning dict
    自動設定 NextReviewDate 為明天
    可選 kwargs: tags, project_id, hours_spent, source, confidence
    """
    lid = _next_id("L", "learning", "learning_id")
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    fields = ["learning_id", "title", "category", "content", "next_review_date"]
    vals = [lid, title, category, content, tomorrow]

    for k, v in kwargs.items():
        fields.append(k)
        vals.append(v)

    placeholders = ",".join("?" * len(fields))
    col_str = ",".join(fields)
    with _conn() as c:
        c.execute(
            f"INSERT INTO learning ({col_str}) VALUES ({placeholders})", vals
        )
        row = c.execute(
            "SELECT * FROM learning WHERE learning_id=?", (lid,)
        ).fetchone()
    return dict(row)


def get_learning(learning_id):
    """取得單一學習紀錄；不存在返回 None"""
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM learning WHERE learning_id=?", (learning_id,)
        ).fetchone()
    return dict(row) if row else None


def query_learning(query=None, category=None, tags=None, project_id=None, limit=50):
    """查詢學習紀錄，支援關鍵字搜尋 (LIKE on title/content/tags)"""
    clauses, params = [], []
    if query:
        clauses.append("(title LIKE ? OR content LIKE ? OR tags LIKE ?)")
        params.extend([f"%{query}%"] * 3)
    if category:
        clauses.append("category=?")
        params.append(category)
    if tags:
        clauses.append("tags LIKE ?")
        params.append(f"%{tags}%")
    if project_id:
        clauses.append("project_id=?")
        params.append(project_id)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    with _conn() as c:
        rows = c.execute(
            f"SELECT * FROM learning {where} "
            f"ORDER BY updated_at DESC LIMIT ?",
            params + [limit],
        ).fetchall()
    return [dict(r) for r in rows]


def update_learning(learning_id, **kwargs):
    """更新學習紀錄欄位"""
    if not kwargs:
        return get_learning(learning_id)
    sets = ",".join(f"{k}=?" for k in kwargs)
    vals = list(kwargs.values()) + [learning_id]
    with _conn() as c:
        c.execute(
            f"UPDATE learning SET {sets}, updated_at=datetime('now') "
            f"WHERE learning_id=?",
            vals,
        )
    return get_learning(learning_id)


# ═══════════════════════════════════════════════════════════════════════════════
# Spaced Repetition — 間隔重複學習
# ═══════════════════════════════════════════════════════════════════════════════

# Stage → days until next review
_REVIEW_INTERVALS = {
    0: 1,     # Stage 0 → 1 day
    1: 7,     # Stage 1 → 7 days
    2: 30,    # Stage 2 → 30 days
    3: None,  # Stage 3 → mastered, no more review
}


def get_due_reviews():
    """取得今日到期需複習的學習紀錄 (review_stage < 3)"""
    today = date.today().isoformat()
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM learning "
            "WHERE next_review_date <= ? AND review_stage < 3 "
            "ORDER BY next_review_date ASC",
            (today,),
        ).fetchall()
    return [dict(r) for r in rows]


def mark_reviewed(learning_id, confidence="Medium"):
    """標記已複習：推進 review_stage，計算下次複習日期
    Stage progression: 0→1 (1d) → 1→2 (7d) → 2→3 (30d) → 3 (mastered)
    """
    item = get_learning(learning_id)
    if item is None:
        return None

    current_stage = item["review_stage"] or 0
    new_stage = min(current_stage + 1, 3)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    interval = _REVIEW_INTERVALS.get(new_stage)
    if interval is not None:
        next_date = (date.today() + timedelta(days=interval)).isoformat()
    else:
        next_date = None  # mastered — no more reviews

    with _conn() as c:
        c.execute(
            "UPDATE learning SET "
            "review_stage=?, next_review_date=?, last_reviewed_at=?, "
            "confidence=?, updated_at=datetime('now') "
            "WHERE learning_id=?",
            (new_stage, next_date, now_str, confidence, learning_id),
        )

    return get_learning(learning_id)


# ═══════════════════════════════════════════════════════════════════════════════
# Inbox CRUD
# ═══════════════════════════════════════════════════════════════════════════════

def add_inbox(content, source="manual", **kwargs):
    """新增收件匣項目，返回 inbox dict
    可選 kwargs: tags, priority
    """
    iid = _next_id("I", "inbox", "inbox_id")
    fields = ["inbox_id", "content", "source"] + list(kwargs.keys())
    vals = [iid, content, source] + list(kwargs.values())
    placeholders = ",".join("?" * len(fields))
    col_str = ",".join(fields)
    with _conn() as c:
        c.execute(
            f"INSERT INTO inbox ({col_str}) VALUES ({placeholders})", vals
        )
        row = c.execute(
            "SELECT * FROM inbox WHERE inbox_id=?", (iid,)
        ).fetchone()
    return dict(row)


def query_inbox(processed=None, limit=50):
    """查詢收件匣，可依 processed 狀態過濾"""
    clauses, params = [], []
    if processed is not None:
        clauses.append("processed=?")
        params.append(int(processed))
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    with _conn() as c:
        rows = c.execute(
            f"SELECT * FROM inbox {where} ORDER BY created_at DESC LIMIT ?",
            params + [limit],
        ).fetchall()
    return [dict(r) for r in rows]


def process_inbox(inbox_id, move_to):
    """處理收件匣項目：標記 processed=1，設定 moved_to"""
    with _conn() as c:
        c.execute(
            "UPDATE inbox SET processed=1, moved_to=? WHERE inbox_id=?",
            (move_to, inbox_id),
        )
        row = c.execute(
            "SELECT * FROM inbox WHERE inbox_id=?", (inbox_id,)
        ).fetchone()
    return dict(row) if row else None


# ═══════════════════════════════════════════════════════════════════════════════
# Search — 全文搜尋
# ═══════════════════════════════════════════════════════════════════════════════

def search(query, limit=20):
    """跨表全文搜尋 (projects.name/description, learning.title/content, inbox.content)
    Returns: list of dicts with _source field indicating origin table
    """
    pattern = f"%{query}%"
    results = []

    with _conn() as c:
        # Search projects
        rows = c.execute(
            "SELECT *, 'project' as _source FROM projects "
            "WHERE name LIKE ? OR description LIKE ? "
            "ORDER BY updated_at DESC LIMIT ?",
            (pattern, pattern, limit),
        ).fetchall()
        results.extend(dict(r) for r in rows)

        # Search learning
        rows = c.execute(
            "SELECT *, 'learning' as _source FROM learning "
            "WHERE title LIKE ? OR content LIKE ? "
            "ORDER BY updated_at DESC LIMIT ?",
            (pattern, pattern, limit),
        ).fetchall()
        results.extend(dict(r) for r in rows)

        # Search inbox
        rows = c.execute(
            "SELECT *, 'inbox' as _source FROM inbox "
            "WHERE content LIKE ? "
            "ORDER BY created_at DESC LIMIT ?",
            (pattern, limit),
        ).fetchall()
        results.extend(dict(r) for r in rows)

    # Sort by most recently updated and cap at limit
    results.sort(
        key=lambda x: x.get("updated_at") or x.get("created_at") or "",
        reverse=True,
    )
    return results[:limit]


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    init_db()

    # Print status
    with _conn() as c:
        p_count = c.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        l_count = c.execute("SELECT COUNT(*) FROM learning").fetchone()[0]
        i_count = c.execute("SELECT COUNT(*) FROM inbox").fetchone()[0]
    print(f"[knowledge_hub_db] Status: {p_count} projects, "
          f"{l_count} learning entries, {i_count} inbox items")

    # Try pulling from Google Sheets
    if SHEET_ID:
        print("[knowledge_hub_db] Attempting pull from Google Sheets...")
        pull_from_sheets()
    else:
        print("[knowledge_hub_db] No KNOWLEDGE_HUB_SHEET_ID set — "
              "running in SQLite-only mode")

    print(f"[knowledge_hub_db] Ready: {DB_PATH}")
