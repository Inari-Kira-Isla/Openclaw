# GitHub 監控報告 - 2026-03-02

## 23:10 最新 Release 摘要

**v2026.3.1 Release** (2026-03-02 04:42)

| 變更 | 說明 |
|------|------|
| Claude 4.6 adaptive thinking | Anthropic 模型預設 adaptive thinking |
| Health endpoints | Gateway 新增 /health, /healthz 端點 |
| Android nodes | 相機、通知新功能 |
| Discord lifecycle | Thread 閒置 24h 自動結束 |
| Telegram DM topics | DM 主題配置功能 |
| Cron i18n | Web UI 本地化 |

### 相關性評估
- ✅ Health endpoints 與系統監控相關
- ⚠️ 其他為功能增強，非緊急性質

---
## 11:27 PR 摘要

| # | 標題 | 狀態 | 相關性 |
|---|------|------|--------|
| 31232 | fix(signal): ignore system messages | OPEN | ⚠️ 與 group 相關 |
| 31230 | feat(gateway): detect exec/sandbox config conflicts | OPEN | ✅ 相關 |
| 31229 | fix(webchat): allow image-only sends | OPEN | ⚠️ |
| 31228 | fix(test): correct mock parameter type | OPEN | ⚠️ |
| 31227 | feat(agents): support thinkingDefault: adaptive | OPEN | ✅ 相關 |

---
_記錄時間: 2026-03-02 23:10 GMT+8_
