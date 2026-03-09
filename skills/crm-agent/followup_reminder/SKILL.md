---
name: followup_reminder
description: 客戶跟進提醒系統。當需要設定、查詢或管理客戶跟進提醒時觸發，包括：跟進時間設定、提醒發送、逾期追蹤、建議跟進動作。
---

# Followup Reminder — 跟進提醒

## 功能說明

確保每位需要跟進的客戶都不被遺忘。自動在指定時間發送提醒，附上客戶摘要與建議動作，提升客戶維護效率。

## 提醒優先級

| 等級 | 觸發條件 | 提醒方式 |
|------|----------|----------|
| P0 | 重要客戶逾期未跟進 | Telegram 即時通知 + SQLite 待辦記錄 |
| P1 | 一般客戶到期提醒 | Telegram 每日摘要 |
| P2 | 低優先客戶 | 僅 SQLite 待辦記錄 |

## 操作步驟

### 設定提醒
1. 確認客戶名稱與跟進事項
2. 設定提醒日期與時間
3. 附上建議動作（選填）
4. 透過 `cs_customer_db.py` 寫入 SQLite `conversations` 表格（intent 標記為 `followup`）
5. 同步至排程系統（cron）

### 觸發提醒
1. 排程系統到時觸發
2. 透過 `cs_customer_db.py` 的 `get_customer_history()` 查詢該客戶最新互動記錄
3. 組合提醒訊息：客戶資訊 + 跟進事項 + 上次互動摘要
4. 依優先級選擇通知管道發送

### 逾期處理
1. 每日掃描 SQLite `conversations` 表格中已逾期未完成的跟進
2. 自動升級優先級（P2→P1→P0）
3. 連續逾期 3 天的提醒標記為「需關注」

## 提醒訊息格式

```
跟進提醒
客戶：[姓名]（[公司]）
事項：[跟進事項]
上次互動：[日期] — [摘要]
建議動作：
1. [動作 1]
2. [動作 2]
優先級：P1
```

## 工具指引

- **cs_customer_db.py**：提醒記錄與客戶資料查詢（SQLite `cs_customers.db`）
  - `log_conversation(customer_id, brand_id, channel, message, intent, sentiment, agent_reply)` — 寫入跟進記錄（intent=`followup`）
  - `get_customer_history(customer_id, limit)` — 取得最新互動摘要
  - `get_vip_candidates(brand_id, ...)` — 識別高優先客戶
- **Telegram Bot**：發送提醒通知
- **Cron 排程**：定時觸發提醒
- **interaction_tracker**：取得最新互動資訊

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| 客戶不存在 | 提示先建立客戶資料 |
| 提醒時間已過 | 立即發送，並提示設定時間已過期 |
| Telegram 發送失敗 | 寫入 SQLite 待辦記錄（intent=`followup_failed`），下次摘要時補發 |
| 重複提醒 | 提示已有相同提醒，詢問是否更新或新增 |

## 使用範例

- 「提醒我下週三跟進 ABC 公司的報價」
- 「有哪些客戶的跟進已經逾期了？」
- 「取消對李小明的跟進提醒」

## 防護規則

- 不可在非工作時間（22:00-08:00）發送 P1/P2 提醒
- P0 提醒不受時間限制，可即時發送
- 已完成的提醒需標記「已完成」，不可刪除
- 不可代替使用者自動完成跟進動作，僅負責提醒
