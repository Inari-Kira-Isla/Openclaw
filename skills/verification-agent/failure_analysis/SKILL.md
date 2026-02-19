---
name: failure_analysis
description: 失敗分析與診斷。當需要分析系統或任務失敗的原因時觸發，包括：錯誤分類、根因分析、修復建議、預防措施。
---

# Failure Analysis

## 錯誤分類

### 層級分類
| 層級 | 描述 | 範例 |
|------|------|------|
| L1 | 輸入錯誤 | 參數格式錯誤、缺參數 |
| L2 | 執行錯誤 | API 調用失敗、超時 |
| L3 | 邏輯錯誤 | 計算錯誤、判斷失誤 |
| L4 | 系統錯誤 | 記憶體不足、磁碟滿 |

### 錯誤模式
- Timeout - 執行超時
- Permission - 權限不足
- Not Found - 資源不存在
- Validation - 驗證失敗
- Network - 網路錯誤
- Rate Limit - 頻率限制

## 分析流程

```
收集錯誤資訊 → 分類錯誤 → 找出根因 → 提出修復 → 記錄教訓
```

### 錯誤資訊收集
```json
{
  "timestamp": "錯誤時間",
  "error_type": "錯誤類型",
  "error_message": "錯誤訊息",
  "stack_trace": "堆疊追蹤",
  "context": {
    "user_input": "用戶輸入",
    "system_state": "系統狀態"
  }
}
```

## 根因分析技術

### 5 Whys
```
為什麼失敗？因為 API 返回錯誤
為什麼 API 返回錯誤？因為超時
為什麼超時？因為請求太多
為什麼請求太多？因為沒有緩存
為什麼沒有緩存？因為忘記實現
```

### 修復建議模板
```json
{
  "issue": "問題描述",
  "root_cause": "根本原因",
  "fix": "修復方案",
  "priority": "high|medium|low",
  "estimated_effort": "修復工作量"
}
```

## 預防措施

1. 添加驗證
2. 增加錯誤處理
3. 添加監控
4. 優化架構
5. 增加測試
