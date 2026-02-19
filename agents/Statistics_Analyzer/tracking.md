# 技能使用追蹤系統

## 追蹤目標
收集每個技能的使用數據，用於分析和優化

## 數據格式

### 技能使用記錄
```json
{
  "agent": "Writing_Master",
  "skill": "技術寫作",
  "timestamp": "2026-02-16T17:30:00Z",
  "context": "API文檔",
  "success": true,
  "rating": 5,
  "duration_seconds": 120
}
```

### 使用統計
```json
{
  "agent": "Writing_Master",
  "skill": "技術寫作",
  "total_uses": 50,
  "success_rate": 0.92,
  "avg_rating": 4.5,
  "last_used": "2026-02-16"
}
```

## 追蹤的關鍵指標

| 指標 | 說明 | 重要性 |
|------|------|--------|
| 使用次數 | 技能被調用次數 | ⭐⭐⭐⭐⭐ |
| 成功率 | 完成任務的比例 | ⭐⭐⭐⭐⭐ |
| 滿意度 | 用戶評分 | ⭐⭐⭐⭐ |
| 平均時間 | 完成任務平均時間 | ⭐⭐⭐ |

## 熟練度計算

```
經驗值 = 使用次數 × 權重 + 成功獎勵 - 失敗 penalty
```

### 等級閾值
| 等級 | 經驗值 |
|------|--------|
| Novice | 0-100 |
| Intermediate | 101-500 |
| Advanced | 501-1000 |
| Expert | 1001-2000 |
| Master | 2001+ |

## 下一步

選擇一個 Agent 開始試點收集數據！
