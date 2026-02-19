---
name: workflow_improvement
description: 工作流改進與優化。當需要優化現有工作流程時觸發，包括：瓶頸分析、優化方案、實施評估、效果追蹤。
---

# Workflow Improvement

## 分析維度

### 1. 效能瓶頸
- 耗時步驟
- 等待時間
- 資源衝突

### 2. 錯誤模式
- 失敗步驟
- 重試次數
- 錯誤類型

### 3. 複雜度
- 步驟數量
- 依賴深度
- 分支數量

## 優化策略

### 並行化
```
串行: A → B → C → D
並行: A, B → C, D → 結果
```

### 簡化
```
複雜: A → B → C → D → E → F
簡化: A → [整合] → F
```

### 快取
- 重複結果快取
- 預計算常用值
- 減少重複計算

### 重試優化
- 智慧重試策略
- 快速失敗
- 降級處理

## 評估框架

### 指標測量
```json
{
  "before": {
    "total_time": "10s",
    "error_rate": "5%",
    "steps": 10
  },
  "after": {
    "total_time": "3s",
    "error_rate": "1%",
    "steps": 6
  },
  "improvement": {
    "speed": "+70%",
    "reliability": "+80%",
    "simplicity": "+40%"
  }
}
```

### 追蹤週期
- 發布後 24 小時
- 發布後 1 週
- 發布後 1 個月
