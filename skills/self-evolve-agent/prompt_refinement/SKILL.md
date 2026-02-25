---
name: prompt_refinement
description: Prompt 優化。當 Agent 的提示詞需要改進時觸發，診斷問題並產出優化版本。
metadata: { "openclaw": { "emoji": "✨" } }
---

# Prompt 優化

診斷 Agent 系統提示詞的問題，產出優化版本並追蹤效果。

## 操作 / 工作流程

1. **讀取現有 Prompt** — 從 agent 配置或 SKILL.md 中取得當前提示詞
2. **問題診斷** — LLM 從四個維度評估：
   - 清晰度：指令是否明確、有無歧義
   - 完整性：是否覆蓋所有情況、邊界條件
   - 一致性：風格統一、指令無矛盾
   - 精簡度：是否冗長、有無廢話
3. **優化改寫** — 依診斷結果改進：
   - 結構化：加入角色 / 任務 / 輸出格式 / 範例區塊
   - 清晰化：使用明確動詞，提供具體例子
   - 精簡化：移除冗餘，合併相似指令
4. **產出對比** — 並列顯示原始版與優化版的差異
5. **版本記錄** — 透過 `memory_search` 記錄優化歷史，追蹤效果

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| target | string | 必填 | 目標 agent 或 skill 名稱 |
| focus | string | "all" | 優化焦點：clarity / completeness / consistency / brevity / all |
| auto_apply | boolean | false | 是否自動套用優化結果 |

## 輸出格式

```
✨ Prompt 優化報告 — {target}

診斷結果：
- 清晰度：{clarity_score}/10
- 完整性：{completeness_score}/10
- 一致性：{consistency_score}/10
- 精簡度：{brevity_score}/10

主要問題：
{issues}

優化建議：
---原始---
{original_excerpt}
---優化---
{optimized_excerpt}

狀態：{applied / pending_review}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 目標不存在 | 列出可用 agent/skill，請用戶選擇 |
| Prompt 已經很好（全項 > 8） | 回報「無需優化」，提供微調建議 |
| 優化後變更過大 | 分階段建議，先改最關鍵的部分 |
| auto_apply 失敗 | 保留優化版本，提示手動套用 |

## 使用範例

- "優化一下 memory-agent 的 system prompt"
- "這個 SKILL.md 的描述寫得好不好"
- "讓 bni-agent 的回覆更簡潔一點"
