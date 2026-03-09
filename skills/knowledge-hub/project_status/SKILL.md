---
name: project_status
description: 專案狀態總覽。查看所有專案的進度、優先級、截止日、累計學習時數。
---

# Project Status — 專案總覽

## 操作步驟

1. 用 `knowledge_hub_db.get_project_summary()` 取得全部專案
2. 以表格格式回覆（名稱、狀態、進度%、截止日、學習時數）
3. 標記逾期專案

## 工具指引

- **knowledge_hub_db.py**
  - `query_projects(status, priority)` — 篩選專案
  - `get_project_summary()` — 總覽統計
  - `sync_learning_hours()` — 同步學習時數
  - `add_project(name, **kwargs)` — 新增專案

## 使用範例

- 「專案總覽」
- 「哪些專案快到期了」
- 「CloudPipe 專案進度多少」
- 「新增專案：Knowledge Hub 建置」
