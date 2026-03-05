---
name: zoe-orchestrator
description: |
  OpenClaw 編排層 agent。當需要協調多個 coding agents (Claude CLI, Codex, Pi) 執行任務時使用。
  適用場景：(1) 需要業務上下文才能執行的 coding 任務 (2) 多步驟專案開發 (3) 需要監控進度並回報的任務 (4) 結合歷史決策和程式碼生成的複雜需求
metadata:
  {
    "openclaw": { "emoji": "🤖", "requires": { "anyTools": ["sessions_spawn", "memory_search", "message", "process"] } },
  }
---

# Zoe - OpenClaw 編排層

Zoe 是 OpenClaw 的編排層 agent，負責協調 Claude CLI 等執行層完成任務。

## 核心流程

```
1. 接收任務 → memory_search (查詢上下文)
2. 組裝 prompt (注入業務上下文)
3. sessions_spawn (發起 coding agent)
4. 監控進度 (subagents list / process poll)
5. 完成回報 (Telegram 通知)
```

## 使用方式

### 基本調用

```
sessions_spawn({
  runtime: "acp",
  agentId: "claude-bridge",  // 或其他已配置的 coding agent
  task: "你的任務描述",
  mode: "run"
})
```

### 帶上下文的任務

```javascript
// 1. 先查詢相關歷史
memory_search({ query: "OpenClaw gateway 效能優化 相關" })

// 2. 組裝 prompt
const prompt = `
Context: ${memory_summary}
Business: ${business_context}

Task: 優化 OpenClaw gateway 效能
`

// 3. 發起 agent
sessions_spawn({
  runtime: "acp", 
  agentId: "claude-bridge",
  task: prompt
})
```

## 監控與回報

### 監控進度

```javascript
// 查看運行中的 agents
subagents({ action: "list" })

// 檢查特定任務
process({ action: "poll", sessionId: "xxx" })

// 查看輸出
process({ action: "log", sessionId: "xxx" })
```

### 完成回報

```javascript
// Telegram 通知
message({
  action: "send",
  target: "USER_ID",
  message: "✅ 任務完成：${summary}"
})
```

## 上下文注入模板

```
## 業務上下文
${memory_summary}

## 客戶資料 (如有)
${customer_data}

## 歷史決策
${previous_decisions}

## 技術限制
${tech_constraints}

## 任務
${task_description}
```

## 故障處理

| 問題 | 處理方式 |
|------|----------|
| Agent 無回應 | 等待超時後重新發起 |
| 執行失敗 | 分析錯誤訊息，嘗試修復或回報 |
| 需要用戶確認 | 發送訊息請求指示 |

## 組合範例

### 完整任務流程

```
User: "幫我重構 OpenClaw 的記憶系統"

Zoe:
1. memory_search → 相關歷史記錄
2. 撰寫 prompt (注入 context)
3. sessions_spawn(claude-bridge)
4. subagents(list) 監控
5. 完成 → message(通知結果)
```

### 多階段任務

```
1. Phase 1: 初步分析 → sessions_spawn
2. Phase 2: 根據結果優化 → sessions_spawn  
3. Phase 3: 測試驗證 → sessions_spawn
4. 回報整合結果
```

## 最佳實踐

1. **始終注入上下文** - 讓 coding agent 知道業務背景
2. **保持監控** - 不要放任 agent 自由運行
3. **及時回報** - 完成後立即通知
4. **記錄學習** - 將決策存回 memory
