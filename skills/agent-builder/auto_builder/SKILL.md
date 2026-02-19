---
name: auto_builder
description: 自動化建構與部署。當需要自動建立和部署 Agent 時觸發，包括：配置寫入、重啟服務、驗證測試、狀態報告。
---

# Auto Builder

## 建構流程

```
配置生成 → 寫入配置 → 重啟服務 → 驗證 → 報告
```

## 步驟詳解

### 1. 配置寫入
```bash
# 備份現有配置
cp agents.yml agents.yml.bak

# 追加新 Agent 配置
cat >> agents.yml << EOF
  new-agent:
    role: specialist
    ...
EOF
```

### 2. 重啟服務
```bash
openclaw gateway restart
```

### 3. 驗證測試
```bash
# 檢查 Agent 狀態
openclaw status

# 測試 Agent 回應
echo "測試訊息" | openclaw chat --agent new-agent
```

## 安全檢查

### 建構前
- 配置語法驗證
- 技能存在性檢查
- 權限檢查

### 建構後
- Agent 可用性
- 功能正常運作
- 資源消耗正常

## 報告格式

```json
{
  "build_status": "success",
  "agent": "agent-name",
  "changes": ["新增配置"],
  "verification": {
    "syntax": "passed",
    "functionality": "passed"
  },
  "service_status": "running",
  "message": "Agent 建立成功"
}
```

## 回滾機制

```bash
# 如有問題，回滾配置
cp agents.yml.bak agents.yml
openclaw gateway restart
```
