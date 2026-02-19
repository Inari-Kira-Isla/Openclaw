---
name: workflow_router
description: 任務路由與分發。當需要將用戶需求分發到正確的專業 Agent 時觸發，包括：任務分類、Agent 選擇、優先級判定、串接順序規劃。
---

# Workflow Router

## 核心功能

1. **任務分類** - 分析用戶需求，判斷任務類型
2. **Agent 選擇** - 從可用 Agent 清單中選擇最適合的
3. **優先級判定** - 決定任務執行順序
4. **串接規劃** - 規劃多 Agent 協作的順序

## 決策流程

```
用戶需求 → 任務分類 → Agent 匹配 → 優先級 → 輸出路由計畫
```

### 任務分類

| 類型 | 描述 | 範例 |
|------|------|------|
| build | 建構類任務 | 建立 Agent、建立 Skill、寫程式 |
| analyze | 分析類任務 | 數據分析、趨勢預測 |
| manage | 管理類任務 | 排程、提醒、日程 |
| research | 研究類任務 | 資訊收集、學習 |
| execute | 執行類任務 | 自動化操作、執行命令 |

### Agent 匹配

根據任務類型匹配 Agent：

- build → mcp-builder, skill-creator, agent-builder
- analyze → analytics-agent, knowledge-agent
- manage → lifeos-agent, reminder-agent
- research → knowledge-agent
- execute → workflow-orchestrator

### 優先級規則

1. **緊急** - 用戶明確標記緊急性
2. **依賴** - 有依賴關係的任務
3. **簡單** - 可快速完成的任務先做
4. **重要** - 根據任務價值判定

## 輸出格式

輸出應包含：
- `task_type`: 任務類型
- `target_agents`: 目標 Agent 清單（排序）
- `execution_order`: 執行順序
- `priority`: 優先級 (1-5)
- `estimated_steps`: 預估步驟數
