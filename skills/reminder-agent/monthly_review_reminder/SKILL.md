---
name: monthly_review_reminder
description: 月度回顧。當用戶說「月度回顧」「這個月表現」或 cron 排程觸發時啟動。
metadata: { "openclaw": { "emoji": "📈" } }
---

# 月度回顧

每月自動彙整 BNI 活動、業務成果與個人目標的達成狀況，產出回顧報告。

## 操作 / 工作流程
1. 用 `cron` 排程在每月最後一週觸發：
   - 每月 25 日 10:00：發送月度回顧提醒 + 數據報告
2. 用 Notion API 彙整當月數據：
   - 轉介紹統計（收到 / 給出 / 成交）
   - 一對一會議次數
   - BNI 出席率
   - 營收數據
3. 用 `memory_search` 取得月初設定的目標，計算達成率
4. 與上月數據比較，標示成長或衰退
5. 產出回顧報告，用 `message` 傳送到 Telegram
6. 引導設定下月目標

## cron 排程
```
0 10 25 * *    # 每月 25 日 10:00 — 月度回顧
```

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| month | string | current | 回顧月份：`current` / `last` / 指定 `YYYY-MM` |
| compare | bool | true | 是否與上月比較 |

## 輸出格式
```
📈 月度回顧 — {year}年{month}月

📊 BNI 數據：
- 轉介紹收到：{received} 筆 ({vs_last_month})
- 轉介紹給出：{given} 筆 ({vs_last_month})
- 成交：{closed} 筆 / ${amount}
- 一對一會議：{meetings} 次
- 出席率：{attendance_rate}%

🎯 目標達成：
| 目標 | 目標值 | 實際 | 達成率 |
|------|--------|------|--------|
| {goal} | {target} | {actual} | {rate}% |

💡 本月亮點：{highlights}
📌 待改善：{improvements}

下月目標建議：
1. {suggestion}
2. {suggestion}

回覆設定下月目標，或回覆「確認」存檔。
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| Notion 數據不完整 | 標注缺失欄位，基於可用數據產出報告 |
| 無上月數據可比較 | 跳過比較，標注「首月報告」 |
| 用戶未設定月目標 | 列出建議目標，引導用戶設定 |

## 使用範例
- "這個月的回顧報告"
- "我這個月 BNI 表現怎樣"
- "跟上個月比成長了嗎"
