#!/usr/bin/env python3
"""
site_daily_report.py
每天晚上 10 點生成詳細網站報告並發送到 Telegram。
"""

import os, sqlite3, subprocess, requests
from datetime import datetime, date, timedelta

OC_GATEWAY  = "http://127.0.0.1:18789"
OC_TOKEN    = "4267bd714b23adeba00e1e99ad60c066f29006cc5e84a15e"
TG_CHAT_ID  = "8399476482"
DB_PATH     = os.path.expanduser("~/.openclaw/memory/site_articles.db")
BASE_URL    = "https://inari-kira-isla.github.io/Openclaw"
REPO_DIR    = os.path.expanduser("~/Documents/Openclaw")

CAT_ICONS = {
    "prompts":   "💡",
    "configs":   "⚙️",
    "tutorials": "📚",
    "workflows": "🔄",
    "articles":  "📰",
}

def send_telegram(msg: str):
    try:
        import subprocess
        result = subprocess.run(
            ["/usr/local/bin/openclaw", "message", "send",
             "--channel", "telegram", "--account", "kira",
             "--target", TG_CHAT_ID, "--message", msg],
            capture_output=True, timeout=25
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[report] Telegram error: {e}")
        return False

def get_db():
    if not os.path.exists(DB_PATH):
        return None
    return sqlite3.connect(DB_PATH)

def get_today_articles(con):
    today = str(date.today())
    rows = con.execute(
        "SELECT category, title, url, published_at FROM articles WHERE date=? ORDER BY published_at",
        (today,)
    ).fetchall()
    return rows

def get_week_stats(con):
    week_ago = str(date.today() - timedelta(days=7))
    rows = con.execute(
        "SELECT date, COUNT(*) as cnt FROM articles WHERE date >= ? GROUP BY date ORDER BY date DESC LIMIT 7",
        (week_ago,)
    ).fetchall()
    return rows

def get_total_stats(con):
    total = con.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    by_cat = con.execute(
        "SELECT category, COUNT(*) as cnt FROM articles GROUP BY category ORDER BY cnt DESC"
    ).fetchall()
    return total, by_cat

def get_github_pages_status():
    try:
        result = subprocess.run(
            ["gh", "run", "list", "--repo", "Inari-Kira-Isla/Openclaw",
             "--limit", "1", "--json", "status,conclusion,createdAt"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            import json
            runs = json.loads(result.stdout)
            if runs:
                r = runs[0]
                status = r.get("conclusion") or r.get("status", "unknown")
                return "✅ 部署成功" if status == "success" else f"⚠️ {status}"
    except Exception:
        pass
    return "🔄 狀態未知"

def get_site_file_count():
    count = 0
    for root, dirs, files in os.walk(REPO_DIR):
        dirs[:] = [d for d in dirs if d not in [".git", ".github", "docs", "api"]]
        count += sum(1 for f in files if f.endswith(".html") and f != "ai-footprint.html")
    return count

def format_report(today_articles, week_stats, total, by_cat, gh_status, file_count):
    today_str  = date.today().strftime("%Y年%m月%d日")
    now_str    = datetime.now().strftime("%H:%M")
    today_count = len(today_articles)

    # 今日文章列表
    today_lines = ""
    if today_articles:
        cat_groups = {}
        for cat, title, url, published_at in today_articles:
            cat_groups.setdefault(cat, []).append((title, url))
        for cat, arts in cat_groups.items():
            icon = CAT_ICONS.get(cat, "📄")
            today_lines += f"\n{icon} {cat.upper()}\n"
            for title, url in arts:
                short = title[:35] + "…" if len(title) > 35 else title
                today_lines += f"  · {short}\n"
    else:
        today_lines = "\n  （今日尚未發布文章）\n"

    # 本週趨勢
    week_lines = ""
    for d, cnt in week_stats:
        bar = "█" * min(cnt, 15) + "░" * max(0, 15 - cnt)
        week_lines += f"  {d}  {bar} {cnt}\n"

    # 分類統計
    cat_lines = ""
    for cat, cnt in by_cat:
        icon = CAT_ICONS.get(cat, "📄")
        cat_lines += f"  {icon} {cat}: {cnt} 篇\n"

    report = f"""📊 AI 學習寶庫 每日報告
📅 {today_str}  ⏰ {now_str}
━━━━━━━━━━━━━━━━━━━━━

📝 今日發布：{today_count} 篇
{today_lines}
━━━━━━━━━━━━━━━━━━━━━

📈 本週發布趨勢：
{week_lines}
━━━━━━━━━━━━━━━━━━━━━

📚 累計數據：
  總文章數：{total} 篇
  網站頁面：{file_count} 個
{cat_lines}
━━━━━━━━━━━━━━━━━━━━━

🌐 部署狀態：{gh_status}
🔗 {BASE_URL}

#每日報告 #AI學習寶庫"""

    return report

def main():
    print(f"[site_daily_report] 生成報告 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    con = get_db()
    if con is None:
        send_telegram("⚠️ AI 學習寶庫報告：資料庫尚未建立，請確認文章生成器已運行。")
        return

    today_articles = get_today_articles(con)
    week_stats     = get_week_stats(con)
    total, by_cat  = get_total_stats(con)
    con.close()

    gh_status  = get_github_pages_status()
    file_count = get_site_file_count()

    report = format_report(today_articles, week_stats, total, by_cat, gh_status, file_count)
    print(report)

    ok = send_telegram(report)
    print(f"[site_daily_report] Telegram {'✅ 發送成功' if ok else '❌ 發送失敗'}")

if __name__ == "__main__":
    main()
