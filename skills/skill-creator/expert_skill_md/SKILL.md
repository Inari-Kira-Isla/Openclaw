---
name: expert_skill_md
description: 專家級 SKILL.md 撰寫。當需要撰寫或優化技能說明文件時觸發。
metadata: { "openclaw": { "emoji": "✍️" } }
---

# SKILL.md 撰寫

撰寫符合 OpenClaw 規範的高品質 SKILL.md 技能說明文件。

## 操作 / 工作流程

1. **需求釐清** — 確認技能名稱、功能、觸發條件、使用工具
2. **結構設計** — 依標準模板規劃各章節：
   - YAML Frontmatter（name / description / metadata）
   - 一句話說明 + 操作流程 + 參數 + 輸出格式 + 錯誤處理 + 使用範例
3. **內容撰寫** — 遵循撰寫原則：
   - 繁體中文，簡潔明確，每句話都有價值
   - description 格式：`一句話描述。觸發條件。`
   - 操作流程具體告訴 LLM 用什麼工具、怎麼做
   - 目標 30-60 行
4. **品質檢查** — 使用檢查清單驗證：
   - [ ] name 小寫底線命名
   - [ ] description 含觸發條件
   - [ ] metadata 含 emoji
   - [ ] 操作流程提及具體工具
   - [ ] 有錯誤處理表格
   - [ ] 有使用範例（2-3 句）
   - [ ] Markdown 格式正確
5. **寫入檔案** — 寫入對應的 SKILL.md 路徑

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| skill_name | string | — | 技能名稱 |
| skill_path | string | — | SKILL.md 檔案路徑 |
| description | string | — | 功能描述 |
| tools | array | [] | 使用的工具列表 |
| emoji | string | — | 技能代表 emoji |

## 輸出格式

```
✍️ SKILL.md 已撰寫完成
技能：[skill_name]
路徑：[skill_path]
行數：[N] 行
品質檢查：全部通過 ✅
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 缺少必要資訊 | 列出缺少的欄位，詢問用戶 |
| 檔案路徑不存在 | 建議正確路徑或建立目錄 |
| 內容超過 60 行 | 精簡內容，移除冗餘 |
| YAML 語法錯誤 | 自動修正並提示 |

## 使用範例

- "幫我寫一個新技能的 SKILL.md"
- "優化這個 SKILL.md 的品質"
- "檢查這份 SKILL.md 是否符合規範"
