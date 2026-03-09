---
name: knowledge_hub
description: Knowledge Hub 知識管理系統。整合 Google Sheets，提供知識查詢、新增、專案追蹤、間隔複習管理。支援 Projects / Learning / Inbox 三大模組。取代 Notion 的本地 + 雲端混合知識中樞。
---

# Knowledge Hub — 知識管理中心

## 功能說明

整合 Google Sheets 的個人知識管理系統，取代 Notion。支援：
- 知識筆記查詢與新增（分類：Tech Insight / Error Log / Tutorial / Concept / Tool / Pattern）
- 專案追蹤與進度管理
- 間隔複習提醒（艾賓浩斯記憶曲線：1天 / 7天 / 30天）
- 快速收集（Inbox）
- Google Drive 文件管理

## 系統架構

- **Google Sheets**: 3 tabs (Projects / Learning / Inbox) — 雲端資料源
- **SQLite**: `~/.openclaw/memory/knowledge_hub.db` — 本地快取
- **GAS Web App**: Bootstrap 5 前端（Tech Card 卡片流）
- **OpenClaw 整合**: 透過此技能讀寫知識庫

## 工具指引

- **knowledge_hub_db.py**: 核心 Python 模組，SQLite + Google Sheets API
- **knowledge_hub_sync.py**: 排程同步（每 30 分鐘 LaunchAgent）
- **Telegram**: 透過 OpenClaw CLI 發送複習提醒
- **Gmail**: GAS 發送每日摘要與複習郵件

## 子技能

- `query_knowledge` — 查詢知識庫
- `add_entry` — 新增條目
- `project_status` — 專案總覽
- `sync_review` — 複習管理
