# OpenClaw 系統監控儀表板

**最後更新**: 2026-03-01 01:13 (Asia/Macau)

---

## 系統狀態 ✅

| 項目 | 狀態 |
|------|------|
| Gateway | ✅ reachable (18ms) |
| Node Service | ✅ running (pid 86484) |
| Gateway Service | ✅ running (pid 86206) |
| Sessions | 646 active |
| Model | MiniMax-M2.5 (200K ctx) |

---

## 安全警示 ⚠️

| 等級 | 數量 | 說明 |
|------|------|------|
| CRITICAL | 1 | 小模型需啟用沙箱 |
| WARN | 2 | 代理設定、多用戶潛在風險 |
| INFO | 2 | 需配置 trustedProxies |

**修復建議**: `openclaw security audit --deep`

---

## Channels

| Channel | Enabled | State |
|---------|---------|-------|
| Telegram | ON | WARN (token config) |

---

## 監控備註

- 安靜時段 (23:00-07:00) - 不發送通知
- 下次主動檢查: 07:00 早安簡報

---

_由 cron:5c949e8d-658b-47d4-b93d-1d356fe3e71b 更新_
