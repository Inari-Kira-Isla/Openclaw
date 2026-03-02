# Bot Team Setup Workflow

設定多 Bot 協作團隊的標準流程。

## 目標

將多個 Telegram Bots 設定為獨立 Agents，各自負責不同工作，由中央協調者管理。

## 步驟

### 1. 新增 Bot 帳號

```bash
# 在 openclaw.json 加入新帳號
openclaw channels login --channel telegram --account <name>
```

### 2. 建立 Agent

```bash
openclaw agents add <agent-id> --workspace ~/.openclaw/workspace-<agent-id>
```

### 3. 設定 Binding

在 openclaw.json 加入：
```json
"bindings": [
  {
    "agentId": "<agent-id>",
    "match": {
      "channel": "telegram",
      "accountId": "<account-id>"
    }
  }
]
```

### 4. 設定模型

在 agent 設定中加入：
```json
"model": "<provider/model>"
```

### 5. 設定 SOUL.md

為每個 Agent 定義：
- 角色 Identity
- 工作職責
- 溝通風格

### 6. 設定 Subagents 權限

在 main agent 加入：
```json
"subagents": {
  "allowAgents": ["<agent-1>", "<agent-2>", ...]
}
```

## 團隊配置範例

| Bot | Agent | 模型 | 角色 |
|-----|-------|------|------|
| Kira | main | MiniMax | 協調者 |
| Cynthia | cynthia | qwen2.5:7b | 快速回覆 |
| 史萊姆 | slime | llama3 | 學習/記憶 |
| Team | team | mistral | 團隊協調 |
| Evolution | evolution | deepseek-coder | 優化/進化 |

---

_更新：2026-02-27_
