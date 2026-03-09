# 範例文章 - 高質量標準

---

title: "Claude Code 完整教學"
type: system_prompt
date: 2026-03-02
tags: ["AI", "Claude", "教學", "開發"]
description: "從零開始學習 Claude Code 的完整教學指南，包含安裝、設定、實作範例。"
keywords: ["Claude Code", "AI 程式碼助手", "開發工具"]

---

# Claude Code 完整教學

## 概述

本文詳細介紹 Claude Code 的安裝、配置和使用方法，幫助開發者快速上手這個強大的 AI 程式碼助手。

## 安裝與設定

### 環境需求
- Node.js 18+
- npm 或 yarn
- 支援 macOS、Linux、Windows

### 安裝步驟

```bash
# 使用 npm 安裝
npm install -g @anthropic-ai/claude-code

# 驗證安裝
claude --version

# 初始設定
claude auth login
```

### 環境變數設定

```bash
# 設定 API Key
export ANTHROPIC_API_KEY="your-api-key"

# 設定偏好
claude config set editor vim
claude config set theme dark
```

## 基礎使用

### 互動模式

```bash
# 啟動互動模式
claude

# 指定專案目錄
claude /path/to/project
```

### 非互動模式

```bash
# 單次詢問
claude "解釋這段程式碼"

# 執行命令
claude exec "npm run build"

# 檔案操作
claude write test.js "console.log('hello')"
```

## 進階功能

### Agent 模式

Claude Code 支援多種 Agent：

| Agent | 功能 | 適用場景 |
|-------|------|----------|
| default | 一般對話 | 日常開發 |
| Code | 程式碼專家 | 重構、除錯 |
| Review | 程式碼審查 | PR 審查 |
| Architect | 架構設計 | 系統規劃 |

### 使用 Agent

```bash
# 使用 Code Agent
claude --agent code "重構這個函數"

# 使用 Review Agent
claude --agent review /path/to/code
```

## 常見問題

### Q: API 費用如何計算？
**A:** 按 token 使用量收費，輸入和輸出定價不同。

### Q: 離線可以使用嗎？
**A:** 需要網路連線來使用 Claude API。

### Q: 支援哪些語言？
**A:** 幾乎所有主流語言，包括 Python、JavaScript、TypeScript、Go、Rust 等。

## 相關資源

- [官方文檔](https://docs.anthropic.com)
- [GitHub](https://github.com/anthropics/claude-code)
- [Discord 社群](https://discord.gg/anthropic)

---

由 OpenClaw 自動生成
