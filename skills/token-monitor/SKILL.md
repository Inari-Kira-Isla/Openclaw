---
name: token-monitor
description: |
  Claude Token 計算與監控。當需要追蹤 Claude CLI 使用量、計算成本、分析趨勢時使用。
  適用場景：(1) 追蹤每次 Claude 執行的 token 消耗 (2) 每日/每週成本統計 (3) 
  監控對話長度是否超標 (4) 優化 prompt 減少 token 使用
metadata:
  {
    "openclaw": { "emoji": "💰", "requires": { "anyTools": ["exec", "read"] } },
  }
---

# Token Monitor

Claude Token 計算與監控系統

## 快速查詢

```bash
# 查詢本週統計
python ~/.openclaw/workspace/scripts/claude_token_tracker.py --stats 7

# 查詢本月統計
python ~/.openclaw/workspace/scripts/claude_token_tracker.py --stats 30
```

## 使用方式

### 1. 追蹤執行

```bash
# 執行任務並追蹤
python ~/.openclaw/workspace/scripts/claude_token_tracker.py "你的任務"
```

輸出:
```
🎯 任務: 你的任務...
✅ 完成 (15.2s)
   📥 Input:  1,234 tokens
   📤 Output: 2,567 tokens
   💰 Cost:   $0.0234
```

### 2. 統計分析

```bash
# 過去 7 天
python ~/.openclaw/workspace/scripts/claude_token_tracker.py --stats 7

# 過去 30 天
python ~/.openclaw/workspace/scripts/claude_token_tracker.py --stats 30
```

輸出:
```
📊 Claude Token 統計 (過去 7 天)
========================================
   任務數:     23
   Token總量:  156,789
   總成本:     $1.2345
   平均/任務:  6,817 tokens
   平均耗時:   12.3s
```

## 計算方式

### Token 估算
- **約 4 個字元 = 1 token** (中文較高，約 2 字 = 1 token)
- 精確計算需要 API 回傳的 usage 欄位

### 成本計算 (Claude Sonnet 4)

| 類型 | 價格 |
|------|------|
| Input | $3 / 1M tokens |
| Output | $15 / 1M tokens |

### 公式
```
Cost = (InputTokens × $3/M) + (OutputTokens × $15/M)
```

## 監控指標

| 指標 | 警告閾值 |
|------|----------|
| 單次輸出 | > 5,000 tokens |
| 每日總量 | > 50,000 tokens |
| 每月成本 | > $10 |
| 對話長度 | > 20,000 tokens |

## 整合 Telegram 回報

```javascript
// 每日定時回報
const stats = exec("python ~/.openclaw/workspace/scripts/claude_token_tracker.py --stats 1")

message({
  action: "send",
  target: "group",
  message: `📊 昨日 Claude 使用情況\n\n${stats.stdout}`
})
```

## 優化建議

| 問題 | 解決方案 |
|------|----------|
| Prompt 太長 | 使用精簡指令，移除冗餘描述 |
| 輸出太多 | 指定輸出格式限制長度 |
| 重複上下文 | 使用 summary 而非完整記錄 |
| 太頻繁調用 | 合併多次任務為一次 |

## 歷史記錄

記錄檔案: `~/.claude_token_history.json`

結構:
```json
[
  {
    "timestamp": "2026-03-02T02:30:00",
    "task": "你的任務",
    "input_tokens": 1234,
    "output_tokens": 2567,
    "total_tokens": 3801,
    "duration_seconds": 15.2,
    "cost": {
      "input_tokens": 1234,
      "output_tokens": 2567,
      "total_tokens": 3801,
      "cost_usd": 0.0234
    }
  }
]
```
