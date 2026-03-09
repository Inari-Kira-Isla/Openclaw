# 統一數據收集系統

## 目標
從 Agent Builder 和 Skill Creator 收集數據

## 數據來源

### Agent Builder
| 技能 | 權重 |
|------|------|
| 需求分析 | 1.5 |
| 身份設計 | 1.5 |
| 工作流程設計 | 1.5 |
| 技能清單 | 1.5 |
| 架構規劃 | 1.0 |

### Skill Creator
| 技能 | 權重 |
|------|------|
| 核心技能設計 | 1.5 |
| 輔助技能設計 | 1.5 |
| 專業領域設計 | 1.5 |
| 技能樹設計 | 1.5 |
| 熟練度系統 | 1.0 |

## 數據格式（統一）

```json
{
  "agent": "Agent_Builder",
  "skill": "需求分析",
  "timestamp": "ISO8601",
  "context": "場景描述",
  "success": true/false,
  "rating": 1-5,
  "duration_seconds": 數字
}
```

## 收集流程

```
1. 使用技能
   ↓
2. 記錄數據（JSON）
   ↓
3. 驗證格式
   ↓
4. 存入數據庫
   ↓
5. 統計分析
   ↓
6. 生成報告
```

## 數據存儲

```
/agents_data/
├── agent_builder/
│   ├── raw/
│   ├── cleaned/
│   └── reports/
├── skill_creator/
│   ├── raw/
│   ├── cleaned/
│   └── reports/
└── unified/
    └── analysis/
```

## 下一步

等待使用並收集數據！
