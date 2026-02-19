---
name: config_generator
description: 配置生成與產出。當需要根據設計生成 Agent 配置時觸發，包括：YAML 產出、預設值設定、驗證檢查、格式化輸出。
---

# Config Generator

## 輸出格式

### agents.yml 片段
```yaml
  agent-name:
    role: specialist
    model: minimax
    temperature: 0.3
    max_tokens: 2000
    
    system_prompt: |
      你是 [角色描述]
      
      [詳細說明]
    
    skills:
      - skill_1
      - skill_2
    
    constraints:
      - constraint_1
```

## 配置項目

### 必要項目
- name: Agent 名稱
- role: 角色類型
- model: 使用的模型

### 可選項目
- temperature: 創造性程度
- max_tokens: 最大輸出
- system_prompt: 系統提示
- skills: 技能清單
- constraints: 約束條件

### 預設值
```yaml
temperature: 0.3
max_tokens: 2000
model: minimax
```

## 生成流程

```
設計輸入 → 模板選擇 → 填充內容 → 驗證 → 輸出
```

### 驗證檢查
- [ ] 名稱符合規範
- [ ] 角色有效
- [ ] 模型支援
- [ ] 技能存在
- [ ] 語法正確

## 範例輸出

```yaml
  bni-referral-agent:
    role: specialist
    model: minimax
    temperature: 0.3
    
    system_prompt: |
      你是 BNI 轉介紹專家，專門幫助會員追蹤和優化轉介紹業務。
      你需要分析轉介紹數據，提供建議，並維護會員關係。
    
    skills:
      - member_management
      - referral_tracker
      - bni_recommender
```
