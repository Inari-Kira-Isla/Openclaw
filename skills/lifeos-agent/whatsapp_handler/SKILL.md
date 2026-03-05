---
name: whatsapp_handler
description: WhatsApp 處理。當需要透過 n8n 接收、分類、回覆 WhatsApp 訊息時觸發，包括：訊息接收解析、自動分類、AI 回覆生成、對話記錄同步。
---

# WhatsApp Handler

## 功能說明

透過 n8n 工作流中轉 WhatsApp 訊息，由 OpenClaw AI 進行分類與回覆處理。支援自動回覆常見問題、人工轉接、對話歷史記錄至本地資料庫（SQLite）。

## 架構流程

```
WhatsApp 訊息 -> n8n Webhook -> OpenClaw API -> AI 處理 -> n8n -> WhatsApp 回覆
```

## 執行步驟

### 1. 訊息接收與解析

- 從 n8n Webhook 接收 WhatsApp 訊息
- 解析發訊者身份（電話、姓名）
- 提取訊息文字內容

### 2. 訊息分類

根據內容自動分類並決定處理方式：

| 類別 | 處理方式 |
|------|----------|
| 問答類（FAQ） | AI 自動回覆 |
| 訂單相關 | 記錄後轉接人工 |
| 投訴/抱怨 | 安撫回覆後轉接人工 |
| 未知/其他 | AI 嘗試回覆 |

### 3. 回覆生成

- 依分類結果生成對應回覆
- 自動回覆格式：保持友善、專業、簡潔
- 轉接人工時告知用戶等待

### 4. 對話記錄

- 將對話內容同步至本地資料庫（SQLite: cs_customers.db）
- 建立或更新客戶檔案
- 記錄互動時間、分類、處理結果

## 整合方式

| 方案 | 說明 | 適用情境 |
|------|------|----------|
| Twilio | 較簡單，使用 Twilio WhatsApp Sandbox | 測試階段 |
| WhatsApp Business API | 需 Facebook 企業認證 | 正式上線 |

## 必要環境變數

```
WHATSAPP_PHONE_NUMBER_ID=xxx
WHATSAPP_ACCESS_TOKEN=xxx
OPENCLAW_API_URL=http://localhost:8080
# NOTION_API_KEY — 已棄用，改用 SQLite 本地方案
```

## 工具指令

- **n8n Workflow**：訊息收發中轉（Webhook + HTTP Request + WhatsApp 節點）
- **SQLite（cs_customers.db）**：客戶檔案與對話記錄 CRUD（透過 cs_customer_db.py）
- **OpenClaw API**：AI 回覆生成

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| n8n Webhook 無回應 | 記錄失敗事件，不回覆（避免重複） |
| AI 回覆生成失敗 | 回傳預設訊息「感謝您的訊息，我們會盡快回覆」 |
| SQLite 同步失敗 | 先回覆用戶，背景重試記錄同步（最多 3 次） |
| WhatsApp API 限流 | 等待後重試，記錄受影響的訊息 |
| 訊息含不支援格式（語音/影片） | 回覆「目前僅支援文字訊息，請以文字描述您的需求」 |

## 使用範例

- 客戶透過 WhatsApp 詢問「你們有什麼產品？」-> FAQ 自動回覆
- 客戶傳「我要退貨」-> 記錄後轉接人工
- 國外客戶用英文諮詢 -> AI 以對應語言回覆

## 安全邊界

- 不主動發送訊息給用戶，僅回覆收到的訊息
- 不處理付款或敏感個資（信用卡號等），一律轉人工
- 回覆內容不得包含未經確認的價格或承諾
- 對話記錄僅存於本地資料庫（SQLite），不額外備份至其他平台
- 若無法判斷訊息意圖，預設轉接人工而非猜測回覆
