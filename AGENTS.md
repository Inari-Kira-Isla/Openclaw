# AGENTS.md - Agent 架構

## 版本資訊
- **版本**: 2.0
- **架構**: Workflow-driven
- **模型策略**: minimax-only

---

## 📊 Agent 總覽

| # | Agent ID | 名稱 | 類型 | 狀態 |
|---|----------|------|------|------|
| 0 | muse-core | 中央治理核心 | core | ✅ 運作中 |
| 12 | model-dispatcher | 模型調度員 | dispatcher | ✅ 新建立 |
| 1 | workflow-orchestrator | 工作流協調器 | planner | ⏳ 待設定 |
| 2 | mcp-builder | MCP 構建器 | builder | ⏳ 待設定 |
| 3 | skill-creator | 技能創建器 | author | ⏳ 待設定 |
| 4 | verification-agent | 驗證代理 | verifier | ⏳ 待設定 |
| 5 | memory-agent | 記憶代理 | archivist | ⏳ 待設定 |
| 6 | skill-slime-agent | 技能史萊姆 | evolver | ⏳ 待設定 |
| 7 | self-evolve-agent | 自我進化代理 | optimizer | ⏳ 待設定 |
| 8 | analytics-agent | 分析師 | analyst | ⏳ 待設定 |
| 9 | knowledge-agent | 知識庫管理 | librarian | ⏳ 待設定 |
| 10 | governance-agent | 治理代理 | judge | ⏳ 待設定 |
| 11 | lifeos-agent | 生活 OS | assistant | ⏳ 待設定 |

---

## 🏛️ 核心層（Core Layer）

### muse-core（中央治理核心）
- **狀態**: ✅ 運作中
- **角色**: manager
- **模型**: minimax
- **功能**: 任務拆解、Workflow 指派、GSCC 判定、最終裁決

---

## 📋 Agent 類型說明

| 類型 | 說明 | 範例 |
|------|------|------|
| **core** | 中央治理核心 | muse-core |
| **planner** | 規劃與協調 | workflow-orchestrator |
| **builder** | 構建與開發 | mcp-builder, skill-creator |
| **assistant** | 輔助工具 | lifeos-agent |
| **archivist** | 記憶管理 | memory-agent |
| **evolver** | 進化優化 | skill-slime-agent, self-evolve-agent |
| **judge** | 治理裁決 | governance-agent |
| **analyst** | 數據分析 | analytics-agent |
| **librarian** | 知識管理 | knowledge-agent |

---

## 🔄 系統優化流程

### 收到新資料時的處理流程

1. **分析內容** → 評估系統優化點
2. **應用優化** → 更新 Agent/Skill/Workflow
3. **生成筆記** → 記錄到 Notion

### 相關檔案
- `/system/提示詞資料庫.md`
- `/system/系統優化工作流.md`

---

## 🔄 設定狀態

- Workspace SOUL.md: ✅ 已更新為 muse-core
- Sub-agents: ✅ 主要 agents 已建立
- 技能: ✅ 向量摘要標準流程已建立

---

## 📊 最新成就 (2026-02-19)

- 11萬檔案整理里程碑
- 50頁 Notion 筆記向量優化
- Ollama + MiniMax 混合系統

---

_Last Updated: 2026-02-19_
