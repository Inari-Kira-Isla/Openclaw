# Gmail 郵件整理自動化

**用途**: 郵件標籤化/分類
**目標**: 自動將郵件分類到不同標籤

---

## 自動化流程

```
新郵件進入
    ↓
n8n Gmail Trigger
    ↓
AI 分析郵件內容
    ↓
自動標籤/分類
    ↓
移動到相應標籤
```

---

## 建議標籤分類

| 標籤 | 條件 |
|------|------|
| 🛒 訂單 | 含 order, purchase, 訂單 |
| 💰 帳單 | 含 invoice, 發票, 帳單 |
| 📢 推銷 | 含 promotion, sale, 優惠 |
| ✅ 待處理 | 需要回覆的郵件 |
| 📎 附件 | 有附件的郵件 |

---

## n8n 節點

1. **Gmail Trigger** - 監控 INBOX
2. **IF** - 根據條件分類
3. **Gmail** - 添加標籤/移動郵件

---

## 需要設定

1. Google Cloud 專案 + Gmail API
2. OAuth 2.0 憑證
3. n8n Gmail credentials

---

要我幫你設定嗎？
