#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Hub Sync — 排程同步 + 複習提醒
每 30 分鐘由 LaunchAgent 執行：
  1. pull Google Sheets → SQLite
  2. 檢查今日待複習項
  3. 發 Telegram 複習提醒 (每天只發一次)
  4. push 變更回 Google Sheets
v1.0 — 2026-03-04

Usage:
    python3 knowledge_hub_sync.py              # 正常同步
    python3 knowledge_hub_sync.py --dry-run    # 只印出不發送
    python3 knowledge_hub_sync.py --force      # 強制發送提醒（無視已發送記錄）
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime, date

# Ensure knowledge_hub_db is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import knowledge_hub_db

TG_CHAT_ID = "8399476482"
SENT_FLAG_DIR = os.path.expanduser("~/.openclaw/memory")


def send_telegram(msg: str) -> bool:
    """透過 OpenClaw CLI 發送 Telegram 訊息"""
    try:
        r = subprocess.run(
            ["/usr/local/bin/openclaw", "message", "send",
             "--channel", "telegram", "--account", "kira",
             "--target", TG_CHAT_ID, "--message", msg],
            capture_output=True, timeout=20
        )
        return r.returncode == 0
    except Exception as e:
        print(f"[kh_sync] Telegram send failed: {e}")
        return False


def already_sent_today(flag_name: str) -> bool:
    """檢查今日是否已發送過此類提醒"""
    flag_file = os.path.join(SENT_FLAG_DIR, f".kh_{flag_name}_{date.today().isoformat()}")
    return os.path.exists(flag_file)


def mark_sent_today(flag_name: str):
    """標記今日已發送"""
    os.makedirs(SENT_FLAG_DIR, exist_ok=True)
    flag_file = os.path.join(SENT_FLAG_DIR, f".kh_{flag_name}_{date.today().isoformat()}")
    with open(flag_file, "w") as f:
        f.write(datetime.now().isoformat())
    # 清理前天的 flag
    yesterday = date.today().isoformat()
    for fname in os.listdir(SENT_FLAG_DIR):
        if fname.startswith(f".kh_{flag_name}_") and yesterday not in fname and date.today().isoformat() not in fname:
            try:
                os.remove(os.path.join(SENT_FLAG_DIR, fname))
            except OSError:
                pass


def build_review_message(due_items):
    """組合複習提醒訊息"""
    count = len(due_items)
    lines = [
        f"📚 Knowledge Hub — 今日複習提醒",
        f"共 {count} 項待複習",
        "",
    ]

    for item in due_items[:10]:
        stage = item.get("review_stage", 0)
        stage_emoji = ["🔴", "🟡", "🟢", "✅"][min(stage, 3)]
        title = item.get("title", "未命名")
        category = item.get("category", "")
        lid = item.get("learning_id", "")
        lines.append(f"{stage_emoji} [{lid}] {title} ({category})")

    if count > 10:
        lines.append(f"\n... 還有 {count - 10} 項")

    lines.extend([
        "",
        "回覆「複習」開始今天的複習！",
    ])

    return "\n".join(lines)


def build_summary_message(pull_stats, due_count, push_stats):
    """組合同步摘要（僅 dry-run 時使用）"""
    lines = ["📊 Knowledge Hub Sync Summary", ""]

    if pull_stats:
        lines.append("Pull from Sheets:")
        for tab, count in pull_stats.items():
            lines.append(f"  - {tab}: {count} rows")
    else:
        lines.append("Pull: skipped (no Sheet ID or credentials)")

    lines.append(f"\nDue for review today: {due_count}")

    if push_stats:
        lines.append("\nPush to Sheets:")
        for tab, count in push_stats.items():
            lines.append(f"  - {tab}: {count} rows")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Knowledge Hub Sync")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print actions without sending Telegram")
    parser.add_argument("--force", action="store_true",
                        help="Force send review reminder even if already sent today")
    args = parser.parse_args()

    print(f"[kh_sync] Starting sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 0: Init DB
    knowledge_hub_db.init_db()

    # Step 1: Pull from Google Sheets
    print("[kh_sync] Step 1: Pull from Google Sheets...")
    pull_stats = knowledge_hub_db.pull_from_sheets()

    # Step 2: Sync learning hours to projects
    print("[kh_sync] Step 2: Sync learning hours...")
    knowledge_hub_db.sync_learning_hours()

    # Step 3: Check due reviews
    print("[kh_sync] Step 3: Check due reviews...")
    due_items = knowledge_hub_db.get_due_reviews()
    due_count = len(due_items)
    print(f"[kh_sync] Due for review: {due_count} items")

    # Step 4: Send Telegram reminder (once per day, 07:00-10:00 window)
    hour = datetime.now().hour
    should_send = due_count > 0 and (7 <= hour <= 10)
    already_sent = already_sent_today("review_reminder")

    if should_send and (args.force or not already_sent):
        msg = build_review_message(due_items)
        if args.dry_run:
            print("--- DRY RUN: Review Reminder ---")
            print(msg)
            print("--- END ---")
        else:
            ok = send_telegram(msg)
            if ok:
                mark_sent_today("review_reminder")
                print(f"[kh_sync] Review reminder sent ({due_count} items)")
            else:
                print("[kh_sync] WARNING: Failed to send review reminder")
    elif due_count > 0 and already_sent:
        print("[kh_sync] Review reminder already sent today — skip")
    elif due_count == 0:
        print("[kh_sync] No items due for review")
    else:
        print(f"[kh_sync] Outside reminder window (hour={hour}) — skip")

    # Step 5: Push changes to Google Sheets
    print("[kh_sync] Step 5: Push changes to Sheets...")
    push_stats = {}
    for tab_name in ["Projects", "Learning", "Inbox"]:
        result = knowledge_hub_db.push_to_sheets(tab_name)
        if result is not None:
            push_stats[tab_name] = result

    # Summary
    if args.dry_run:
        summary = build_summary_message(pull_stats, due_count, push_stats)
        print("\n" + summary)

    print(f"[kh_sync] Sync complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
