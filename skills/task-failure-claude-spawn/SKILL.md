---
name: task-failure-claude-spawn
description: 當所有任務失敗時，自動 spawn Claude CLI 進行修復。攔截失敗的 cron job，調用 ACP runtime 執行修復。
metadata: { "openclaw": { "emoji": "🤖", "triggers": ["cron_failure", "task_failure"] } }
---

# 任務失敗 Claude 修復鉤子

當偵測到任務完全失敗時，自動 spawn Claude CLI 進行問題診斷與修復。

## 觸發條件

- Cron job 失敗
- 連續任務失敗達到閾值
- 特定關鍵錯誤出現

## 工作流程

### 1. 監控失敗

```bash
# 檢查最近失敗的任務
openclaw cron runs --status failed
```

### 2. 評估嚴重性

| 失敗類型 | 閾值 | 動作 |
|----------|------|------|
| 單一任務失敗 | 1次 | 記錄觀察 |
| 連續失敗 | 3次 | 發送警告 |
| 關鍵任務失敗 | 1次 | 立即修復 |

### 3. Spawn Claude 修復

```javascript
// 當需要修復時
openclaw sessions_spawn({
  runtime: "acp",
  agentId: "claude-sonnet", // 或根據任務類型選擇
  task: `修復以下失敗任務：\n\n${errorDetails}\n\n請分析錯誤原因並嘗試自動修復。`,
  mode: "run"
})
```

### 4. 修復後驗證

- 檢查修復是否成功
- 記錄修復過程
- 更新失敗任務狀態

## 配置

| 參數 | 預設 | 說明 |
|------|------|------|
| failure_threshold | 3 | 觸發修復的失敗次數 |
| critical_jobs | [] | 關鍵任務列表（1次失敗即修復） |
| model | claude-sonnet-4-20250514 | 修復用模型 |

## 使用方式

此鉤子為被動觸發，透過 OpenClaw 的 cron 或事件系統調用。

如需手動觸發：
- "檢查失敗任務並修復"
- "spawn claude 修復失敗任務"
