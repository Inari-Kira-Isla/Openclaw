---
name: facebook_messenger_handler
description: Facebook Messenger 處理。當需要處理 Facebook Messenger 訊息時觸發，包括：訊息接收、分類、回覆、記錄。
---

# Facebook Messenger Handler

## 概述

透過 n8n 中轉處理 Facebook Messenger 訊息，統一由 OpenClaw AI 大腦處理回覆。

## 架構

```
Facebook Messenger → n8n Webhook → OpenClaw API → AI 處理 → 回覆 → n8n → Messenger
```

## 功能

### 1. 訊息接收
- 接收粉絲專頁 Messenger 訊息
- 解析用戶身份與訊息內容
- 轉發給 OpenClaw 處理

### 2. 訊息分類
- 問答類 → FAQ Auto Reply
- 訂單類 → 轉接人工
- 抱怨類 → 轉接人工
- 未知類 → AI 回覆

### 3. 回覆處理
- AI 生成回覆
- 統一回覆格式
- 記錄對話歷史

### 4. 對話記錄
- 同步到 Notion
- 建立客戶檔案
- 追蹤互動歷史

## 使用情境

- 「粉絲透過 Messenger 詢問產品資訊」
- 「客戶在 FB 私訊詢價」
- 「粉絲專頁收到投訴訊息」

## 必要設定

### n8n Workflow 節點

1. **Facebook Webhook** - 接收訊息
2. **HTTP Request** - 發送至 OpenClaw
3. **OpenAI/LLM** - 生成回覆 (可選)
4. **Facebook Messenger** - 發送回覆

### 環境變數

```
FACEBOOK_PAGE_ACCESS_TOKEN=xxx
FACEBOOK_VERIFY_TOKEN=xxx
OPENCLAW_API_URL=http://localhost:8080
NOTION_API_KEY=xxx
```

## 對話流程

```
1. 用戶發送訊息到粉絲專頁
2. n8n 接收 Webhook 觸發
3. 解析訊息並記錄到 Notion
4. 發送至 OpenClaw API
5. AI 生成回覆
6. 回覆透過 n8n 發送回 Messenger
7. 對話記錄同步到 Notion
```

## 回覆格式

### 自動回覆
```
👋 您好！感謝您的訊息。

[AI 生成的回覆內容]

💡 如需更多幫助，請告訴我！
```

### 轉接人工
```
📋 您的問題已經記錄。

我們的團隊將盡快與您聯繫。
預計等待時間：X 分鐘
```

## 常見問題處理

| 問題類型 | 處理方式 |
|----------|----------|
| 產品詢問 | AI 回覆 + 產品資訊 |
| 價格諮詢 | AI 回覆 + 轉人工 |
| 訂單問題 | 轉接人工客服 |
| 抱怨投訴 | 轉接人工 + 標記優先 |
| 陌生訊息 | AI 初步回覆 + 分類 |

## 整合檢查清單

- [ ] Facebook 開發者帳號
- [ ] 粉絲專頁
- [ ] Meta App 建立
- [ ] Messenger 產品啟用
- [ ] Page Access Token 取得
- [ ] n8n Workflow 完成
- [ ] Webhook 設定
- [ ] Notion 對話資料庫

## 參考資源

- Facebook Messenger API: https://developers.facebook.com/docs/messenger-platform
- n8n Facebook 節點: https://docs.n8n.io/integrations/builtin/app-nodes/n8n.nodes.facebookTrigger/
