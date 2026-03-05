# GitHub 監控報告 - 2026-03-04

## OpenClaw Repo

### 最新 PRs
| # | Title | Status |
|---|-------|--------|
| 33603 | fix(memory): replace glob patterns with directory paths for chokidar v5 | OPEN |
| 33602 | fix(mattermost): honor resolved cfg in outbound sends | OPEN |
| 33601 | fix(cron): return error when payload model is not allowed instead of silent fallback | OPEN |
| 33598 | fix(irc): honor resolved cfg in outbound sends | OPEN |
| 33595 | fix(nextcloud-talk): honor resolved cfg in outbound sends | OPEN |

### 最新 Issues
| # | Title | Status |
|---|-------|--------|
| 33600 | [Bug]: agents.defaults.models allowlist changes not applied on hot-reload | OPEN |
| 33599 | [Bug]: Mattermost outbound send path ignores resolved cfg | OPEN |
| 33596 | [Bug]: IRC outbound send path ignores resolved cfg | OPEN |
| 33594 | ACP bridge not invoking acpx backend from sessions_spawn | OPEN |

## acpx Repo

### 最新 PRs
| # | Title | Status |
|---|-------|--------|
| 43 | chore: align acpx tooling with openclaw stack | MERGED |
| 42 | feat: add Kiro CLI as built-in agent | OPEN |
| 41 | fix: restore --version and staged adapter shutdown fallback | MERGED |

## 相關性分析

### 高度相關
- **#33603** (memory fix): 與記憶系統相關，可能影響本地監控
- **#33601** (cron fix): 與定時任務相關，影響模型驗證
- **#33594** (ACP bridge): 與 ACP 橋接器相關

### 中度相關
- **#33600** (hot-reload bug): 模型 allowlist 熱重載問題
- **#42** (Kiro CLI): 新增 Kiro 作為內建代理

---
_監控時間: 2026-03-04 07:10 UTC+8_
