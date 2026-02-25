---
name: version_tracking
description: 版本追蹤。追蹤技能的版本變更歷史與相容性。
metadata: { "openclaw": { "emoji": "📋" } }
---

# 版本追蹤

管理技能的版本號、變更記錄與相容性追蹤。

## 操作 / 工作流程

1. **版本偵測** — 讀取技能 SKILL.md 的 frontmatter，檢查當前版本
2. **變更比對** — 與上一版本比較，由 LLM 分析差異：
   - 新增功能
   - 修改行為
   - 移除功能
   - API 變更
3. **版本號建議** — 依語義化版本規則建議新版號：
   - Patch（x.x.+1）：修復問題，無行為變更
   - Minor（x.+1.0）：新增功能，向後相容
   - Major（+1.0.0）：破壞性變更，不相容
4. **更新記錄** — 在 `memory_search` 中記錄版本歷史
5. **相容性標記** — 標記與其他技能的相容性狀態

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| skill_name | string | 必填 | 技能名稱 |
| action | string | "check" | 動作：check / bump / history |
| bump_type | string | "patch" | 版本升級類型：patch / minor / major |
| changelog | string | "" | 變更說明 |

## 輸出格式

```
📋 版本追蹤
- 技能：{skill_name}
- 當前版本：{current_version}
- 上次更新：{last_updated}

{if action == "history"}
變更歷史：
{foreach version}
  [{version}] {date} — {summary}
{/foreach}
{/if}

{if action == "bump"}
版本升級：{old_version} → {new_version}
變更：{changelog}
{/if}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 技能無版本資訊 | 初始化為 v1.0.0 |
| 版本號格式錯誤 | 自動修正為語義化版本格式 |
| 變更歷史遺失 | 從 memory_search 嘗試恢復，無則從當前版本重建 |
| 相容性無法判定 | 標記為「未驗證」，建議手動測試 |

## 使用範例

- "查一下 semantic_ingest 的版本歷史"
- "把 conflict_detection 升級到新版本"
- "這次改動算 minor 還是 major"
