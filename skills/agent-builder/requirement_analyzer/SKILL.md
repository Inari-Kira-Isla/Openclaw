---
name: requirement_analyzer
description: 需求分析。當用戶要建立新 Agent 時觸發，分析需求並評估可行性。
metadata: { "openclaw": { "emoji": "🎯" } }
---

# 需求分析

分析用戶對新 Agent 的需求，提取功能點、評估複雜度並排定優先級。

## 操作 / 工作流程

1. **需求收集** — 從用戶描述中提取需求：
   - 用 LLM 解析自然語言描述
   - 分類為功能需求 / 非功能需求 / 約束條件
2. **現有能力比對** — 用 `memory_search` 搜尋現有 agent 與 skill：
   - 是否已有類似 agent
   - 哪些現有技能可以複用
3. **複雜度評估** — 依維度評分：
   - 功能數量：1-3（低）/ 4-6（中）/ 7+（高）
   - 整合需求：無（低）/ 簡單（中）/ 複雜（高）
   - 外部依賴：無（低）/ 少（中）/ 多（高）
4. **可行性分析** — 評估技術限制、資源需求、時間估算
5. **產出需求文檔** — 結構化需求清單 + 優先級排序

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| description | string | 必填 | 用戶的 agent 需求描述 |
| priority_focus | string | "balanced" | 優先級偏好：speed / quality / balanced |

## 輸出格式

```
🎯 需求分析報告

功能需求：
{foreach requirement}
  [{priority}] {description}
{/foreach}

非功能需求：{non_functional}
約束條件：{constraints}

複雜度：{complexity}（{complexity_detail}）
預估工時：{estimated_effort}
可複用技能：{reusable_skills}
風險：{risks}
待釐清：{clarifications_needed}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 需求描述模糊 | 用 `message` 向用戶提出釐清問題 |
| 需求過於龐大 | 建議拆分為多個 agent，分階段實現 |
| 技術不可行 | 明確指出限制，建議替代方案 |
| 已有相同 agent | 提示現有 agent，建議擴展而非新建 |

## 使用範例

- "我想建一個專門追蹤 BNI 轉介紹的 agent"
- "幫我設計一個能自動回覆 Facebook 訊息的 agent"
- "需要一個每天自動整理 Notion 的 agent"
