---
name: auto_fix_hook
description: 自動修復鉤子。定時檢測系統錯誤並嘗試自動修復，包括：cron job 失敗、配置異常、服務中斷等。
metadata: { "openclaw": { "emoji": "🔧" } }
---

# 自動修復鉤子

定時檢測系統錯誤並嘗試自動修復，實現系統自癒能力。

## 操作 / 工作流程

### 1. 錯誤檢測

透過 `exec` 調用 `openclaw cron runs` 取得最近錯誤：

```
openclaw cron runs --id {jobId}
```

### 2. 錯誤分類

| 錯誤類型 | 辨識關鍵字 | 修復策略 |
|----------|-----------|----------|
| timeout | "job execution timed out" | 增加超時 / 簡化任務 |
| delivery_failed | "announce delivery failed" | 檢查 agent 狀態 / 重新調度 |
| permission | "permission denied" | 修復權限 |
| not_found | "not found" | 重新創建資源 |

### 3. 自動修復執行

根據錯誤類型執行對應修復：

```javascript
// 範例修復邏輯
if (error.includes("timeout")) {
  // 嘗試增加超時時間
  exec(`openclaw cron edit ${jobId} --timeout 180`)
}

if (error.includes("delivery failed")) {
  // 檢查目標 agent 是否在線
  exec(`openclaw sessions list --agent ${targetAgent}`)
  // 嘗試重新調度
  exec(`openclaw cron run ${jobId}`)
}
```

### 4. 修復記錄

將修復記錄寫入記憶：

```
## 自動修復日誌 - {timestamp}

| 錯誤 ID | 錯誤類型 | 修復動作 | 結果 |
|---------|----------|----------|------|
| {jobId} | {type} | {action} | {result} |
```

### 5. 上報修復失敗

若自動修復失敗，發送通知給管理員：

```
🔧 自動修復失敗

錯誤：{error}
嘗試修復：{action}
建議：{manual_fix}
```

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| check_interval | number | 30 | 檢查間隔（分鐘） |
| max_retries | number | 3 | 最大重試次數 |
| auto_fix | boolean | true | 是否自動修復 |

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 無法取得錯誤列表 | 跳過本次，記錄日誌 |
| 修復失敗 | 上報管理員，手動處理 |
| 修復成功 | 記錄並持續監控 |

## 使用範例

- "檢查系統錯誤並嘗試修復"
- "auto-fix-hook status"
- "最近有自動修復什麼嗎"
