---
name: interaction_tracker
description: 客戶互動記錄追蹤。當需要記錄、查詢或統計與客戶的互動歷史時觸發，包括：互動記錄新增、時間線檢視、互動類型統計、跟進備註。
---

# Interaction Tracker — 互動追蹤

## 功能說明

記錄與客戶的每一次互動（電話、會議、訊息、Email），建立完整時間線，作為客戶關係管理與價值評估的基礎數據。

## 互動類型

| 類型 | 圖示 | 記錄重點 |
|------|------|----------|
| 電話 | TEL | 通話時長、討論主題、結論 |
| Email | MAIL | 主旨、關鍵內容摘要 |
| 會議 | MTG | 地點、參與者、會議結論 |
| 訊息 | MSG | 平台（Telegram/LINE/Messenger）、內容摘要 |
| 其他 | OTHER | 活動巧遇、社群互動等 |

## 操作步驟

### 新增互動記錄
1. 確認客戶身份（姓名或公司）
2. 選擇互動類型
3. 記錄日期、內容摘要、結論
4. 設定下次跟進日期（選填）
5. 透過 `cs_customer_db.py` 的 `log_conversation()` 寫入 SQLite `conversations` 表格

### 查詢互動歷史
1. 接收查詢條件（客戶、時間、類型）
2. 透過 `cs_customer_db.py` 的 `get_customer_history()` 從 SQLite 拉取符合記錄
3. 以時間線格式輸出

### 統計互動數據
1. 指定客戶或時間範圍
2. 透過 `cs_customer_db.py` 的 `get_weekly_stats()` 計算互動次數、類型分布
3. 輸出統計摘要

## 記錄格式

```
互動記錄：
客戶：[名稱]
類型：電話
日期：2024-01-15
內容：討論網站改版報價細節，客戶偏好方案 B
結論：將於週五前提交正式報價
下次跟進：2024-01-20
```

## 工具指引

- **cs_customer_db.py**：互動記錄 CRUD（SQLite `cs_customers.db` `conversations` 表格）
  - `log_conversation(customer_id, brand_id, channel, message, intent, sentiment, agent_reply)` — 新增互動記錄
  - `get_customer_history(customer_id, limit)` — 查詢客戶互動時間線
  - `get_weekly_stats(brand_id)` — 取得週統計（互動次數、類型分布）
  - `get_top_intents(brand_id, limit)` — 取得最常見意圖分布
- **contact_management**：客戶基本資料查詢
- **followup_reminder**：設定跟進提醒

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| 客戶不存在 | 建議先用 contact_management 新增客戶 |
| 缺少必要資訊 | 詢問客戶名稱、互動類型與內容 |
| 重複記錄 | 提示相同日期已有記錄，詢問是否合併或新增 |
| SQLite 寫入失敗 | 確認 `cs_customers.db` 路徑與權限，暫存於對話中稍後重試 |

## 使用範例

- 「記錄一下今天跟王總通了電話，討論合作案」
- 「列出上個月跟 ABC 公司的所有互動」
- 「我這個月跟幾個客戶有過互動？」

## 防護規則

- 互動記錄一旦建立不可刪除，僅可補充修正
- 內容摘要不可包含第三方的敏感資訊
- 查詢他人的客戶互動記錄需有權限
- 不可批次修改歷史互動記錄的日期或內容
