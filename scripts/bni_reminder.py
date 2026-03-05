#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BNI Reminder System — 定時提醒腳本
透過 Telegram 推送 BNI 相關提醒通知。
v1.0 — 2026-03-04

Usage:
    python3 bni_reminder.py --type {bni_meeting|bni_report|daily_checkin|followup}
    python3 bni_reminder.py --auto   # 根據當前時間自動判斷類型
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime, date, timedelta

# Ensure bni_db is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bni_db

TG_CHAT_ID = "8399476482"
WEEKDAY_NAMES = ["一", "二", "三", "四", "五", "六", "日"]


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
        print(f"[bni_reminder] Telegram send failed: {e}")
        return False


def remind_bni_meeting() -> str:
    """週二 06:30 — BNI 例會提醒"""
    today = date.today()
    next_mtg = bni_db.get_next_meeting_date()

    # 取得本週轉介紹數據
    week_start = (today - timedelta(days=today.weekday())).isoformat()
    stats = bni_db.get_referral_stats(date_from=week_start)

    # 取得待跟進項目
    overdue = bni_db.get_due_followups("overdue")
    due_today = bni_db.get_due_followups("due_today")
    pending_count = len(overdue) + len(due_today)

    # 取得活躍會員數
    member_count = bni_db.count_members(status="active")

    lines = [
        f"📅 BNI 例會提醒 — {today.isoformat()}（週{WEEKDAY_NAMES[today.weekday()]}）",
        "",
        "⏰ 時間：早上 7:00",
        "📍 請提早 10 分鐘到場",
        "",
        "📋 會前準備：",
        "  - 準備 60 秒自我介紹",
        "  - 攜帶名片",
        f"  - 本週轉介紹：{stats.get('total', 0)} 筆",
    ]

    if pending_count > 0:
        lines.append(f"  - 待跟進事項：{pending_count} 筆")

    if member_count > 0:
        lines.append(f"\n👥 目前活躍會員：{member_count} 人")

    if overdue:
        lines.append("\n⚠️ 逾期跟進：")
        for f in overdue[:3]:
            lines.append(f"  - {f['client_name']}：{f['reason']}")

    lines.append("\n加油！讓今天的會議更有收穫 💪")

    return "\n".join(lines)


def remind_bni_report() -> str:
    """週五 17:00 — 本週報告提醒"""
    data = bni_db.get_weekly_report_data()
    rs = data["referral_stats"]

    lines = [
        f"📊 BNI 本週報告 — {data['week_start']} ~ {data['week_end']}",
        "",
        "🤝 轉介紹統計：",
        f"  - 總數：{rs.get('total', 0)} 筆",
        f"  - 進行中：{rs.get('active', 0)} 筆",
        f"  - 成交：{rs.get('won', 0)} 筆",
        f"  - 未成交：{rs.get('lost', 0)} 筆",
    ]

    if rs.get("total_estimated", 0) > 0:
        lines.append(f"  - 預估金額：${rs['total_estimated']:,.0f}")
    if rs.get("total_actual", 0) > 0:
        lines.append(f"  - 實際成交：${rs['total_actual']:,.0f}")

    lines.extend([
        "",
        f"👥 活躍會員：{data['total_active_members']} 人",
        f"🆕 本週新增：{data['new_members']} 人",
        f"📅 會議出席：{data['meetings_attended']} 次",
        f"✅ 跟進完成：{data['followups_completed']} 筆",
    ])

    # 未完成跟進
    pending = bni_db.get_due_followups("all_pending")
    if pending:
        lines.append(f"\n📌 尚有 {len(pending)} 筆待處理跟進")

    lines.append("\n辛苦了！好好享受週末 🎉")

    return "\n".join(lines)


def remind_daily_checkin() -> str:
    """每天 08:00 — 每日簽到"""
    today = date.today()
    streak = bni_db.get_checkin_streak()

    # 今日待跟進
    due_today = bni_db.get_due_followups("due_today")
    overdue = bni_db.get_due_followups("overdue")

    # 下次會議
    next_mtg = bni_db.get_next_meeting_date()
    days_to_mtg = (date.fromisoformat(next_mtg) - today).days

    lines = [
        f"🌅 早安！每日簽到 — {today.isoformat()}（週{WEEKDAY_NAMES[today.weekday()]}）",
    ]

    if streak > 0:
        lines.append(f"🔥 連續簽到：{streak} 天")

    lines.append("")

    if due_today:
        lines.append(f"✅ 今日待辦（{len(due_today)} 筆）：")
        for f in due_today:
            pri = "🔴" if f["priority"] in ("high", "urgent") else "🟡"
            lines.append(f"  {pri} {f['client_name']}：{f['reason']}")
        lines.append("")

    if overdue:
        lines.append(f"⚠️ 逾期未處理（{len(overdue)} 筆）：")
        for f in overdue[:5]:
            lines.append(f"  - {f['client_name']}：{f['reason']}（到期 {f['due_date']}）")
        lines.append("")

    if days_to_mtg <= 2:
        lines.append(f"📅 BNI 會議倒數 {days_to_mtg} 天！")
    else:
        lines.append(f"📅 下次 BNI 會議：{next_mtg}（{days_to_mtg} 天後）")

    if not due_today and not overdue:
        lines.append("\n🎯 今天沒有待辦事項，可以專注開發新客戶！")

    lines.append("\n回覆「簽到」開始今天的工作！")

    return "\n".join(lines)


