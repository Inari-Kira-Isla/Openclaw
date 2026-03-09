---
name: auto_builder
description: 自動化建構。將生成的配置寫入系統、重啟服務並驗證 Agent 可用性。
metadata: { "openclaw": { "emoji": "🤖" } }
---

# 自動化建構

將 config_generator 產出的配置自動部署到系統中，包含備份、寫入、重啟與驗證。

## 操作 / 工作流程

1. **備份現有配置** — 複製當前 agents.yml 為 agents.yml.bak
2. **寫入配置** — 將新 agent 配置追加到 agents.yml
3. **建立技能目錄** — 在 workspace/skills/{agent}/ 下建立技能資料夾並寫入 SKILL.md
4. **重啟服務** — 執行 `openclaw gateway restart`
5. **驗證測試** — 檢查新 agent 狀態：
   - 服務是否正常運行
   - Agent 是否可回應
   - 技能是否正確載入
6. **狀態報告** — 回報建構結果

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| config | string | 必填 | 要部署的配置內容（YAML） |
| agent_name | string | 必填 | 新 agent 名稱 |
| dry_run | boolean | true | 預設為試運行，不實際寫入 |
| auto_rollback | boolean | true | 失敗時是否自動回滾 |

## 輸出格式

```
🤖 自動化建構報告
- Agent：{agent_name}
- 模式：{dry_run ? "試運行" : "正式部署"}

步驟狀態：
1. 備份配置：{status}
2. 寫入配置：{status}
3. 建立技能目錄：{status}
4. 重啟服務：{status}
5. 驗證測試：{status}

結果：{success / failed / rolled_back}
{if failed}回滾狀態：{rollback_status}{/if}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 備份失敗 | 終止流程，不進行任何寫入 |
| 配置寫入失敗 | 從備份還原，回報錯誤 |
| 重啟失敗 | 自動回滾配置，還原備份，用 `message` 通知 |
| 驗證未通過 | 回滾配置，列出失敗原因供排查 |
| 技能目錄已存在 | 詢問是否覆蓋，預設跳過 |

## 使用範例

- "把剛才的配置部署上去"
- "試運行一下，看看有沒有問題"
- "建構新的 BNI agent 並上線"
