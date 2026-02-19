---
name: whatsapp_handler
description: WhatsApp 處理。當需要處理 WhatsApp 訊息時觸發，包括：訊息接收、分類、回覆、記錄。
---

# WhatsApp Handler

## 概述

透過 n8n 中轉處理 WhatsApp 訊息，統一由 OpenClaw AI 大腦處理回覆。

## 架構

```
WhatsApp → n8n Webhook → OpenClaw API → AI 處理 → 回覆 → n8n → WhatsApp
```

## 功能

### 1. 訊息接收
- 接收 WhatsApp 訊息
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

- 「客戶透過 WhatsApp 詢問產品資訊」
- 「顧客在 WhatsApp 私訊詢價」
- 「國外客戶諮詢」

## 必要設定

### n8n Workflow 節點

1. **WhatsApp Webhook** - 接收訊息
2. **HTTP Request** - 發送至 OpenClaw
3. **OpenAI/LLM** - 生成回覆 (可選)
4. **WhatsApp** - 發送回覆

### 環境變數

```
WHATSAPP_PHONE_NUMBER_ID=xxx
WHATSAPP_ACCESS_TOKEN=xxx
OPENCLAW_API_URL=http://localhost:8080
NOTION_API_KEY=xxx
```

## 整合方式

### 選項 A: Twilio (較簡單)
- 註冊 Twilio 帳號
- 申請 WhatsApp Sandbox
- 在 n8n 使用 Twilio 節點

### 選項 B: WhatsApp Business API
- 需要 Facebook 企業認證
- 申請 WhatsApp Business API
- 在 n8n 使用 HTTP Request 節點

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
```

---

*此 SKILL 配合 workflow-orchestrator 使用*
