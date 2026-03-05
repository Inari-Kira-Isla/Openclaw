# GitHub 監控報告 - 2026-03-04

## 📊 概覽
- **PRs:** 10 個新開啟
- **Issues:** 10 個新開啟

## 🔥 重點關注

### PRs

| # | Title | Labels | 相關性 |
|---|-------|--------|--------|
| **34055** | feat(acp): add sessions_spawn streamTo parent relay for ACP spawns | acp, maintainer | ⭐ ACP 核心功能 |
| **34046** | feat(hooks): add auto-wake hook — assistant speaks first after restart | - | ⭐ 新功能，自動喚醒 |
| **34053** | refactor(plugins): improve type safety in sync hook handlers | plugins | 中 |
| **34050** | fix(web): fix nested disconnect status code parsing | whatsapp-web | 中 |
| **34048** | fix(media): cap inbound extracted file blocks | media | 中 |

### Issues

| # | Title | Labels | 優先級 |
|---|-------|--------|--------|
| **34006** | Gateway crashes on unhandled fetch rejection when node disconnects | bug | 🔴 高 |
| **34052** | [Bug] Health monitor restarts ALL channels in multi-account setup | bug:crash | 🔴 高 |
| **34054** | ACP gateway should always call runtime.close() for completed oneshot sessions | - | 🟡 中 |
| **34041** | [Queued messages] causes duplicate delivery | - | 🟡 中 |
| **34008** | [Bug] Gemini 3 function calling softlocked via Ollama Cloud | bug:behavior | 🟡 中 |
| **34057** | Feature: Bot should self-report group ID when added to group | - | 🟢 功能建議 |
| **34056** | Feature: Send authorization hint when @mentioned but unauthorized | - | 🟢 UX 優化 |

## 🎯 系統相關性分析

### 與 OpenClaw 系統直接相關
1. **#34055** (ACP sessions_spawn) - 與我們的 ACP 架構直接相關
2. **#34046** (auto-wake hook) - 可考慮整合到系統
3. **#34006** (Gateway crash) - 需要關注
4. **#34052** (Health monitor bug) - 多帳號設定問題

### 不需要發起到群組討論
- 大部分為一般性 bug 修復和 UI 改進
- 翻譯相關 PR (#34044, #34043)
- Webchat 確認對話框 (#34051) - 小功能

## 📋 建議

✅ **已記錄但暫不需要群組討論:**
- #34055 ACP 功能將在穩定後自動應用
- #34006, #34052 為已知問題，等待 maintainer 修復

---
*Generated: 2026-03-04 14:31 UTC+8*
