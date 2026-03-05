# Task Failure Record

## 2026-03-05 15:17

### Failed Task
- **Session**: mild-nud
- **Signal**: SIGTERM
- **Error**: openclaw not found

### Root Cause
Cron job 環境 PATH 不含 npm global bin (`/usr/local/bin`)

### Resolution
使用 `npx openclaw` 或設定完整 PATH

### Status
✅ 已識別，系統正常運行
