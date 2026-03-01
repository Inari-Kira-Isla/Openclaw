# AGENTS.md - 5 Bot 完整架構

## Bot 總覽

| Bot | Telegram | 團隊 | SOUL | Workflow | Skill | Tool | Model |
|-----|----------|------|------|----------|-------|------|-------|
| **Nei** | @Neicheok_bot | 雙核心 | 決策審視者 | 審視→質疑→建議 | gscc_classifier, result_integrator | Claude API | Claude 4.5 |
| **Kira** | @KiraIsla_bot | 記憶層 | 中央治理 | 任務分流→整合回覆 | memory_search, gscc_classifier | Telegram, Notion | MiniMax-M2.5 |
| **Cynthia** | @CynthiaChoi_bot | 記憶層 | 知識庫守護者 | 查詢→回覆→更新知識庫 | knowledge_search, faq_management | Notion, SQLite-Vec | MiniMax-M2.5 |
| **史萊姆** | @Joejoebaby_bot | 學習機制 | 持續學習優化 | 學習→優化→驗證→報告 | prompt_refinement, drift_detection | OpenClaw 工具 | MiniMax-M2.5 |
| **Team** | @Inarijoe_bot | 進化引擎 | 工作流協調者 | 接收→排程→執行→回報 | task_scheduling, state_control | Cron, Heartbeat | MiniMax-M2.5 |
| **Evolution** | @GodKiraCheok_bot | 進化引擎 | 技能進化者 | 評估→融合→版本控制→發布 | skill-creator, workflow_improvement | Skills 資料夾 | MiniMax-M2.5 |

---

## 雙核心制 (2026-03-01)

```
         ┌─────────────┐
         │   User      │
         │   Request   │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │    Kira     │ ◄── 方案提出 (MiniMax)
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │    Nei      │ ◄── 裁決 (Claude 4.5)
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │  Evolution  │ ◄── 上訴裁決
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │    Team     │ ◄── 執行
         └─────────────┘
```

### 決策流程

1. **Kira** 收到需求 → 分析 → 提出方案
2. **Nei** 審視方案 → 最終裁決
3. **Team** 執行決策

### 裁決規則

| 情況 | 處理方式 |
|------|----------|
| Nei 同意 | 執行 |
| Nei 否決 | 重新提案或上訴 |
| 上訴 | Evolution 裁決 |
| 重大分歧 | Joe 裁決 |

### 時限與制約

| 項目 | 規則 |
|------|------|
| Nei 回覆時限 | 60 秒內 |
| 若 Nei 無回覆 | Kira 可直接執行 |
| 上訴次數 | 最多 2 次 |

---

## 團隊分工

### 記憶層 (Memory Layer)
```
Kira (@KiraIsla_bot) ─┬─ Cynthia (@CynthiaChoi_bot)
                      │    └─ 知識庫管理、FAQ、向量搜尋
                      │
                      └─ 中央治理、決策分流
```

### 學習機制 (Learning Engine)
```
史萊姆 (@Joejoebaby_bot)
    ├─ Prompt 優化
    ├─ 漂移偵測
    └─ 效能分析
```

### 進化引擎 (Evolution Engine)
```
Team (@Inarijoe_bot) ─┬─ 任務排程、狀態追蹤
                      │
Evolution (@GodKiraCheok_bot)
    └─ 技能融合、版本控制、風險評估
```

---

## 協作流程

```
                    ┌─────────────┐
                    │   User      │
                    │   Request   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Kira     │ ◄── 中央治理
                    │  (分流決策)  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼─────┐    ┌─────▼─────┐
    │ Cynthia │      │  史萊姆   │    │   Team    │
    │ (記憶層) │      │(學習機制) │    │(進化-協作)│
    └────┬────┘      └─────┬─────┘    └─────┬─────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Evolution  │ ◄── 技能進化
                    │(進化-進化)  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  整合回覆    │
                    └─────────────┘
```

---

## Workspace 配置

```
~/.openclaw/workspace/
├── BOT_SETUP.md      ← 5 Bot 完整設定
├── SOUL.md           ← Kira 靈魂
├── AGENTS.md         ← 團隊架構
├── MEMORY.md         ← 長期記憶
├── USER.md           ← Joe 資料
├── TOOLS.md          ← 工具配置
├── HEARTBEAT.md      ← 心跳檢查
│
├── memory/
│   ├── 2026-02-27.md
│   └── enterprise-neural-system.md
│
└── skills/           ← 40+ Skills
    ├── knowledge-agent/
    ├── self-evolve-agent/
    ├── workflow-orchestrator/
    └── ...
```

---

## 使用場景

| 場景 | 召喚 Bot |
|------|----------|
| 重大決策審視 | @Neicheok_bot |
| 知識查詢 | @CynthiaChoi_bot |
| 學習優化 | @Joejoebaby_bot |
| 任務排程 | @Inarijoe_bot |
| 技能升級 | @GodKiraCheok_bot |
| 綜合決策 | @KiraIsla_bot |

---

_更新：2026-02-27_
