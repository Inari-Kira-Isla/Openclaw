---
name: config_validation
description: 配置驗證與檢查。當需要驗證 agents.yml、SKILL.md 或其他系統配置是否正確時觸發。
metadata: { "openclaw": { "emoji": "✅" } }
---

# 配置驗證

驗證系統配置檔的語法、完整性、權限與一致性，確保系統正常運作。

## 操作 / 工作流程

1. **語法檢查** — 驗證 JSON/YAML 語法正確，必要欄位存在，型別正確
2. **依賴檢查** — 確認引用的套件已安裝、版本相容、無循環依賴
3. **權限檢查** — 確認檔案可讀寫、API Key 有效、路徑存在
4. **一致性檢查** — 配置項邏輯一致、與環境變數匹配、預設值合理
5. **產出報告** — 列出所有錯誤與警告，依嚴重程度排序

### 驗證清單

**agents.yml：**
- version 欄位存在
- 每個 agent 有 name、role、model
- skills 陣列存在且引用的技能路徑有效

**SKILL.md：**
- YAML frontmatter 語法正確
- name 符合命名規範（小寫、底線）
- description 不為空且含觸發條件
- metadata 含 emoji

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| target | string | all | 驗證目標：all / agents / skills / specific 路徑 |
| fix_auto | boolean | false | 是否自動修正可修復的問題 |
| severity_filter | string | all | 過濾層級：error / warning / all |

## 輸出格式

```
✅ 配置驗證報告
目標：[驗證目標]
結果：[通過 / 有問題]

❌ 錯誤 ([N] 個)：
1. [檔案:行號] [錯誤描述]

⚠️ 警告 ([M] 個)：
1. [檔案:行號] [警告描述]
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 配置檔不存在 | 回報缺失檔案，建議建立 |
| YAML 語法錯誤 | 標出錯誤行號，若 fix_auto=true 嘗試修正 |
| API Key 無效 | 標記為 error，提示重新設定 |
| 引用的技能不存在 | 列出無效引用，建議移除或建立 |

## 使用範例

- "檢查一下所有配置是否正確"
- "驗證 agents.yml"
- "自動修正配置問題"
