# Token 使用手則

## 問題診斷
- **原因**：過多 cron jobs 同時觸發 → API rate limit
- **解決**：錯峰執行 + 禁用無效 jobs + 配額管理

---

## 1. 已執行的優化

### 禁用無效 Jobs（減少 3 個）
| Job | 原因 |
|-----|------|
| auto-vectorize-rag | delivery error |
| 自動向量提取 | delivery error |
| 對話-快速存儲 | 過於頻繁 (每5分) |

### 排程分組錯峰
```
Group A (每30分): heartbeat agents → 0, 30 分
Group B (每15分): 監控系統 → +5 分偏移  
Group C (每15分): 安全/學習 → +10 分偏移
```

---

## 2. 速率限制規則

| 窗口 | 最大請求 | 冷卻 |
|-----|---------|-----|
| 每分鐘 | 10 | 6s |
| 每 5 分鐘 | 40 | 3s |
| 每小時 | 300 | 1s |

---

## 3. 新增 Cron 建議

用以下命令錯開新 cron：
```bash
# 每15分 → 改為 17, 32, 47, 02 (每小時4次，不重疊)
# 每30分 → 改為 35, 05 (避開 30/00)

# 建議每小時總請求 < 50
```

---

## 4. 監控

配置路徑：`~/.openclaw/workspace/config/token-scheduler.json`

可用命令：
- `openclaw cron list` - 查看所有排程
- `openclaw cron disable <id>` - 禁用
- `openclaw cron enable <id>` - 啟用

---

## 5. 後續建議

1. **每週審查** cron jobs 狀態
2. **合併相似功能**（多個 RAG cron → 1個）
3. **監控儀表板** - 查看即時 token 使用

---

## 6. 向量化排程優化 (2026-03-01)

### 新排程分配
| Job | Cron | Agent | 優先級 | 偏移 |
|-----|------|-------|--------|------|
| sync-quick | */17 | memory-agent | High | 17分 |
| sync-full | */31 | cynthia | High | 31分 |
| deep-embed | 0 * * * * | memory-agent | Medium | 整點 |
| quality-check | 0 4 * * * | cynthia | Low | 4am |

### 設計原則
- 使用質數偏移 (17, 31) 減少衝突
- sync 分離為 quick (5分內) + full (驗證)
- 整點保留給 deep-embed（低流量時段）
- 凌晨 4am 品質檢查（最低流量）

---
_更新：2026-03-01_
