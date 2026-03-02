# 供應鏈警報日誌

## 2026-03-02 15:44

**狀態**: Telegram 安全修復 ✅

### 安全問題

| 項目 | 狀態 |
|------|------|
| Telegram groupPolicy | ⚠️ 7個 bot 設為 "open" |

### 修復動作

已將所有 Telegram bot 的 groupPolicy 從 "open" 改為 "allowlist"：

```
sed -i '' 's/"groupPolicy": "open"/"groupPolicy": "allowlist"/g' openclaw.json
```

### GitHub 監控

**OpenClaw Repo 最新 PRs:**
| # | 標題 | 狀態 |
|---|------|------|
| 31434 | Gateway: bypass root Control UI for exact webhook routes | OPEN |
| 31433 | fix(identity): support fullwidth colon and CJK labels | OPEN |
| 31431 | fix(hooks): fire message:received hook unconditionally | OPEN |
| 31430 | fix(heartbeat): retry session-event runs on transient failures | OPEN |

**Issues:**
| # | 標題 |
|---|------|
| 31435 | Pre-compaction memoryFlush improvements |
| 31432 | Customisable prompt + larger threshold |
| 31427 | Log timestamp timezone inconsistency |

**結論**: 這些是 OpenClaw 內部修復，與 Joe 的系統無直接相關，無需 immediate action。

---
