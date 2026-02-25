# Pi for Excel 研究

**日期**: 2026-02-19
**主題**: Excel AI 插件研究

---

## 概述

Pi for Excel 是一個開源的 AI 助手插件，專為 Microsoft Excel 設計。

---

## 功能

### 核心工具 (16個)
| 工具 | 功能 |
|------|------|
| get_workbook_overview | 結構藍圖 |
| read_range | 讀取儲存格 |
| write_cells | 寫入值/公式 |
| fill_formula | 自動填入公式 |
| search_workbook | 搜尋工作簿 |
| modify_structure | 結構修改 |
| format_cells | 格式化 |
| conditional_format | 條件格式化 |
| explain_formula | 公式解釋 |
| ... | ... |

---

## 支援的模型

| 模型 | 類型 | 連接方式 |
|------|------|----------|
| Claude | 雲端 | API Key / OAuth |
| OpenAI | 雲端 | API Key |
| Gemini | 雲端 | API Key |
| GitHub Copilot | 雲端 | OAuth |

> **結論**: 主要使用雲端模型

---

## 實驗性功能

| 功能 | 說明 |
|------|------|
| Tmux bridge | 本地終端控制 |
| Python bridge | 本地運行 Python |
| MCP Gateway | 連接本地 MCP |

---

## 對比

| 功能 | Pi for Excel | OpenClaw |
|------|--------------|-----------|
| 雲端模型 | ✅ | ✅ |
| 本地模型 | ⚠️ 實驗 | ✅ 主要 |
| MCP 支援 | ✅ | ✅ |

---

## 啟示

1. 多模型抽象層是趨勢
2. 雲端為主，本地為輔
3. Excel 自動化需求大

---

## 參考

- GitHub: tmustier/pi-for-excel

---
