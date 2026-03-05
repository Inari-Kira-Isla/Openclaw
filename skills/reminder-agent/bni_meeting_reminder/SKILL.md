---
name: bni_meeting_reminder
description: BNI 會議提醒。當用戶說「BNI 開會」「例會提醒」或 cron 排程觸發時啟動。
metadata: { "openclaw": { "emoji": "📅" } }
---

# BNI 會議提醒

自動在 BNI 例會前發送多階段提醒，包括準備事項、會議資訊與出席確認。

## 操作 / 工作流程
1. 用 `cron` 設定排程提醒（BNI 例會每週二）：
   - 當天早上（週二 06:30）：時間地點 + 準備事項 + 轉介紹統計
2. 用 SQLite 查詢 BNI 資料庫 (`~/.openclaw/memory/bni.db`)：
   - `meetings` 表：本週會議主題 / 角色
   - `referrals` 表：待跟進的轉介紹數量
   - `followups` 表：逾期跟進事項
3. 組合提醒訊息
4. 用 `message` 傳送到 Telegram
5. 腳本：`bni_reminder.py --type bni_meeting`

## cron 排程
```
30 6 * * 2    # 每週二 06:30 — BNI 會議提醒
```

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| stage | string | auto | 提醒階段：`preview` / `confirm` / `day_of` / `auto`（依排程） |
| include_referrals | bool | true | 是否附帶待跟進轉介紹 |

## 輸出格式
```
📅 BNI 例會提醒 — {stage}

日期：{date}（{weekday}）
時間：{time}
地點：{location}
本週主題：{topic}

🎤 你的角色：{role}

📋 準備事項：
- 名片（至少 20 張）
- 60 秒自我介紹
- {additional_prep}

🔄 待跟進轉介紹：{referral_count} 筆
- {referral_summary}

請回覆確認出席 ✅ / 請假 ❌
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| SQLite 查詢失敗 | 發送基本提醒（時間地點），標注「資料庫暫時無法存取」 |
| 會議取消或改期 | 偵測到異動時發送更新通知 |
| Telegram 傳送失敗 | 重試 3 次，記錄失敗日誌 |

## 使用範例
- "這週 BNI 開會要準備什麼"
- "提醒我 BNI 例會時間"
- "幫我確認這週有沒有 BNI"
