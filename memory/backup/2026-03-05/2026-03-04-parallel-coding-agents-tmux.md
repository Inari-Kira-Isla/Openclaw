# 並行 Coding Agents 與 Tmux 實踐指南

**標籤**: #coding-agents #tmux #parallel-development #devtools #productivity

**優先級**: P1

**更新日期**: 2026-03-04

---

## 為什麼使用 Tmux 進行並行開發

### Tmux 的核心優勢

1. **會話持久化** - 連線中斷不影響運行中的任務
2. **視窗分割** - 同時查看多個任務輸出
3. **會話共享** - 多個終端連接到同一會話
4. **腳本化** - 透過腳本自動化管理

---

## 實踐架構

```
┌─────────────────────────────────────────────┐
│           主控會話 (Main Session)             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ Agent 1 │ │ Agent 2 │ │ Agent 3 │       │
│  │  (PM)   │ │ (Dev)   │ │ (Test)  │       │
│  └────┬────┘ └────┬────┘ └────┬────┘       │
│       │           │           │              │
│       └───────────┴───────────┘              │
│                 │                            │
│           [協調層 Coordination]               │
└─────────────────────────────────────────────┘
```

---

## 最佳實踐

### 1. 會話命名規範

```bash
# 建立結構化會話名稱
SESSION="ai-coder-${PROJECT}-${DATE}"

# 範例
ai-coder-openclaw-20260304
```

### 2. 自動化腳本模板

```bash
#!/bin/bash
# parallel-agents.sh

PROJECT=$1
AGENTS=("planner" "coder" "reviewer" "tester")

# 建立主會話
tmux new-session -d -s "${PROJECT}"
tmux rename-window -t "${PROJECT}:0" "main"

# 為每個 Agent 建立專用視窗
for agent in "${AGENTS[@]}"; do
    tmux new-window -t "${PROJECT}" -n "${agent}" "./run-agent.sh ${agent}"
done

# 分割主視窗查看所有輸出
tmux split-window -h
tmux split-window -v
tmux select-layout tiled
```

### 3. Agent 協調模式

```bash
# 監控所有 Agent 狀態
watch -n 5 'tmux list-windows -t "${SESSION}"'

# 廣播命令到所有 Agent
tmux send-keys -t "${SESSION}:agent1" "cd /project" C-m
tmux send-keys -t "${SESSION}:agent2" "cd /project" C-m
```

---

## 實用 Tmux 命令速查

### 會話管理
```bash
# 建立會話
tmux new -s <name>

# 分離會話 (保持運行)
Ctrl+b d

# 重新連接
tmux attach -t <name>

# 列出會話
tmux ls
```

### 視窗操作
```bash
# 新建視窗
Ctrl+b c

# 切換視窗
Ctrl+b 0-9

# 重新命名視窗
Ctrl+b ,

# 關閉視窗
Ctrl+b &
```

### 分割視窗
```bash
# 水平分割
Ctrl+b "

# 垂直分割
Ctrl+b %

# 切換分割
Ctrl+b o

# 調整大小
Ctrl+b :resize-pane -D/U/L/R
```

---

## 與 AI Coding Agents 整合

### OpenClaw + Tmux 實踐

1. **Agent 隔離**: 每個 Agent 獨立會話，避免相互干擾
2. **狀態持久化**: Agent 崩潰不會丟失上下文
3. **並發執行**: 同時運行多個任務

```bash
# OpenClaw workflow 範例
openclaw spawn --agent code-agent --tmux opencoder-1
openclaw spawn --agent code-agent --tmux opencoder-2
openclaw monitor --session opencoder-project
```

---

## 常見問題與解決方案

### Q1: 如何處理 Agent 輸出過多?
```bash
# 滾動緩衝區設定
tmux set -g history-limit 50000

# 輸出到檔案
tmux pipe-pane -t "${WINDOW}" "tee /tmp/agent-${WINDOW}.log"
```

### Q2: 如何同步多個 Agent?
```bash
# 等待所有 Agent 準備就緒
for w in agent1 agent2 agent3; do
    while ! tmux capture-pane -t "${SESSION}:${w}" | grep -q "READY"; do
        sleep 1
    done
done
echo "All agents ready"
```

### Q3: 資源管理?
```bash
# 限制每個視窗的 CPU 使用
# 配合 cgroup 或 ulimit
```

---

## 內容創作方向

- 📝 **教程**: "5 分鐘學會用 Tmux 管理多個 AI Coding Agents"
- 📝 **腳本庫**: "AI Developer Tmux Starter Kit"
- 📝 **最佳實踐**: "大型專案的多 Agent 協作架構"
