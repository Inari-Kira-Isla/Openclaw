# OpenClaw 生態系介紹 - Claude Code 整合指南

> 這份文件幫助 Claude Code 理解 OpenClaw 平台架構，以便進行系統優化與 ACP Agent 整合。

---

## 系統總覽

### 核心定位
- **OpenClaw**: 自架 AI 助理平台（類似 Claude Desktop but self-hosted）
- **主要功能**: 多 Bot 協作、任務分流、記憶管理、自動化工作流
- **執行環境**: macOS (Kira's iMac), Node.js v25.6.0, OpenClaw Gateway (localhost:18789)

### 技術堆疊
| 層面 | 技術 |
|------|------|
| 訊息通道 | Telegram, WhatsApp, Discord, Signal |
| AI 模型 | MiniMax-M2.5 (主要), Ollama (本地) |
| 向量搜尋 | SQLite-VEC (本地向量庫) |
| 資料儲存 | Notion, Memory Files, SQLite |
| 自動化 | n8n, Cron Jobs, Heartbeat |

---

## 3 系統生態系架構

### 1. 記憶層 (Memory Layer)
```
Kira (中央治理) ─┬─ Cynthia (知識庫守護者)
                └─ 職責：知識查詢、FAQ 管理、向量搜尋
```
- **Cynthia**: 維護知識庫、FAQ、向量化筆記
- **Kira**: 中央協調、任務分流、決策制定

### 2. 學習機制 (Learning Engine)
```
Slime (史萊姆)
├─ Prompt 優化 (prompt_refinement)
├─ 漂移偵測 (drift_detection)
└─ 效能分析 (performance_analysis)
```
- 持續學習、系統自我優化
- 每日學習趨勢、AI Agents 動態

### 3. 進化引擎 (Evolution Engine)
```
Team (任務執行) ─┬─ 任務排程、狀態追蹤
                │
Evolution (技能進化者)
                └─ 技能融合、版本控制、風險評估
```
- 技能封裝與版本管理
- MCP/Skill 架構設計

---

## 5 Bot 團隊

| Bot | Telegram | 角色 | 模型 |
|-----|----------|------|------|
| **Kira** | @KiraIsla_bot | 中央治理、方案提出 | MiniMax-M2.5 |
| **Nei** | @Neicheok_bot | 決策審視、最終裁決 | Claude 4.5 |
| **Cynthia** | @CynthiaChoi_bot | 知識庫守護者 | MiniMax-M2.5 |
| **史萊姆** | @Joejoebaby_bot | 持續學習優化 | MiniMax-M2.5 |
| **Team** | @Inarijoe_bot | 任務排程執行 | MiniMax-M2.5 |

### 決策流程
```
User Request → Kira (提出方案) → Nei (裁決) → Team (執行)
                                            ↑
                                      Evolution (上訴)
```

---

## OpenClaw 核心能力

### 可用工具
- **訊息**: telegram, whatsapp, discord 發送/回覆
- **瀏覽器**: 網頁自動化 (Playwright)
- **檔案**: 讀寫編輯 local files
- **執行**: shell commands, sub-agents 管理
- **向量**: 本地向量搜尋 (sqlite-vec)
- **記憶**: memory_search, memory_get

### Skill 架構 (40+ Skills)
Skills 位於 `~/.openclaw/workspace/skills/`

| 類別 | Skills |
|------|--------|
| 知識管理 | knowledge_search, faq_management, knowledge_updater |
| 自我進化 | prompt_refinement, drift_detection, performance_analysis |
| 工作流 | workflow_orchestrator, task_scheduling, state_control |
| 自動化 | n8n-workflow-automation, social_media_automation |

---

## ACP Agent 整合目標

### 當前挑戰
1. **多 Bot 協作效率**: 5 Bot 之間的溝通與任務分配
2. **決策品質**: Nei 裁決的準確性與一致性
3. **學習閉環**: 史萊姆的優化建議如何實際落地
4. **技能進化**: Evolution 如何自動創建/更新 Skills

### 期望方向
- [ ] ACP Agent 作為「超級大腦」支援決策
- [ ] Claude Code 理解系統架構後提出優化方案
- [ ] 自動化技能生成與測試
- [ ] 多模型協作 (MiniMax + Claude + Ollama)

---

## 關鍵檔案位置

| 檔案 | 用途 |
|------|------|
| `~/.openclaw/workspace/AGENTS.md` | 5 Bot 完整架構 |
| `~/.openclaw/workspace/SOUL.md` | Kira 核心角色定義 |
| `~/.openclaw/workspace/MEMORY.md` | 知識庫索引 |
| `~/.openclaw/workspace/USER.md` | Joe 個人資料與偏好 |
| `~/.openclaw/openclaw.json` | OpenClaw 設定 |

---

## 歡迎 Claude Code

> 如果你需要了解任何具體模組、查看程式碼、或測試假設，請告訴我。

期待你的優化建議！ 🚀

---

*Created: 2026-03-01*
