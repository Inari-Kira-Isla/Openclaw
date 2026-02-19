---
name: openclaw-monitor
description: OpenClaw 監控工具 - 監控 token 使用、session 狀態
metadata:
  openclaw:
    emoji: "📊"
    version: "1.0"
---

# OpenClaw 監控方案

## 內建監控

OpenClaw 已有內建狀態監控：

```bash
# 查看狀態
openclaw status

# 查看 session
openclaw sessions --limit 5

# 查看特定 session
openclaw sessions --key agent:main:main
```

---

## 顯示內容

| 項目 | 說明 |
|------|------|
| Tokens (ctx %) | 上下文使用百分比 |
| Age | session 存活時間 |
| Model | 使用模型 |
| Flags | 特殊標記 |

---

## 即時監控腳本

### 監控 session 狀態

```bash
#!/bin/bash
# monitor-sessions.sh

while true; do
    clear
    echo "=== OpenClaw Session Monitor ==="
    echo "時間: $(date)"
    echo ""
    openclaw sessions --limit 5
    echo ""
    echo "按 Ctrl+C 退出"
    sleep 10
done
```

### 監控 token 使用

```bash
#!/bin/bash
# monitor-tokens.sh

while true; do
    openclaw sessions --limit 3 | grep -E "(Tokens|ctx)"
    sleep 5
done
```

---

## 建立監控腳本

```bash
# 建立監控目錄
mkdir -p ~/Desktop/openclaw-monitor

# 建立 session 監控
cat > ~/Desktop/openclaw-monitor/session-monitor.sh << 'EOF'
#!/bin/bash
echo "=== OpenClaw Session Monitor ==="
openclaw sessions --limit 5
EOF

chmod +x ~/Desktop/openclaw-monitor/session-monitor.sh
```

---

## Session Status 顯示

```
Kind   Key                        Age       Model          Tokens (ctx %)
direct agent:main:main            1m ago    MiniMax-M2.5   91k/200k (46%)
```

| 欄位 | 意義 |
|------|------|
| Tokens | 已用/總量 |
| ctx % | 上下文使用率 |

---

## 與 Claude Code 比較

| 功能 | Claude Code | OpenClaw |
|------|-------------|----------|
| 顯示方式 | statusline | CLI 命令 |
| 即時性 | 每行更新 | 可監控 |
| 自動壓縮 | /compact | 自動管理 |
| 內建 | 否 | ✅ 是 |

---

## 使用方式

```bash
# 快速查看
openclaw sessions

# 監控模式
~/Desktop/openclaw-monitor/session-monitor.sh
```

---

## Context 管理

OpenClaw 自動處理：
- 對話歷史壓縮
- 記憶分層
- 向量搜尋

不需要手動 /compact！

---
