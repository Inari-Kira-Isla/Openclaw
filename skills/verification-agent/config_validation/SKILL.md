---
name: config_validation
description: 配置驗證與檢查。當需要驗證系統配置是否正確時觸發，包括：語法檢查、權限檢查、依賴檢查、一致性檢查。
---

# Config Validation

## 驗證項目

### 1. 語法檢查
- JSON/YAML 語法正確
- 必要欄位存在
- 類型正確

### 2. 依賴檢查
- 必要套件已安裝
- 版本相容
- 沒有循環依賴

### 3. 權限檢查
- 檔案可讀寫
- API Key 有效
- 路徑存在

### 4. 一致性檢查
- 配置項目的邏輯一致性
- 與環境變數匹配
- 預設值合理

## 驗證清單

### agents.yml 驗證
- [ ] version 欄位存在
- [ ] 每個 agent 有 name
- [ ] 每個 agent 有 role
- [ ] model 有效
- [ ] skills 陣列存在

### Skill 驗證
- [ ] SKILL.md 存在
- [ ] YAML frontmatter 正確
- [ ] name 符合規範
- [ ] description 不為空

## 錯誤報告

```json
{
  "valid": false,
  "errors": [
    {
      "file": "agents.yml",
      "line": 42,
      "error": "missing required field 'model'",
      "severity": "error"
    }
  ],
  "warnings": [
    {
      "file": "agents.yml",
      "line": 10,
      "warning": "unused skill 'xxx'",
      "severity": "warning"
    }
  ]
}
```

## 驗證工具

```bash
# 語法檢查
yq validate agents.yml
jq . agents.yml

# 完整性檢查
openclaw config validate
```
