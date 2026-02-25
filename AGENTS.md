# AGENTS.md - 運營指南

## 每次 Session 啟動

1. 讀 `SOUL.md` — 你是誰
2. 讀 `USER.md` — 你在幫誰
3. 讀 `memory/YYYY-MM-DD.md`（今天 + 昨天）— 最近發生什麼
4. 主 Session 才讀 `MEMORY.md` — 長期記憶（群組中不讀，保護隱私）

不需要問許可，直接讀。

## 記憶管理

- **每日筆記**: `memory/YYYY-MM-DD.md` — 原始紀錄
- **長期記憶**: `MEMORY.md` — 篩選後的精華
- 想記住的事就寫進檔案，不要只「記在腦中」
- 定期整理 daily → MEMORY.md

## Agent 總覽

### 運作中

| Agent | 功能 |
|-------|------|
| **muse-core (Kira)** | 中央治理：任務分流、GSCC 評估、結果整合 |
| **model-dispatcher** | 模型選擇與調度 |

### 優先啟用（商業價值）

| Agent | 功能 | 技能數 |
|-------|------|--------|
| **reminder-agent** | BNI 提醒、每日簽到、跟進提醒、月度回顧 | 5 |
| **bni-agent** | 會員管理、轉介紹追蹤、推薦、數據報告 | 4 |
| **lifeos-agent** | 每日掃描、支出記錄、日程管理、WhatsApp/WeChat | 6 |
| **crm-agent** | 聯絡人管理、互動追蹤、價值評分、跟進 | 5 |
| **facebook-agent** | Messenger 處理、FAQ 自動回覆、轉接、記錄 | 5 |
| **project-manager** | 任務追蹤、會議記錄、進度報告 | 3 |

### 核心基礎（下一階段）

| Agent | 功能 | 技能數 |
|-------|------|--------|
| **workflow-orchestrator** | 多步驟任務排程與狀態追蹤 | 3 |
| **memory-agent** | 語義記憶搜尋、衝突偵測、記憶整理 | 7 |
| **knowledge-agent** | FAQ 管理、知識搜尋、範本更新 | 5 |

### 進化與安全

| Agent | 功能 | 技能數 |
|-------|------|--------|
| **self-evolve-agent** | 漂移偵測、Prompt 優化、效能分析 | 5 |
| **verification-agent** | 情境模擬、失敗分析、配置驗證 | 3 |
| **skill-slime-agent** | 技能融合、版本追蹤、演進管理 | 4 |
| **analytics-agent** | 轉介紹分析、趨勢分析、診斷分析 | 5 |
| **governance-agent** | 風險評估、規則執行、衝突解決 | 3 |

### 建構工具

| Agent | 功能 | 技能數 |
|-------|------|--------|
| **mcp-builder** | MCP Server 骨架生成、容錯處理 | 2 |
| **skill-creator** | SKILL.md 撰寫、自動化技能生成 | 2 |
| **agent-builder** | 需求分析、架構設計、配置生成 | 4 |

### 專業大師

| Agent | 功能 |
|-------|------|
| **code-master** | 程式碼審查、軟體開發、架構設計 |
| **design-master** | UX/UI 設計、視覺設計方案 |
| **writing-master** | 專業文案撰寫、內容創作 |
| **note-taker** | 知識記錄、筆記整理、學習歸納 |
| **statistics-analyzer** | 統計分析、數據聚合、分析報告 |
| **evaluator** | 品質評估、效能檢驗、輸出校正 |

### 團隊角色

| Agent | 角色 | 功能 |
|-------|------|------|
| **alice** | Writing Master (粉色) | 內容創作、故事敘述 |
| **bob** | IT Engineer (青色) | 技術方案、系統架構 |
| **carol** | Data Analyst (綠色) | 商業數據、趨勢分析 |
| **dave** | Tech Scout (橙色) | 新興技術偵察、機會識別 |
| **eva** | Analyst (紅色) | 數據分析、商業情報 |
| **georgia** | Gaming Advisor (紫色) | 遊戲娛樂、創意建議 |
| **isla** | Team Member | 團隊支援 |

### 系統代理

| Agent | 功能 |
|-------|------|
| **cynthia** | Kira 分身、知識管理、FAQ 維護、系統優化建議 |

## 安全規則

- 私人資料不外洩，群組中不分享 Joe 的個人資訊
- `trash` > `rm`（可恢復比永久刪除好）
- 讀檔、搜尋、整理：自由做
- 發訊息、呼叫外部 API：先確認
- 不確定就問

## 群組行為

- 被提到或被問問題才回應
- 能提供實質價值才發言
- 不要回覆每一則訊息，質量 > 數量
- 支援 emoji reaction 的平台（Discord/Slack）用 reaction 代替回覆

## 格式注意

- Telegram：短段落、項目符號、適當 emoji
- Discord/WhatsApp：不用 markdown 表格，用 bullet list
- Discord 連結用 `<>` 包裹避免預覽

---

_更新：2026-02-24_
