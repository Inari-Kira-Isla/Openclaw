---
name: active_thought_logger
description: 工作中動態標註。在處理任務時，即時捕捉「暫存記憶」，包括發現的規律或解決的難點。
---

# 工作中動態標註 (Active Thought Logger)

## 功能說明

在處理任務時，即時捕捉：
- 發現的規律
- 解決的難點
- 臨時洞察
- 決策理由

## 輸入

| 欄位 | 類型 | 說明 |
|------|------|------|
| task_id | string | 任務 ID |
| thought | string | 當前思考 |
| insight_type | string | 洞察類型 |

## 輸出

| 欄位 | 類型 | 說明 |
|------|------|------|
| saved_thoughts | array | 已儲存的思考 |
| metadata | object | 中繼資料 |

## 洞察類型

| 類型 | 說明 |
|------|------|
| pattern | 發現的規律 |
| solution | 解決的難點 |
| decision | 決策理由 |
| observation | 觀察記錄 |
| question | 產生的問題 |

## 工作流程

```
1. 任務進行中
   ↓
2. 捕捉臨時思考
   - 分析用戶請求
   - 識別關鍵決策點
   ↓
3. 分類洞察類型
   - pattern / solution / decision
   ↓
4. 暫存到記憶緩衝區
   - 格式：[類型] 內容
   - 添加時間戳
   ↓
5. 工作結束後
   - 傳遞給 memory_deepener
   - 進行長期儲存
```

## 範例

### 發現規律
```
[pattern] 週三的價格波動通常受物流影響
[context] 分析豐洲市場數據時發現
```

### 解決難點
```
[solution] 使用 n8n Webhook 解決本地無法被訪問的問題
[context] 設定 Facebook Messenger 整合時
```

### 決策理由
```
[decision] 選擇本地 Embedding 而非 API
[cost] $0 vs $0.01/1k tokens
[reason] 大量資料需要低成本方案
```

---

## 使用時機

- 分析數據時發現規律
- 解決技術難- 做出題
重要決策
- 觀察異常情況

---

*此技能用於工作中即時捕捉臨時記憶*
