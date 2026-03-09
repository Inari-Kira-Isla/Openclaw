# Claude Code Skills - 深入研究

**日期**: 2026-02-20
**來源**: GitHub anthropics/skills

---

## 什麼是 Skills？

Skills 是「指令、腳本和資源的資料夾」，Claude 會動態載入以提高特定任務的表現。

> Skills 教 Claude 如何以可重複的方式完成特定任務

---

## 官方資源

| 資源 | 連結 |
|------|------|
| GitHub | github.com/anthropics/skills |
| 文檔 | code.claude.com/docs |
| 標準 | agentskills.io |

---

## Skills 類型

| 類型 | 說明 |
|------|------|
| **Creative & Design** | 藝術、音樂、設計 |
| **Development & Technical** | 測試、Web Apps、MCP |
| **Enterprise & Communication** | 企業工作流 |
| **Document Skills** | 文件處理 (docx, pdf, pptx, xlsx) |

---

## 與 OpenClaw Skills 的比較

| 特性 | Claude Code Skills | OpenClaw Skills |
|------|-------------------|-----------------|
| 格式 | SKILL.md + 資源 | SKILL.md |
| 載入方式 | 動態載入 | 靜態配置 |
| 標準 | agentskills.io | 自有格式 |
| 類型 | 多樣化 | 較少 |

---

## 安裝方式

```bash
# MacOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew
brew install --cask claude-code
```

---

## 整合建議

1. **採用標準** - 參考 agentskills.io 格式
2. **擴展類型** - 增加更多 Skill 類型
3. **動態載入** - 實現動態 Skill 載入
4. **資源支持** - 允許包含腳本/資源

---
