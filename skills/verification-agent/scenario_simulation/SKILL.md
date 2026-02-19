---
name: scenario_simulation
description: 情境模擬測試。當需要模擬真實使用情境進行測試時觸發，包括：情境設計、測試案例、執行模擬、結果分析。
---

# Scenario Simulation

## 測試情境設計

### 情境類型

| 類型 | 描述 | 範例 |
|------|------|------|
| Happy Path | 正常流程 | 查詢天氣 → 顯示結果 |
| Edge Case | 邊界情況 | 無效輸入 → 適當處理 |
| Error Case | 錯誤情況 | 網路錯誤 → 顯示錯誤訊息 |
| Complex | 複雜情境 | 多步驟任務 → 正確串接 |

### 情境模板
```json
{
  "scenario": "情境名稱",
  "description": "情境描述",
  "preconditions": ["前提條件"],
  "steps": [
    {"step": 1, "action": "執行動作", "expected": "預期結果"}
  ],
  "expected_outcome": "最終預期結果"
}
```

## 執行模式

### 1. 單一情境
```
輸入 → 執行 → 比對結果 → 通過/失敗
```

### 2. 批量情境
```
情境集 → 逐一執行 → 彙總報告
```

### 3. 鏈式情境
```
情境1 → 結果 → 情境2 → ...
```

## 結果分析

### 評估維度
- 正確性：輸出是否符合預期
- 完整性：是否處理所有情況
- 效率：執行時間是否合理
- 容錯：錯誤處理是否恰當

### 報告格式
```json
{
  "total": 10,
  "passed": 8,
  "failed": 2,
  "details": [
    {"scenario": "xxx", "status": "passed/failed", "reason": "..."}
  ]
}
```
