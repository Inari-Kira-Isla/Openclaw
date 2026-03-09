# Session 效能優化報告

**時間:** 2026-02-28 21:39 (Asia/Macau)

---

## 系統狀態

| 項目 | 狀態 |
|------|------|
| Gateway | ✅ 正常 (26ms) |
| Sessions | 483 總數 / 1 active |
| Model | MiniMax-M2.5 |

---

## Context 使用量 (需關注)

| Agent | Session | Context | 狀態 |
|-------|---------|---------|------|
| Cynthia | group:-5138835175 | 163k/200k (82%) | ⚠️ 過高 |
| Main | group:-5138835175 | 124k/200k (62%) | ⚠️ 中高 |
| Slime | group:-5138835175 | 92k/200k (46%) | ⚠️ 中高 |
| Evolution | group:-5138835175 | 92k/200k (46%) | ⚠️ 中高 |
| Team | group:-5138835175 | 72k/200k (36%) | ⚠️ 中高 |

---

## 優化動作

1. ✅ 閒置資源: 483 sessions 中僅 1 個 active，其餘為 cron sessions（正常）
2. ⚠️ 高 context group sessions: 5 個群組 session 超過 35%
3. ⏸️ 壓縮建議: 考慮對 80%+ 的 Cynthia group session 進行壓縮

---

## 建議

- Cynthia group session (82%) 建議壓縮或重置
- 其餘 group sessions 可暫時維持

---

_Generated: 2026-02-28 21:39_
