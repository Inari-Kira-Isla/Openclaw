# OpenClaw + Claude Code 整合方案

## 架構設計

```
┌─────────────────┐     ┌─────────────────┐
│   OpenClaw     │     │  Claude Code   │
│  (橋梁/調度)    │────▶│   (執行層)     │
│                 │     │                 │
│ • 接收指令      │     │ • 實際運算      │
│ • 排程管理      │     │ • 代碼生成      │
│ • 結果記錄      │◀────│ • 任務執行      │
│ • 回傳結果      │     │ • 回傳輸出      │
└─────────────────┘     └─────────────────┘
         │
         ▼
    Grok API (橋梁)
```

---

## 整合方式

### 方式 1：TMUX 整合 (推薦)

```bash
# 1. 啟動 Claude Code 在 TMUX
tmux new -s claude -d "claude"

# 2. OpenClaw 傳送指令
tmux send-keys -t claude "你的指令" Enter

# 3. 獲取輸出
tmux capture-pane -t claude -p
```

### 方式 2：Subagent 整合

```python
# 使用 sessions_spawn 調用 Claude Code Agent
sessions_spawn(
    runtime="subagent",
    agentId="claude-code",
    task="執行呢個任務..."
)
```

### 方式 3：API 整合

```bash
# Claude Code 有 REST API
curl -X POST http://localhost:8080/api/execute \
  -d '{"task": "你的指令"}'
```

---

## 實施步驟

### Step 1：環境準備

| 項目 | 狀態 | 動作 |
|------|------|------|
| Claude Code 安裝 | ✅ 已有 | 確認路徑 |
| TMUX 設定 | ✅ 已有 | 確認可用 |
| Grok API Key | ✅ 已有 | 確認有效 |

### Step 2：建立連接脚本

```python
# claude_bridge.py
import subprocess

def send_to_claude_code(command):
    """傳送指令俾 Claude Code"""
    # TMUX 方式
    subprocess.run(["tmux", "send-keys", "-t", "claude", command, "Enter"])
    return True

def get_claude_output():
    """獲取 Claude Code 輸出"""
    result = subprocess.run(
        ["tmux", "capture-pane", "-t", "claude", "-p"],
        capture_output=True, text=True
    )
    return result.stdout
```

### Step 3：設定排程

```yaml
# cron 設定
- 任務：OpenClaw Bridge
- 觸發：收到指令
- 流程：
  1. 接收指令
  2. 轉發俾 Claude Code
  3. 等待結果
  4. 記錄並回傳
```

---

## 成本分析

| 組件 | 成本 | 備註 |
|------|------|------|
| OpenClaw | $0 | 已有 |
| Grok API | ~$5/月 | 橋梁費用 |
| Claude Max | 已包月 | 執行層 |
| Claude Code | 本地運行 | 無額外費用 |

**總成本：~$5/月** (只用 Grok 橋梁)

---

## 優點 vs 缺點

### ✅ 優點

1. **慳錢** - 只用 Grok 橋梁費
2. **強大** - Claude Max 質量保證
3. **靈活** - OpenClaw 排程 + Claude Code 執行
4. **隔離** - 執行環境分離

### ⚠️ 缺點

1. **延遲** - 雙重調用 (~1-2秒)
2. **複雜** - 需要維護連接
3. **依賴** - Claude Code 需要運行

---

## 決定清單

- [ ] 確認 Claude Code 已安裝並運行
- [ ] 確認 TMUX 可用
- [ ] 確認 Grok API 正常
- [ ] 決定整合方式 (TMUX/API/Subagent)
- [ ] 測試單一指令
- [ ] 設定排程

---

**準備好可以開始整？** 🦞
