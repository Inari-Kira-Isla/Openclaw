---
name: api_key_audit
description: API 金鑰審計。當需要檢查和管理 API 金鑰時觸發，包括：金鑰識別、風險評估、到期檢查、安全建議。
---

# API Key Audit

## 審計維度

### 1. 存在性檢查
- 哪些金鑰已配置
- 存放位置
- 覆蓋範圍

### 2. 有效性檢查
- 是否過期
- 是否有效
- 權限範圍

### 3. 安全性檢查
- 暴露風險
- 權限過度
- 誰有訪問權

## 檢查清單

```json
{
  "keys": [
    {
      "name": "telegram_token",
      "location": "config",
      "status": "valid",
      "expires": null,
      "risk": "low"
    },
    {
      "name": "openai_api_key",
      "location": "env",
      "status": "expiring_soon",
      "expires": "2024-02-01",
      "risk": "medium"
    }
  ]
}
```

## 安全建議

| 風險 | 建議 |
|------|------|
| 金鑰暴露 | 使用環境變數 |
| 權限過大 | 最小權限原則 |
| 未過期 | 設定過期時間 |
| 無輪換 | 定期輪換 |

## 審計命令
```bash
# 檢查配置
openclaw config get

# 安全審計
openclaw security audit
```
