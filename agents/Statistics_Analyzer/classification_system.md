# 數據分類系統

## 分類目標
建立乾淨有用的數據資產

## 分類結構

```
/data/
├── raw/                    # 原始數據（未處理）
│   ├── agent_builder/
│   └── skill_creator/
│
├── cleaned/                # 清理後數據
│   ├── agent_builder/
│   └── skill_creator/
│
├── aggregated/            # 聚合數據
│   ├── usage_stats/
│   ├── skill_stats/
│   └── report_stats/
│
├── processed/             # 處理後數據
│   ├── analysis/
│   └── insights/
│
└── reports/              # 報告輸出
    ├── daily/
    ├── weekly/
    └── monthly/
```

## 數據類型定義

### 1. 原始數據 (Raw)
```
{
  "agent": "Agent_Builder",
  "skill": "需求分析",
  "timestamp": "ISO8601",
  "context": "string",
  "success": boolean,
  "rating": number,
  "duration": number
}
```

### 2. 清理數據 (Cleaned)
- 移除無效數據
- 標準化格式
- 驗證完整性

### 3. 聚合數據 (Aggregated)
- 使用次數統計
- 成功率統計
- 滿意度統計

### 4. 分析數據 (Analyzed)
- 趨勢分析
- 異常檢測
- 優化建議

## 分類標籤

| 標籤 | 說明 | 範例 |
|------|------|------|
| agent | Agent 名稱 | Agent_Builder |
| skill | 技能名稱 | 需求分析 |
| context | 應用場景 | 新Agent設計 |
| success | 是否成功 | true/false |
| rating | 滿意度 | 1-5 |
| timestamp | 時間戳 | ISO8601 |

## 數據質量標準

### 完整性
- 所有必填欄位都有值
- 無缺失數據

### 一致性
- 格式統一
- 命名一致
- 時間格式標準

### 準確性
- 數值在合理範圍
- 邏輯正確

### 時效性
- 及時記錄
- 按時更新

## 下一步
1. 建立數據庫結構
2. 設定自動化分類
3. 定期質量檢查
