---
name: config_generator
description: 配置生成。根據架構設計產出 agents.yml 配置片段與 SKILL.md 檔案。
metadata: { "openclaw": { "emoji": "⚙️" } }
---

# 配置生成

根據架構設計結果，生成可直接使用的 YAML 配置與 SKILL.md 檔案。

## 操作 / 工作流程

1. **接收設計** — 取得 architecture_designer 的輸出
2. **生成 agents.yml 片段** — 產出標準格式的 YAML 配置：
   - name / role / model / temperature / max_tokens
   - system_prompt（完整版）
   - skills 清單
   - constraints
3. **生成 SKILL.md** — 為每個新技能產出標準 SKILL.md：
   - YAML frontmatter（name, description, metadata with emoji）
   - 操作流程、參數表、輸出格式、錯誤處理、使用範例
4. **驗證檢查** — 確保配置正確：
   - YAML 語法驗證
   - 技能路徑存在性檢查
   - 模型名稱有效性
   - 必填欄位完整性
5. **預覽輸出** — 顯示完整配置供用戶確認

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| design | string | 必填 | 架構設計內容 |
| output_format | string | "preview" | 輸出模式：preview / write |
| config_path | string | "~/.openclaw/agents.yml" | 配置檔路徑 |

## 輸出格式

```
⚙️ 配置生成完成

agents.yml 片段：
```yaml
  {agent_name}:
    role: {role}
    model: {model}
    temperature: {temperature}
    system_prompt: |
      {system_prompt}
    skills:
      - {skill_1}
      - {skill_2}
```

新技能檔案：
- {skill_path_1}/SKILL.md
- {skill_path_2}/SKILL.md

驗證結果：
- YAML 語法：通過
- 技能路徑：通過
- 必填欄位：通過

狀態：{preview / written}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| YAML 語法錯誤 | 自動修正並標記修正處 |
| 技能路徑不存在 | 提示需要先建立技能目錄 |
| 模型名稱無效 | 列出可用模型，請用戶選擇 |
| 配置檔寫入失敗 | 輸出配置內容到回覆中，請用戶手動貼入 |

## 使用範例

- "幫 BNI agent 生成配置"
- "產出這個設計的 YAML"
- "生成新技能的 SKILL.md"
