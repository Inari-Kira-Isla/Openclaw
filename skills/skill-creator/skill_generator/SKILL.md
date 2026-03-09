---
name: skill_generator
description: 自動化技能生成。當需要根據需求自動生成完整技能套件（目錄結構 + SKILL.md + 相關檔案）時觸發。
metadata: { "openclaw": { "emoji": "⚡" } }
---

# 自動化技能生成

根據需求描述自動生成完整的技能套件，包含目錄結構、SKILL.md 與相關檔案。

## 操作 / 工作流程

1. **需求分析** — 解析用戶需求，判斷技能分類與複雜度：
   | 複雜度 | 描述 | 產出 |
   |--------|------|------|
   | simple | 單一功能 | SKILL.md |
   | medium | 多功能整合 | SKILL.md + 參考文檔 |
   | complex | 完整系統 | SKILL.md + 子技能 + 腳本 |
2. **模板選擇** — 依分類選擇模板（功能類 / 自動化類 / 分析類 / 管理類）
3. **目錄建立** — 在 `~/.openclaw/workspace/skills/` 下建立：
   ```
   skills/{agent-name}/{skill-name}/
   ├── SKILL.md
   ├── references/      # 參考文檔（選配）
   └── scripts/         # 腳本（選配）
   ```
4. **內容生成** — 呼叫 `expert_skill_md` 撰寫 SKILL.md
5. **驗證檢查** — 確認 YAML 語法正確、name 符合規範、description 完整、檔案結構正確

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| name | string | — | 技能名稱（小寫、底線分隔） |
| description | string | — | 功能描述 |
| agent | string | — | 所屬 agent 名稱 |
| category | string | functionality | functionality / automation / analysis / management |
| complexity | string | simple | simple / medium / complex |

## 輸出格式

```
⚡ 技能已生成
名稱：[skill_name]
路徑：skills/[agent]/[skill_name]/
分類：[category]
複雜度：[complexity]
檔案數：[N] 個
驗證：全部通過 ✅
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 技能名稱已存在 | 詢問是否覆蓋或使用新名稱 |
| Agent 不存在 | 列出可用 agent，請用戶選擇 |
| 驗證失敗 | 列出失敗項目，自動修正後重新驗證 |
| 需求描述不明確 | 提出具體問題引導用戶補充 |

## 使用範例

- "幫我建立一個新的提醒技能"
- "生成一個本地資料庫整合的技能套件"
- "自動產生這個功能的完整技能結構"