def remind_followup() -> str:
    """每天 09:00 — 跟進提醒"""
    due_today = bni_db.get_due_followups("due_today")
    overdue = bni_db.get_due_followups("overdue")
    upcoming = bni_db.get_due_followups("upcoming_3d")
    # upcoming includes today + overdue, filter to only future
    upcoming_only = [f for f in upcoming
                     if f["due_date"] > date.today().isoformat()]

    total = len(due_today) + len(overdue)

    if total == 0 and not upcoming_only:
        return (
            "📋 跟進提醒 — 今日無待處理事項\n\n"
            "所有跟進都已完成，做得好！👍\n"
            "考慮新增一些潛在客戶跟進？"
        )

    lines = [
        f"📋 跟進提醒 — {date.today().isoformat()}",
        f"待處理：{total} 筆",
        "",
    ]

    if overdue:
        lines.append(f"🔴 逾期（{len(overdue)} 筆）：")
        for f in overdue:
            days_late = (date.today() - date.fromisoformat(f["due_date"])).days
            lines.append(
                f"  - {f['client_name']}：{f['reason']}（逾期 {days_late} 天）"
            )
        lines.append("")

    if due_today:
        lines.append(f"🟡 今日到期（{len(due_today)} 筆）：")
        for f in due_today:
            pri = " ❗" if f["priority"] in ("high", "urgent") else ""
            lines.append(f"  - {f['client_name']}：{f['reason']}{pri}")
        lines.append("")

    if upcoming_only:
        lines.append(f"🔵 未來 3 天（{len(upcoming_only)} 筆）：")
        for f in upcoming_only[:5]:
            lines.append(f"  - {f['due_date']} {f['client_name']}：{f['reason']}")

    lines.append("\n完成後回覆「完成 #ID」標記已處理")

    return "\n".join(lines)


# ─── Auto mode ───────────────────────────────────────────────────────────────

def auto_detect_type():
    """根據當前時間判斷應發送的提醒類型"""
    now = datetime.now()
    weekday = now.weekday()  # 0=Mon
    hour = now.hour
    minute = now.minute

    # 週二 06:00-07:00 → BNI meeting
    if weekday == 1 and 6 <= hour <= 7:
        return "bni_meeting"

    # 週五 16:30-17:30 → BNI report
    if weekday == 4 and (
        (hour == 16 and minute >= 30) or (hour == 17 and minute <= 30)
    ):
        return "bni_report"

    # 07:30-08:30 → daily checkin
    if 7 <= hour <= 8 and not (weekday == 1 and hour <= 7):
        return "daily_checkin"

    # 08:30-09:30 → followup
    if 8 <= hour <= 9:
        return "followup"

    return None


def main():
    bni_db.init_db()

    parser = argparse.ArgumentParser(description="BNI Reminder System")
    parser.add_argument("--type",
                        choices=["bni_meeting", "bni_report",
                                 "daily_checkin", "followup"])
    parser.add_argument("--auto", action="store_true",
                        help="Auto-detect reminder type by current time")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print message without sending")
    args = parser.parse_args()

    if args.auto:
        reminder_type = auto_detect_type()
        if not reminder_type:
            print(f"[bni_reminder] auto: no reminder due at "
                  f"{datetime.now().strftime('%H:%M')} "
                  f"(weekday={datetime.now().weekday()})")
            return
    elif args.type:
        reminder_type = args.type
    else:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "bni_meeting": remind_bni_meeting,
        "bni_report": remind_bni_report,
        "daily_checkin": remind_daily_checkin,
        "followup": remind_followup,
    }

    print(f"[bni_reminder] Generating: {reminder_type}")
    msg = handlers[reminder_type]()

    if args.dry_run:
        print("--- DRY RUN ---")
        print(msg)
        print("--- END ---")
        return

    ok = send_telegram(msg)
    status = "sent" if ok else "FAILED"
    print(f"[bni_reminder] {reminder_type}: {status}")

    if not ok:
        print(f"[bni_reminder] Message was:\n{msg}")


if __name__ == "__main__":
    main()
