# GitHub 監控 - 2026-03-05 22:46

## PRs (5個新PR)

| # | 標題 | 狀態 |
|---|------|------|
| 36285 | fix(telegram): 防止重複訊息 | OPEN |
| 36284 | fix(gateway): chat.inject 自動建立 transcript | OPEN |
| 36283 | fix(chat): inject 時建立 transcript | OPEN |
| 36282 | fix(agents): openai-responses tool_choice | OPEN |
| 36281 | fix(status): 帳戶選擇顯示問題 | OPEN |

## Issues (5個新Issue)

| # | 標題 | 標籤 |
|---|------|------|
| 36280 | [Bug]: Skill apiKey 洩漏至環境變數 | bug |
| 36270 | [Bug]: HTTP 401 認證錯誤 | bug |
| 36267 | status 顯示不一致 | - |
| 36263 | fix(cron): fallback 未儲存 | - |
| 36260 | Feature: Telegram topic 名稱加入 metadata | feature |

## 相關性分析

### 🔴 高度相關
- **#36280**: Skill apiKey 洩漏 → 安全問題
- **#36285**: Telegram 防止重複 → 與我們的發布問題相關

### 🟡 中度相關
- **#36284/#36283**: transcript 自動建立 → 系統功能
- **#36263**: cron fallback → 定時任務

### 🟢 低相關
- 其他為一般修復

## 團隊討論
- Skill apiKey 洩漏問題需關注
- Telegram 相關修復可能有助於解決我們的群組發布問題

---
*監控完成: 2026-03-05 22:46*
