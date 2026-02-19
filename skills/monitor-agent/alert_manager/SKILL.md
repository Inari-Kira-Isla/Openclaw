---
name: alert_manager
description: 警報管理。當需要管理系統警報和通知時觸發，包括：警報規則、觸發條件、通知渠道、升級機制。
---

# Alert Manager

## 警報級別

| 級別 | 描述 | 通知 |
|------|------|------|
| INFO | 資訊 | 記錄 |
| WARN | 警告 | 訊息 |
| ERROR | 錯誤 | 訊息+郵件 |
| CRITICAL | 緊急 | 訊息+電話 |

## 規則配置

```json
{
  "rules": [
    {"metric": "cpu", "threshold": 80, "level": "warn"},
    {"metric": "memory", "threshold": 90, "level": "error"},
    {"metric": "disk", "threshold": 95, "level": "critical"}
  ]
}
```

## 通知渠道
- 訊息 (Telegram/Discord)
- 郵件
- 電話 (緊急)
