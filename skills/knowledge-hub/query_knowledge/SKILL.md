---
name: query_knowledge
description: 查詢知識庫。搜尋 Learning 分頁中的技術筆記、錯誤日誌、學習心得。支援依分類、標籤、專案、關鍵字搜尋。
---

# Query Knowledge — 知識查詢

## 操作步驟

1. 接收查詢條件（關鍵字、分類、標籤、專案ID）
2. 用 `knowledge_hub_db.query_learning()` 查詢 SQLite
3. 若本地無結果，先 `pull_from_sheets()` 同步再查
4. 以卡片格式回覆

## 工具指引

- **knowledge_hub_db.py** (`~/.openclaw/workspace/scripts/`)
  - `query_learning(query, category, tags, project_id, limit)` — 主查詢函式
  - `search(query, limit)` — 全文搜尋（跨 Projects + Learning + Inbox）
  - `pull_from_sheets()` — 強制同步最新資料

## 使用範例

- 「查一下 Docker 相關的筆記」
- 「列出所有 Error Log 分類的項目」
- 「CloudPipe 專案學了什麼」
- 「搜尋 gspread 相關知識」

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| 查無結果 | 建議放寬條件或換關鍵字 |
| SQLite 無資料 | 先執行 pull_from_sheets() 同步 |
| Google Sheets 連線失敗 | 使用本地 SQLite 快取資料 |
