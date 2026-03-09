---
name: daily_checkin_reminder
description: 每日簽到提醒。當用戶說「每日簽到」「今日重點」或 cron 排程觸發時啟動。
metadata: { "openclaw": { "emoji": "🌅" } }
---

# 每日簽到提醒

每天早上發送簽到提醒，彙整今日行程、待辦事項與重點任務，幫助規劃一天。

## 操作 / 工作流程
1. 用 `cron` 排程每天早上自動觸發：
   - 每天 08:00：發送每日簽到
2. 用 SQLite 收集今日資訊 (`~/.openclaw/memory/bni.db`)：
   - `followups` 表：今日到期的跟進事項
   - `checkin_log` 表：簽到連續天數
   - `meetings` 表：下次 BNI 會議日期
3. 用 `memory_search` 查詢：
   - 昨日未完成事項
   - 近期目標進度
4. 組合每日簽到訊息
5. 用 `message` 傳送到 Telegram
6. 等待用戶回覆確認簽到，記錄到 `checkin_log`
7. 腳本：`bni_reminder.py --type daily_checkin`

## cron 排程
```
0 8 * * *    # 每天 08:00 — 每日簽到
```

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| include_calendar | bool | true | 是否包含行事曆 |
| include_todos | bool | true | 是否包含待辦事項 |
| include_followups | bool | true | 是否包含跟進提醒 |

## 輸出格式
```
🌅 早安！每日簽到 — {date}（{weekday}）

📅 今日行程：
- {time}: {event}

✅ 今日待辦：
- [ ] {task_1}
- [ ] {task_2}
- [ ] {carry_over_task}（昨日未完成）

🔔 需跟進：{followup_count} 筆
- {followup_summary}

🎯 本週目標進度：{progress}

回覆「簽到」開始今天的工作！
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| SQLite 無回應 | 發送簡化版簽到（僅問候 + 昨日記憶），標注數據源異常 |
| 無任何待辦/行程 | 發送「今天行程清爽」+ 建議主動安排事項 |
| 用戶連續 3 天未簽到 | 發送關心訊息，詢問是否要調整提醒時間 |

## 使用範例
- "今天有什麼要做的"
- "早安簽到"
- "幫我看今天的行程"
