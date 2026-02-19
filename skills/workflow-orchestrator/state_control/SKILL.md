---
name: state_control
description: 狀態管理與追蹤。當需要管理長時間運行的任務狀態時觸發，包括：狀態儲存、進度記錄、中斷恢復、狀態查詢。
---

# State Control

## 核心功能

1. **狀態儲存** - 保存任務的當前狀態
2. **進度記錄** - 記錄每個步驟的完成情況
3. **中斷恢復** - 支援任務中斷後的恢復
4. **狀態查詢** - 提供狀態查詢介面

## 狀態類型

### 任務狀態
| 狀態 | 描述 |
|------|------|
| pending | 等待開始 |
| running | 執行中 |
| paused | 暫停 |
| completed | 完成 |
| failed | 失敗 |
| cancelled | 取消 |

### 步驟狀態
| 狀態 | 描述 |
|------|------|
| pending | 等待執行 |
| running | 執行中 |
| completed | 完成 |
| skipped | 跳過 |
| failed | 失敗 |

## 狀態儲存

### 儲存位置
- 短期：記憶體
- 長期：檔案/資料庫

### 儲存內容
```json
{
  "task_id": "任務ID",
  "created_at": "創建時間",
  "updated_at": "更新时间",
  "status": "任務狀態",
  "progress": {
    "current": 2,
    "total": 5,
    "percentage": 40
  },
  "context": {
    "step_results": [],
    "variables": {}
  },
  "error": null
}
```

## 恢復機制

### 檢查點
- 每個步驟完成後儲存檢查點
- 包含完整上下文

### 恢復流程
```
檢查是否有未完成任務 → 載入狀態 → 從斷點繼續
```

### 清理規則
- 成功完成 7 天後刪除
- 失敗 30 天後歸檔
