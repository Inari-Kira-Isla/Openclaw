---
name: active_thought_logger
description: 即時思維記錄。在處理任務時自動捕捉洞察、規律與決策理由。
metadata: { "openclaw": { "emoji": "💭" } }
---

# 即時思維記錄

任務進行中即時捕捉暫存思維，包括發現的規律、解決的難點、決策理由與觀察。

## 操作 / 工作流程

1. **監聽任務上下文** — 在任務執行過程中持續觀察
2. **識別可記錄洞察** — LLM 判斷是否出現值得記錄的思維：
   - `pattern`：發現的規律
   - `solution`：解決的難點
   - `decision`：重要決策與理由
   - `observation`：異常觀察
   - `question`：產生的待解問題
3. **格式化暫存** — 以結構化格式暫存到記憶緩衝區：
   ```
   [類型] 內容
   [context] 發生場景
   [timestamp] 時間戳
   ```
4. **任務結束** — 將暫存思維傳遞給 `memory_deepener` 進行長期儲存
5. **清理緩衝區** — 確認移交後清除暫存

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| task_id | string | 自動生成 | 關聯的任務 ID |
| thought | string | 必填 | 當前思考內容 |
| insight_type | string | "observation" | 洞察類型：pattern/solution/decision/observation/question |
| context | string | "" | 觸發場景描述 |

## 輸出格式

```
💭 思維已記錄
- 類型：{insight_type}
- 內容：{thought}
- 任務：{task_id}
- 緩衝區暫存數：{buffer_count}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 緩衝區滿（> 50 筆） | 自動觸發 memory_deepener 批次處理 |
| 重複洞察 | 合併同類洞察，更新時間戳 |
| 任務 ID 遺失 | 使用時間戳生成臨時 ID |
| memory_deepener 不可用 | 暫存保留，下次可用時補送 |

## 使用範例

- "記一下：週三的價格波動通常受物流影響"
- "這次用 n8n Webhook 解決了本地無法被訪問的問題"
- "決策記錄：選擇本地 Embedding，因為成本更低"
