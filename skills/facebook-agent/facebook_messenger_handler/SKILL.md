---
name: facebook_messenger_handler
description: Facebook Messenger 訊息處理核心。當粉絲專頁收到 Messenger 訊息時觸發，包括：訊息接收解析、分類路由、AI 回覆生成、對話記錄同步。
---

# Facebook Messenger Handler — Messenger 訊息處理

## 功能說明

作為 Facebook Messenger 自動化的核心樞紐，透過 n8n 中轉接收粉絲專頁訊息，協調分類、回覆與記錄的完整流程。

## 架構流程

```
用戶訊息 → Facebook → n8n Webhook → OpenClaw API → AI 處理 → n8n → 回覆用戶
                                                      ↓
                                               SQLite（對話記錄）
```

## 操作步驟

### 訊息接收與處理
1. n8n Webhook 接收粉絲專頁 Messenger 訊息
2. 解析用戶身份（FB ID、姓名）與訊息內容
3. 呼叫 question_classifier 進行分類
4. 依分類結果路由：
   - FAQ 類 → faq_auto_reply 處理
   - 投訴/複雜 → handoff_manager 轉人工
   - 其他 → AI 直接生成回覆
5. 回覆透過 n8n 發送回 Messenger
6. 呼叫 conversation_logger 記錄對話

### 訊息路由表

| 分類結果 | 處理方式 | 回覆來源 |
|----------|----------|----------|
| 價格/產品/服務 | FAQ 自動回覆 | faq_auto_reply |
| 訂單/投訴 | 轉接人工 | handoff_manager |
| 閒聊/其他 | AI 生成回覆 | 本技能直接處理 |

## 回覆格式

### 自動回覆
```
您好！感謝您的訊息。
[AI 生成的回覆內容]
如需更多幫助，請隨時告訴我！
```

### 轉接人工
```
您的問題已經記錄，我們的團隊將盡快與您聯繫。
預計回覆時間：30 分鐘內。
```

## 工具指引

- **n8n Workflow**：Webhook 接收 + Messenger API 發送回覆
- **SQLite（cs_customers.db）**：對話記錄存儲（透過 cs_customer_db.py）
- **question_classifier**：訊息分類
- **faq_auto_reply**：FAQ 自動回覆
- **handoff_manager**：人工轉接
- **conversation_logger**：對話記錄

### 必要環境變數
- `FACEBOOK_PAGE_ACCESS_TOKEN` — 粉絲專頁存取權杖
- `FACEBOOK_VERIFY_TOKEN` — Webhook 驗證權杖
- `OPENCLAW_API_URL` — OpenClaw API 端點
- `CS_CUSTOMER_DB` — 本地 SQLite 資料庫路徑（~/.openclaw/memory/cs_customers.db）

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| n8n Webhook 未觸發 | 檢查 Webhook URL 設定與 Facebook App 狀態 |
| Messenger API 回覆失敗 | 重試一次，若仍失敗則記錄錯誤並通知管理員 |
| AI 回覆生成逾時 | 先送出「正在處理中」訊息，稍後補發完整回覆 |
| 用戶身份解析失敗 | 以匿名身份處理，但標記需人工確認 |
| SQLite 同步失敗 | 不影響回覆流程，將記錄排入重試佇列 |

## 使用範例

- 「粉絲透過 Messenger 詢問產品資訊」→ 分類 + FAQ 回覆
- 「客戶在 FB 私訊詢價」→ 分類 + 價格模板回覆
- 「粉絲專頁收到投訴訊息」→ 分類 + 轉人工 + 記錄

## 防護規則

- 回覆內容不可包含競爭對手的負面評論
- 不可承諾具體交期或價格，除非來自官方 FAQ
- 所有對話須記錄，不可跳過 conversation_logger
- 非文字訊息（貼圖、語音）需轉人工處理，不可忽略
- 遵循 Facebook 平台政策，不發送促銷垃圾訊息
