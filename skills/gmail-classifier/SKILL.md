# Gmail 郵件分類 Skill

## 觸發條件

收到分類任務時自動觸發

## 輸入格式

```json
{
  "task": "classify_email",
  "email_subject": "郵件主題",
  "email_snippet": "郵件摘要"
}
```

## 分類邏輯

分析郵件內容，回覆以下分類：

| 分類 | 條件 |
|------|------|
| **spam** | 廣告、推銷、詐騙、赌博 |
| **important** | 工作、會議、家人、帳單、訂單 |
| **normal** | 一般郵件、社交、新聞 |

## 回覆格式

```json
{
  "category": "spam|important|normal",
  "reason": "分類原因"
}
```

## 學習優化

每次分類後記住用戶的反饋，持續優化分類準確率。

---

## 示例

### 輸入
```
Subject: 您的訂單已發貨
Snippet: 親愛的客戶，您的訂單 #12345 已於今天發貨...
```

### 回覆
```json
{
  "category": "important",
  "reason": "訂單確認郵件，對用戶有價值"
}
```

---

## 持續學習

- 記住成功分類的模式
- 根據用戶反饋調整
- 每週生成分類報告
