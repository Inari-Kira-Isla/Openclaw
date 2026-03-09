---
name: decision-optimization-hook
description: |
  決策優化鉤子。當需要追蹤決策結果、分析信心度、優化決策系統時使用。
  功能：(1) 記錄每次決策與結果 (2) 統計分析 (3) 信心度校準 (4) 持續優化閉環。
  適用場景：(1) Claude 決策後追蹤 (2) 決策準確率分析 (3) 信心度優化
metadata:
  {
    "openclaw": { "emoji": "📈", "requires": { "anyTools": ["exec", "read", "write"] } },
  }
---

# Decision Optimization Hook

決策追蹤、分析、優化的完整閉環系統

## 流程

```
┌─────────────────────────────────────────────────────────────┐
│                    決策優化閉環                                │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  1. 記錄決策                                               │
│     - 決策內容                                              │
│     - 信心度                                                │
│     - 上下文                                                │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  2. 執行 + 追蹤結果                                         │
│     - 執行決策                                              │
│     - 記錄結果 (成功/失敗)                                   │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 統計分析                                                │
│     - 信心度 vs 實際結果                                     │
│     - 找出規律                                              │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  4. 優化信心度                                              │
│     - 校準過高                                              │
│     - 提升過低                                              │
│     - 更新規則                                              │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  5. 下次決策                                                │
│     - 使用優化的信心度                                       │
│     - 更準確的決策                                          │
└─────────────────────────────────────────────────────────────┘
```

## 數據結構

```json
{
  "decisions": [
    {
      "id": "uuid",
      "timestamp": "2026-03-02T02:58:00",
      "context": "網站部署",
      "decision": "preview",
      "confidence": 0.8,
      "result": "success",
      "duration_ms": 1500,
      "claude_used": false
    }
  ],
  "statistics": {
    "total": 100,
    "success": 85,
    "accuracy": 0.85,
    "avg_confidence": 0.75,
    "confidence_calibration": 0.85
  }
}
```

## 使用方式

### 1. 記錄決策

```javascript
// 記錄新決策
decisionTracker.record({
  context: "網站部署",
  decision: "preview",
  confidence: 0.8,
  claude_used: false
});
```

### 2. 記錄結果

```javascript
// 執行後記錄結果
decisionTracker.recordResult({
  decisionId: "uuid",
  result: "success"  // "success" | "failure"
});
```

### 3. 獲取統計

```javascript
// 獲取分析報告
const stats = decisionTracker.getStats();
// { accuracy: 0.85, confidence_calibration: 0.85, ... }
```

### 4. 優化建議

```javascript
// 獲取優化建議
const suggestions = decisionTracker.getOptimizations();
// ["信心度 0.9 過高，實際準確率 0.7", ...]
```

## 信心度校準

| 信心度 | 實際準確率 | 校準動作 |
|--------|-----------|----------|
| 0.9 | 0.9 | 無需調整 |
| 0.9 | 0.6 | 降低信心度 |
| 0.5 | 0.8 | 提高信心度 |

### 公式

```
校準後信心度 = 實際準確率 × 信心度權重 + 原始信心度 × (1 - 信心度權重)
```

## 統計指標

| 指標 | 說明 |
|------|------|
| accuracy | 整體準確率 |
| confidence_calibration | 信心度與準確率匹配度 |
| claude_vs_autonomous | Claude 決策 vs 自主決策效果 |
| trend | 趨勢分析 |

## 決策規則優化

```javascript
// 根據歷史數據調整規則
const rules = {
  "網站完成": {
    default: "preview",
    min_confidence: 0.6,
    claude_threshold: 0.4,
    // 根據數據自動調整
    optimized: {
      success_rate: 0.85,
      avg_duration: 2000
    }
  }
};
```

## 整合閉環系統

```javascript
// 完整流程
async function closedLoopWithOptimization(context) {
  // 1. 決策
  const decision = await autoDecide(context);
  
  // 2. 記錄決策
  const decisionId = decisionTracker.record({
    context,
    decision: decision.decision,
    confidence: decision.confidence,
    claude_used: decision.type === "complex"
  });
  
  // 3. 執行
  const result = await execute(decision);
  
  // 4. 記錄結果
  decisionTracker.recordResult({
    decisionId,
    result: result.success ? "success" : "failure"
  });
  
  // 5. 分析
  const stats = decisionTracker.getStats();
  
  // 6. 優化
  if (stats.need_calibration) {
    decisionTracker.calibrate();
  }
  
  return result;
}
```

## 範例情境

### 情境：網站部署決策

```
1. 決策記錄
   決策: 預覽網站
   信心度: 0.8
   類型: 自主

2. 執行結果
   結果: 成功
   耗時: 2s

3. 統計分析
   準確率: 0.85
   信心度校準: 0.85
   趨勢: 📈 上升中

4. 優化
   信心度 0.8 → 保持
   規則: 無需調整
```

### 情境：複雜決策

```
1. 決策記錄
   決策: 部署上線
   信心度: 0.5
   類型: Claude

2. 執行結果
   結果: 失敗 (需要網域)

3. 統計分析
   原因: 缺少前置條件
   建議: 添加檢查清單

4. 優化
   更新規則: 部署前檢查網域
```
