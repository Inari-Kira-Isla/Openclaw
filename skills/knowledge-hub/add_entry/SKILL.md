---
name: add_entry
description: 新增知識條目。將新的技術筆記、錯誤日誌、學習心得寫入 Knowledge Hub（Learning 或 Inbox 分頁）。
---

# Add Entry — 新增知識條目

## 操作步驟

1. 收集標題、分類、內容
2. 可選：關聯專案（ProjectId）、投入時數、來源 URL、標籤
3. 用 `knowledge_hub_db.add_learning()` 寫入 SQLite
4. 觸發 `push_to_sheets('Learning')` 同步到 Google Sheets
5. 回覆確認 + 首次複習日期設定為明天

## 分類選項

- Tech Insight — 技術洞察
- Error Log — 錯誤日誌
- Tutorial — 教學筆記
- Concept — 概念理解
- Tool — 工具使用
- Pattern — 設計模式

## 工具指引

- **knowledge_hub_db.py**
  - `add_learning(title, category, content, **kwargs)` — 新增學習條目
  - `add_inbox(content, source, **kwargs)` — 新增快速收集項
  - `push_to_sheets(tab_name)` — 同步到 Google Sheets

## 使用範例

- 「記錄：學會了 GAS Web App 部署，花了 2 小時」
- 「新增錯誤日誌：Python gspread 認證問題解法」
- 「快速記一下：CloudPipe 需要加 rate limiting」

## 防護規則

- 標題不可為空
- 分類必須在 6 個選項之內
- 時數不可為負數
