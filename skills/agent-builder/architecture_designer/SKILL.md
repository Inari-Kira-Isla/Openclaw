---
name: architecture_designer
description: Agent 架構設計。當需要設計 Agent 的整體架構時觸發，包括：角色定義、技能配置、系統提示、輸出格式。
---

# Architecture Designer

## 設計維度

### 1. 角色定義
- 角色名稱
- 角色描述
- 行為風格
- 專業領域

### 2. 技能配置
- 核心技能
- 輔助技能
- 備用技能

### 3. 系統提示
- 背景上下文
- 能力邊界
- 輸出要求

### 4. 輸出格式
- 格式規範
- 範例展示
- 錯誤處理

## 設計模板

```yaml
agent:
  name: "agent-name"
  role: "角色類型"
  model: "minimax"
  temperature: 0.3
  
  system_prompt: |
    # 角色定義
    你是...
    
    # 能力範圍
    你可以...
    
    # 輸出格式
    請以...格式輸出
  
  skills:
    - core_skill_1
    - core_skill_2
    - auxiliary_skill
  
  constraints:
    - "限制1"
    - "限制2"
```

## 設計原則

### 1. 最小權限
- 只授予必要技能
- 明確邊界

### 2. 清晰職責
- 單一職責
- 明確目標

### 3. 可組合性
- 技能獨立
- 易于擴展

## 檢查清單
- [ ] 角色清晰
- [ ] 技能完整
- [ ] 提示有效
- [ ] 格式規範
- [ ] 邊界明確
