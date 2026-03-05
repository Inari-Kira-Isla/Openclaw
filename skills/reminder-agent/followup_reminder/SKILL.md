---
name: followup_reminder
description: 跟進提醒。當用戶說「提醒我跟進」「follow up」或 cron 排程觸發時啟動。
metadata: { "openclaw": { "emoji": "🔔" } }
---

# 跟進提醒

追蹤需要跟進的客戶、轉介紹與待辦事項，在設定時間自動提醒並建議行動。

## 操作 / 工作流程
1. 用 `cron` 每日檢查到期的跟進項目：
   - 每天 09:00：掃描當天到期的跟進事項
2. 用 SQLite 查詢跟進資料庫 (`~/.openclaw/memory/bni.db`)：
   - `bni_db.get_due_followups('due_today')` + `get_due_followups('overdue')`
   - 取得客戶名稱、到期日、原因、優先級
3. 依優先級排序（過期天數越多越優先）
4. 用 `message` 傳送跟進清單到 Telegram
5. 用戶完成跟進後，透過 `bni_db.mark_followup_done()` 更新狀態
6. 新增跟進：`bni_db.add_followup(client, reason, date)`
7. 腳本：`bni_reminder.py --type followup`

## cron 排程
```
0 9 * * *    # 每天 09:00 — 掃描到期跟進
```

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| scope | string | due_today | 範圍：`due_today` / `overdue` / `this_week` / `all` |
| add | string | — | 新增跟進：格式 `客戶名,原因,日期` |

## 輸出格式
```
🔔 跟進提醒 — {date}

今日需跟進：{count} 筆

| 客戶 | 上次聯繫 | 原因 | 逾期 |
|------|----------|------|------|
| {name} | {last_contact} | {reason} | {overdue_days}天 |

建議動作：
1. {name} — {suggested_action}
2. {name} — {suggested_action}

回覆「完成 {name}」標記已跟進
回覆「延後 {name} {days}天」延後跟進
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| SQLite 查詢失敗 | 用 `memory_search` 查詢快取的跟進清單 |
| 無到期跟進項目 | 發送「今日無需跟進」+ 本週預覽 |
| 新增格式錯誤 | 回覆格式範例，請用戶重新輸入 |

## 使用範例
- "今天有什麼需要跟進的"
- "提醒我三天後跟進王先生"
- "這週還有哪些人要聯繫"
