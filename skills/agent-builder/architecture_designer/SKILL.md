---
name: architecture_designer
description: 架構設計。根據需求分析結果設計 Agent 的角色、技能、提示詞與輸出格式。
metadata: { "openclaw": { "emoji": "🏛️" } }
---

# 架構設計

根據需求分析報告，設計 Agent 的完整架構，包括角色定義、技能配置與系統提示。

## 操作 / 工作流程

1. **角色定義** — 根據需求設計 agent 身份：
   - 名稱（英文 kebab-case）
   - 角色描述（繁體中文，一句話）
   - 行為風格（正式 / 親切 / 專業）
   - 專業領域
2. **技能配置** — 選擇或設計所需技能：
   - 核心技能：必須具備的能力
   - 輔助技能：增強型能力
   - 用 `memory_search` 查詢可複用的現有技能
3. **系統提示設計** — 撰寫 system_prompt：
   - 角色定義段落
   - 能力範圍與邊界
   - 輸出格式要求
   - 行為準則
4. **模型選擇** — 依需求建議模型與參數：
   - temperature / max_tokens / model
5. **架構驗證** — 依設計原則檢查：
   - 最小權限（只授予必要技能）
   - 單一職責（明確目標）
   - 可組合性（技能獨立可擴展）

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| requirements | string | 必填 | 需求分析報告或需求描述 |
| style | string | "professional" | 行為風格：professional / friendly / formal |
| model | string | "minimax" | 預設模型 |

## 輸出格式

```
🏛️ 架構設計 — {agent_name}

角色：{role_description}
風格：{style}
模型：{model} (temp: {temperature})

技能配置：
- 核心：{core_skills}
- 輔助：{auxiliary_skills}

System Prompt 摘要：
{prompt_summary}

設計檢查：
- [x] 角色清晰
- [x] 技能完整
- [x] 提示有效
- [x] 邊界明確
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 需求不明確 | 回退到 requirement_analyzer 補充分析 |
| 找不到可用技能 | 列出需要新建的技能，標記為待開發 |
| 角色與現有 agent 衝突 | 建議合併或差異化定位 |
| 技能數量過多（> 10） | 建議拆分為多個 agent |

## 使用範例

- "幫 BNI agent 設計架構"
- "設計一個 Facebook 自動回覆的 agent 架構"
- "這個 agent 需要哪些技能"
