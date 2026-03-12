# Openclaw

## Project

多 Bot 協作系統，由 6 個 Telegram Bot 組成（Nei、Kira、Cynthia、史萊姆、Team、Evolution），採用雙核心決策制，結合 Claude 4.5 與 MiniMax-M2.5 模型。

## Conventions

- 使用 Python 開發 Bot 邏輯
- 所有技能存放於 `~/.openclaw/workspace/skills/` 目錄
- 每個 Bot 獨立資料夾，含 `BOT_SETUP.md` 設定檔
- 長期記憶記錄於 `~/.openclaw/workspace/memory/` 目錄
- Markdown 格式撰寫文件，保持結構清晰

## Naming

- Bot 帳號使用 Telegram username 格式（如 `@Neicheok_bot`）
- Skill 資料夾使用 kebab-case（如 `knowledge-agent`）
- 記憶檔案使用日期格式（`YYYY-MM-DD.md`）
- 變數與函式使用 snake_case

## Architecture

- **雙核心制**: Kira 提出方案 → Nei 裁決 → Team 執行
- **三層架構**: 記憶層（Kira、Cynthia）→ 學習機制（史萊姆）→ 進化引擎（Team、Evolution）
- **決策流程**: User → Kira → Nei → Evolution → Team
- **裁決規則**: Nei 60 秒內回覆；無回覆時 Kira 可直接執行；上訴最多 2 次

## Commands

- 部署新 Bot：參考 `~/.openclaw/workspace/BOT_SETUP.md`
- 新增 Skill：在 `skills/` 建立獨立資料夾，含 `skill.yaml` 定義
- 查詢知識：呼叫 Cynthia 的 knowledge_search
- 觸發學習：呼叫史萊姆的 prompt_refinement
- 執行排程任務：使用 Team 的 task_scheduling

## Do Not

- 勿直接修改他人 Bot 的設定檔
- 勿跳過 Nei 裁決直接執行重大決策
- 勿在生產環境測試未經漂移偵測的 Prompt
- 勿刪除歷史記憶檔案（保留於 memory/）