# Agent 效能分析報告

**時間:** 2026-03-01 13:59:49 (Asia/Macau)

## 系統概覽

| 項目 | 狀態 | 備註 |
|------|------|------|
| Gateway | ✅ 正常 | 18ms 延遲 |
| Node Service | ✅ 運行中 | pid 35737 |
| Sessions 總數 | 1005 | 歷史累積 |
| Active Sessions | 10 | cron + group |
| 模型 | MiniMax-M2.5 | 200k context |

## 效能指標

### Context 使用率
| Session | Context | 狀態 |
|---------|---------|------|
| agent:evolution:group | 76k/200k (38%) | ⚠️ 較高 |
| agent:main:group | 18k/200k (9%) | ✅ 正常 |
| agent:slime:cron | 13k/200k (7%) | ✅ 正常 |
| agent:team:cron | 12k/200k (6%) | ✅ 正常 |
| agent:evolution:cron | 14k/200k (7%) | ✅ 正常 |

### Cache 命中率
| Session | 命中率 | 評估 |
|---------|--------|------|
| agent:slime:cron | 232% | ✅ 極佳 |
| agent:evolution:cron | 227% | ✅ 極佳 |
| agent:team:cron | 147% | ✅ 良好 |
| agent:main:group | 34% | ⚠️ 較低 |

## 發現

### ✅ 正常項目
- Gateway 響應時間: 18ms (優異)
- 大部分 session cache 命中率 >100%
- 模型運行穩定

### ⚠️ 關注項目
1. **agent:evolution:group** context 使用率 38% - 偏高但仍可控
2. **agent:main:group** cache 命中率僅 34% - 可能需優化 prompt

### 🔴 安全警告 (非效能但需關注)
- Telegram groupPolicy 設為 "open" - CRITICAL 安全風險
- 建議: 改為 "allowlist"

## 建議行動
1. 監控 agent:evolution:group 的 context 增長
2. 考慮為 agent:main:group 優化 prompt 提升 cache 命中率
儘快修復 Telegram3.  安全配置

---
*由 Cron: agent-performance 生成*
