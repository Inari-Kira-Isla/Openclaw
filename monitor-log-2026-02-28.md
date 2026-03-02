# OpenClaw 監控日誌 — 2026-02-28

## 18:24 系統狀態

### Overview
| 項目 | 狀態 |
|------|------|
| Gateway | ✅ 運行中 (pid 44151) |
| Sessions | 316 active |
| 模型 | MiniMax-M2.5 (200k ctx) |
| Memory | ✅ vector ready, fts ready, cache on (296) |

### 熱門 Sessions
| Session | Age | Tokens | 狀態 |
|---------|-----|--------|------|
| agent:main:main | 4m | 61k/200k (30%) | 🟢 |
| agent:team:group | 7m | 103k/200k (52%) | 🟢 |
| agent:main:group | 8m | 156k/200k (78%) | ⚠️ 偏高 |
| agent:cynthia:group | 9m | 101k/200k (51%) | 🟢 |

### 安全審計 🔴
- **CRITICAL**: 小模型需啟用沙箱 + 停用網路工具
  - ollama/qwen2.5:7b 檢測到 (agents.defaults.model.fallbacks)
- **CRITICAL**: 配置文件 world-readable
  - `/Users/ki/.openclaw/openclaw.json` mode=644
  - Fix: `chmod 600 /Users/ki/.openclaw/openclaw.json`
- **WARN**: Reverse proxy headers 未信任
- **WARN**: 多用戶潛在風險

### Telegram 狀態
- 5/6 accounts configured
- ⚠️ 允許未提及的群組訊息 (requireMention=false)

### Heartbeat
- main: 30m 啟用
- 其他 30+ agents: disabled
