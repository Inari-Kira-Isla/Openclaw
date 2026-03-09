---
name: skill_ingestion
description: 技能攝入學習。當需要學習外部技能或整合新 SKILL.md 到系統時觸發。
metadata: { "openclaw": { "emoji": "📚" } }
---

# 技能攝入學習

發現、評估並整合外部技能到 OpenClaw 系統。

## 操作 / 工作流程

1. **來源發現** — 從以下管道尋找技能：
   - workspace/skills/ 目錄掃描
   - 用戶手動提供 SKILL.md
   - 從參考文檔中提取技能定義
2. **分析評估** — LLM 分析技能內容：
   - 功能是否符合需求
   - 與現有技能是否重疊（呼叫 `memory_search` 查詢已有技能）
   - 品質評估（結構完整性、指令清晰度）
3. **轉換適配** — 確保格式符合標準 SKILL.md 模板：
   - 補齊 YAML frontmatter（name, description, metadata）
   - 補齊缺失段落（錯誤處理、使用範例）
   - 路徑與依賴調整
4. **配置更新** — 將技能加入對應 agent 的設定
5. **驗證測試** — 模擬觸發測試技能是否正常運作

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| source | string | 必填 | 技能來源（檔案路徑 / URL / 文本內容） |
| target_agent | string | "" | 目標 agent 名稱，空則自動建議 |
| auto_install | boolean | false | 是否自動安裝（否則僅預覽） |

## 輸出格式

```
📚 技能攝入報告
- 技能名稱：{skill_name}
- 來源：{source}
- 品質評分：{quality_score}/10
- 重疊技能：{overlapping_skills}
- 建議 Agent：{suggested_agent}
- 狀態：{installed / preview}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 來源無法存取 | 回報來源錯誤，請用戶確認路徑 |
| SKILL.md 格式不合規 | 自動修正格式，列出修正項目 |
| 與現有技能高度重疊（> 80%） | 建議使用 fusion_proposal 合併 |
| 目標 agent 不存在 | 列出可用 agent，請用戶選擇 |

## 使用範例

- "學習這個新技能：{SKILL.md 內容}"
- "把這個檔案的技能加到 memory-agent"
- "評估一下這個技能適不適合用"
