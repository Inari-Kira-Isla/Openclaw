---
name: alert_manager
description: 警報管理。當用戶說「設定警報」「查看警報」「警報規則」時觸發。
metadata: { "openclaw": { "emoji": "🔔" } }
---

# 警報管理

統一管理所有系統警報規則、觸發條件與通知發送，支援分級通知與升級機制。

## 操作 / 工作流程
1. 維護警報規則清單（存於 `memory_search`）：
   - 每條規則包含：指標名、閾值、等級、通知對象
2. 持續比對系統指標與警報規則
3. 觸發時依等級執行：
   - INFO：僅記錄到日誌
   - WARN：用 `message` 傳送 Telegram 通知
   - ERROR：Telegram 通知 + 標記需處理
   - CRITICAL：Telegram 緊急通知 + 持續提醒直到確認
4. 避免重複警報：同一事件 30 分鐘內不重複發送
5. 追蹤警報狀態：觸發 → 通知 → 確認 → 解決

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| action | string | status | 動作：`status` / `add` / `remove` / `list` |
| metric | string | — | 指標名稱（新增規則時使用） |
| threshold | number | — | 閾值（新增規則時使用） |
| level | string | warn | 等級：`info` / `warn` / `error` / `critical` |

## 輸出格式
```
🔔 警報管理

目前規則數：{total}
活躍警報：{active_count}

| 指標 | 閾值 | 等級 | 狀態 |
|------|------|------|------|
| {metric} | {threshold} | {level} | {status} |

最近觸發：
- {timestamp}: {alert_description} ({level})

靜默中：{muted_count} 個規則
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| Telegram 發送失敗 | 重試 3 次，若仍失敗記錄到日誌等待恢復 |
| 規則衝突（重複指標） | 提示已有規則，詢問是否更新 |
| 閾值無效 | 拒絕新增，提示合理的閾值範圍 |

## 使用範例
- "目前有哪些警報規則"
- "幫我加一個 CPU 超過 90% 的警報"
- "最近有觸發過什麼警報嗎"
