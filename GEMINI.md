# Openclaw

## Overview
Openclaw 是一個由 6 個 AI Bot 組成的多代理協作系統，採用「雙核心制」運作。Kira 負責提案與分流，Nei 負責審視與裁決，Team 負責執行。系統包含記憶層（Cynthia）、學習機制（史萊姆）與進化引擎（Evolution），旨在實現自主決策與持續優化。

## Tech Stack
- **通訊介面**: Telegram Bot API
- **LLM 核心**: Claude 4.5 API, MiniMax-M2.5
- **知識庫**: Notion, SQLite-Vec
- **排程與監控**: Cron, Heartbeat
- **開發框架**: Python/Node.js (OpenClaw 工具)

## Architecture
- **根目錄**: `~/.openclaw/workspace/`
- **雙核心**:
  - **Kira**: 中央治理（方案提出）。
  - **Nei**: 決策審視者（最終裁決，Claude 4.5）。
- **分層結構**:
  - 記憶層: Cynthia (知識庫), Kira (中央治理)。
  - 學習機制: 史萊姆 (Prompt 優化, 漂移偵測)。
  - 進化引擎: Team (任務排程), Evolution (技能進化)。
- **關鍵檔案**: `BOT_SETUP.md`, `SOUL.md`, `AGENTS.md`, `skills/`

## Commands
| 場景 | 指令/操作 |
|------|----------|
| 綜合決策 | 聯繫 @KiraIsla_bot |
| 重大裁決 | 聯繫 @Neicheok_bot |
| 知識查詢 | 聯繫 @CynthiaChoi_bot |
| 學習優化 | 聯繫 @Joejoebaby_bot |
| 任務排程 | 聯繫 @Inarijoe_bot |
| 技能升級 | 聯繫 @GodKiraCheok_bot |

## Coding Style
- **模組化**: 所有技能存放於 `skills/` 目錄，獨立成冊。
- **一致性**: Workflow 需遵循 `AGENTS.md` 定義的流程（分流 -> 審視 -> 執行）。
- **版本控制**: Evolution 負責 Skill 的版本控制與融合。

## Important Rules
- **裁決權**: Nei 擁有最終裁決權，時限 60 秒。若無回覆，Kira 可直接執行。
- **上訴機制**: 若 Nei 否決，可上訴至 Evolution，最多 2 次。
- **協作禁忌**: 禁止跳過 Kira 直接调度 Team，或绕过 Nei 直接執行裁決。