---
name: perfect-closed-loop
description: |
  完美閉環系統。當需要執行複雜任務並確保完整流程追蹤時使用。
  流程：(1) 前期準備 - 搜尋記憶、網路、整理上下文 (2) 判斷 - 簡單任務直接處理，複雜任務 spawn Claude CLI (3) 執行 - 
  調用 Claude CLI 執行任務 (4) 閉環 - 結果記錄到 Memory、Telegram 通知。
  適用場景：(1) 研究任務 (2) 複雜分析 (3) 技術實現 (4) 需要決策的任務
metadata:
  {
    "openclaw": { "emoji": "🔄", "requires": { "anyTools": ["memory_search", "web_search", "message", "exec"] } },
  }
---

# Perfect Closed-Loop System

完整閉環：前期整理 → 判斷分流 → Claude 執行 → 閉環回報

## 流程圖

```
┌─────────────────────────────────────────────────────────────┐
│  📋 Phase 1: OpenClaw 前期準備                              │
│  ┌──────┐  ┌───────┐  ┌──────┐  ┌──────┐                 │
│  │資料搜集│→│整理分析│→│任務分解│→│脈絡組裝│                 │
│  └──────┘  └───────┘  └──────┘  └──────┘                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ context + prompt
                           ▼
┌────────────────────────────────────────────────────────────  ⚡ Phase 2: Claude─┐
│ CLI 執行 (sessions_spawn)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  深度分析 / 編碼 / 決策                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ result
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  🔄 Phase 3: OpenClaw 閉環                                   │
│  ┌──────┐  ┌───────┐  ┌──────┐  ┌──────┐                   │
│  │結果彙總│→│品質把關│→│決策判斷│→│觸發下一步│                 │
│  └──────┘  └───────┘  └──────┘  └──────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## 使用方式

### 1. 接收任務

```
User: "研究最新 AI Agents 趨勢"
```

### 2. Phase 1: 前期準備

```javascript
// 2.1 分析任務類型
const taskType = analyzeTask(task)
// 回傳: simple | complex | tech | decision

// 2.2 搜尋相關上下文
memory_search({ query: "AI Agents 趨勢 相關" })
web_search({ query: "AI Agents trends 2026" })

// 2.3 組裝 Prompt
const prompt = buildPrompt(task, context)
```

### 3. Phase 2: 判斷分流

| 任務類型 | 處理方式 |
|----------|----------|
| simple | OpenClaw 直接處理 |
| complex | spawn Claude CLI |
| tech | spawn Claude CLI |
| decision | spawn Claude CLI 提供選項 |

### 4. Phase 2.5: 執行（簡單任務）

```javascript
// 直接執行
web_search(...)
memory_search(...)
```

### 5. Phase 2.5: 執行（複雜任務）

```javascript
// 使用 Claude CLI
exec({
  command: "claude -p '你的 prompt'",
  pty: true,
  workdir: "/tmp/task-xxx"
})

// 或通過 sessions_spawn（未來）
sessions_spawn({
  runtime: "acp",
  agentId: "claude",
  task: prompt
})
```

### 6. Phase 3: 閉環

```javascript
// 6.1 結果彙總
const summary = summarize(result)

// 6.2 品質判斷
if (quality < threshold) {
  // 需要重試
  retry()
} else if (needsHumanDecision) {
  // 需要人類決策
  notifyHuman(result)
} else {
  // 完成
  close()
}

// 6.3 記錄 Memory
writeToMemory({
  task: task,
  result: result,
  timestamp: now
})

// 6.4 Telegram 回報
message({
  action: "send",
  target: "group",
  message: `✅ 任務完成\n\n${summary}`
})
```

## 決策點

| 狀態 | 動作 |
|------|------|
| COMPLETE | 記錄結果，關閉任務 |
| NEEDS_RETRY | 重新執行或修復 |
| NEEDS_HUMAN_DECISION | 回報人類決策 |

## 範例流程

### 範例 1: 研究任務

```
User: "研究最新 AI Agents 趨勢"

Kira:
1. analyzeTask → complex
2. memory_search → 過往 AI 研究
3. web_search → 2026 AI Trends
4. buildPrompt → 注入上下文
5. exec(claude) → 研究分析
6. summary → 產出報告
7. recordMemory → 存儲結果
8. notifyTelegram → 回報結果
```

### 範例 2: 簡單查詢

```
User: "今天天氣如何?"

Kira:
1. analyzeTask → simple
2. 直接用天氣 API
3. 回覆用戶
```

### 範例 3: 技術實現

```
User: "幫我重構記憶系統"

Kira:
1. analyzeTask → tech
2. memory_search → 現有架構
3. buildPrompt → 注入代碼上下文
4. exec(claude) → 重構
5. 驗證結果
6. 回報
```

## 最佳實踐

1. **始終先分析任務類型** - 避免過度使用 Claude
2. **充分準備上下文** - 讓 Claude 知道背景
3. **記錄每次執行** - 建立學習循環
4. **及時回報** - Telegram 通知讓用戶知道進度
5. **質量把關** - 不合格的結果要重試
