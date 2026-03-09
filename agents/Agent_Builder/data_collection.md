# Agent Builder - 數據收集

## 收集的數據

### 技能列表
| 技能 | 類型 | 權重 |
|------|------|------|
| 需求分析 | 核心 | 1.5 |
| 身份設計 | 核心 | 1.5 |
| 工作流程設計 | 核心 | 1.5 |
| 技能清單 | 核心 | 1.5 |
| 架構規劃 | 輔助 | 1.0 |
| 整合測試 | 輔助 | 1.0 |

## 數據格式

```json
{
  "agent": "Agent_Builder",
  "skill": "需求分析",
  "timestamp": "2026-02-16T18:30:00Z",
  "context": "新Agent設計",
  "success": true,
  "rating": 5,
  "duration_seconds": 300
}
```

## 數據流向
```
Agent_Builder → 使用記錄 → Statistics_Analyzer
                    ↓
               數據分析
                    ↓
               熟練度計算
                    ↓
               優化建議
```

## 追蹤的指標
- 使用次數
- 成功率
- 用戶滿意度
- 完成時間
