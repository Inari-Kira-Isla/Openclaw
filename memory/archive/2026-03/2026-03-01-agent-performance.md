# Agent 效能分析報告

**日期:** 2026-03-01 01:49 (Asia/Macau)

## 系統狀態總覽

| 項目 | 數值 | 狀態 |
|------|------|------|
| Gateway 響應 | 17ms | ✅ 正常 |
| Agents 數量 | 33 | ✅ 正常 |
| Sessions 總數 | 672 | ✅ 正常 |
| 模型 | MiniMax-M2.5 (200k ctx) | ✅ 正常 |

## 當前運行 Sessions

- **Cron agent-performance**: 26k/200k tokens (13%), 快取 780% ✅
- **Team cron sessions**: 15-17k tokens, 快取 360-417% ✅
- **Main session**: 28k/200k (14%), 快取 129% ✅
- **Group session**: 137k/200k (68%), 快取 99% ⚠️

## 效能觀察

### ✅ 正常指標
1. **Gateway 延遲**: 17ms (低延遲)
2. **快取命中率**: 大多數 session 有高快取率 (99-780%)
3. **Context 使用率**: 大多數低於 20%，表現在控制範圍內
4. **記憶體**: 0 files, 向量搜尋就緒

### ⚠️ 需要關注
1. **Group session context 使用率較高 (68%)** - 建議監控
2. **Security Audit 發現 3 個 CRITICAL 問題** - 見下文

## Security Audit 結果 (CRITICAL)

1. **Small models require sandboxing** - ollama/qwen2.5:7b 使用時需要沙盒
2. **Open groupPolicy with elevated tools** - Telegram groupPolicy="open" 有風險
3. **Open groupPolicy with runtime/filesystem** - 風險工具暴露，建議用 tools.profile="messaging"

## 建議行動

1. 🔴 優先: 修復 Security Audit 中的 CRITICAL 問題
2. 🟡 監控: Team group session (68% context) 是否持續增長
3. 🟢 維持: 目前效能正常，Gateway 響應快速

---
*由 Kira 自動生成*
