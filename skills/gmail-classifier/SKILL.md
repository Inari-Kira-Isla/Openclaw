---
name: gmail_classifier
description: Gmail 郵件智能分類。當收到郵件分類任務時自動觸發，包括：垃圾郵件識別、重要郵件標記、分類學習優化。
---

# Gmail 郵件分類

## 功能說明

分析 Gmail 郵件的主題和摘要，自動判定分類（spam / important / normal），並根據用戶反饋持續優化分類準確率。

## 工作流程

### 第一步：接收郵件資訊
- 接收郵件主題（subject）和摘要（snippet）
- 格式為 JSON：`{"task": "classify_email", "email_subject": "...", "email_snippet": "..."}`

### 第二步：內容分析
- 分析郵件語意、關鍵字、發件人模式
- 比對已知分類規則

### 第三步：判定分類

| 分類 | 條件 |
|------|------|
| spam | 廣告、推銷、詐騙、賭博、釣魚連結 |
| important | 工作、會議、家人、帳單、訂單、系統通知 |
| normal | 一般郵件、社交、新聞、電子報 |

### 第四步：輸出結果
```json
{
  "category": "spam|important|normal",
  "reason": "分類原因說明"
}
```

### 第五步：學習優化
- 記錄每次分類結果及用戶反饋
- 調整分類權重和規則
- 每週生成分類準確率報告

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| 郵件內容為空 | 標記為 normal，附註「內容不足以判斷」 |
| 無法判定分類 | 標記為 normal，建議用戶手動確認 |
| 多語言混合郵件 | 根據主要語言判斷，不因語言混用而誤判 |
| 用戶反饋分類錯誤 | 記錄錯誤模式，更新分類規則 |
| JSON 格式錯誤 | 回傳錯誤提示，附上正確格式範例 |

## 使用範例

- 輸入：`{"task": "classify_email", "email_subject": "您的訂單已發貨", "email_snippet": "親愛的客戶，您的訂單 #12345 已於今天發貨..."}`
  回覆：`{"category": "important", "reason": "訂單確認郵件，對用戶有價值"}`

- 輸入：`{"task": "classify_email", "email_subject": "限時優惠！50% OFF", "email_snippet": "點擊立即購買，僅限今天..."}`
  回覆：`{"category": "spam", "reason": "典型促銷廣告郵件"}`

- 輸入：`{"task": "classify_email", "email_subject": "週末聚會", "email_snippet": "嗨，這週六要不要一起吃飯..."}`
  回覆：`{"category": "normal", "reason": "朋友社交邀約"}`

## 護欄

- 不讀取完整郵件內容，僅分析主題和摘要
- 不自動刪除任何郵件，僅做分類建議
- 不儲存郵件原文內容，僅保留分類紀錄
- 對於無法確定的郵件，寧可標為 normal 也不誤標 spam
- 分類結果僅供參考，重要郵件建議用戶自行確認
