# TOOLS.md - 本地環境配置

## OpenClaw Gateway

- Host: `localhost:18789` (production)
- Auth: Token-based (OPENCLAW_GATEWAY_TOKEN)
- Config: `~/.openclaw/openclaw.json`
- Service: LaunchAgent (auto-start, keep-alive)

## Telegram

- Bot 帳號: Kira, Cynthia
- DM Policy: pairing mode
- Group Policy: allowlist

## 資料儲存

- **Notion** — BNI 會員、轉介紹、客戶、支出等資料庫
- **Memory** — `~/.openclaw/workspace/memory/` 每日筆記 + MEMORY.md
- **SQLite** — OpenClaw 內建向量搜尋 (sqlite-vec)

## 工作流自動化

- **n8n** — 已安裝，尚未建立 workflow
- 預計用途：Facebook Messenger webhook、WhatsApp 中轉

## AI 模型

- **MiniMax-M2.5** — 主要模型 (200K context, 8K output)
- API: `https://api.minimax.io/anthropic` (Anthropic 兼容)
- **nomic-embed-text** — 本地 Embedding 模型 (768 dims, GGUF, node-llama-cpp)

## 專案路徑

- OpenClaw repo: `~/openclaw-dev/repo/`
- openclaw-brain: `~/openclaw-brain/`
- OpenClawASR: `~/OpenClawASR/`
- Workspace: `~/.openclaw/workspace/`
- Skills: `~/.openclaw/workspace/skills/`

---

_更新：2026-02-24_
