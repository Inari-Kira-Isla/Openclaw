---
name: skill_generator
description: 自動化技能生成。當需要根據需求自動生成完整的技能套件時觸發，包括：需求分析、模板選擇、內容生成、驗證檢查。
---

# Skill Generator

## 生成流程

```
需求輸入 → 分析與分類 → 選擇模板 → 生成內容 → 驗證輸出
```

## 需求分析

### 輸入格式
```json
{
  "name": "skill-name",
  "description": "技能描述",
  "category": "functionality|automation|analysis|management",
  "complexity": "simple|medium|complex",
  "required_features": ["feature1", "feature2"]
}
```

### 複雜度分類

| 等級 | 描述 | 預估時間 |
|------|------|----------|
| Simple | 單一功能 | 30分鐘 |
| Medium | 多功能整合 | 2小時 |
| Complex | 完整系統 | 4小時+ |

## 模板選擇

### 功能類
- API 整合
- 資料處理
- 檔案操作

### 自動化類
- 排程任務
- 流程觸發
- 狀態監控

### 分析類
- 數據分析
- 報告生成
- 趨勢預測

### 管理類
- 任務管理
- 提醒通知
- 庫存管理

## 輸出結構

```
skills/{skill-name}/
├── SKILL.md              # 主檔案
├── references/           # 參考文檔
│   └── guide.md
├── scripts/              # 腳本
│   └── main.py
└── assets/               # 資源
    └── template.json
```

## 驗證檢查

生成後自動檢查：
- [ ] YAML 語法正確
- [ ] name 符合規範
- [ ] description 完整
- [ ] 檔案結構正確
- [ ] 腳本語法正確
