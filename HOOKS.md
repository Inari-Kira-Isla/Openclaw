# Hooks 配置 — 精簡閉環架構
_更新：2026-03-04_

## 設計原則：正向閉環

```
Success → 記錄模式 → 強化（保持/增頻）
Failure → 記錄錯誤 → 降級（自動停用）
Recovery → 偵測修復 → 重新啟用
Learning → 每日報告 → 人工決策 → 下一輪改進
```

## 核心架構（優化後）

### 1. 核心閉環 — 每小時 4 階段（保留）

| Job | 排程 | 職責 |
|-----|------|------|
| 閉環啟動 (f0656ece) | `0 * * * *` | 啟動週期，觸發 hooks |
| 閉環反饋 (1344cef3) | `15 * * * *` | 收集結果 |
| 閉環分析 (8a17ed49) | `30 * * * *` | 分析模式 |
| 閉環優化 (5f539354) | `45 * * * *` | 應用優化 |

### 2. Agent 心跳 — 每 30 分鐘（保留）

| Agent | 職責 |
|-------|------|
| cynthia-heartbeat | 知識庫 |
| slime-heartbeat | 學習優化 |
| team-heartbeat | 任務執行 |
| evolution-heartbeat | 技能進化 |
| neicheok-heartbeat | 決策審視 |

### 3. 系統監控 — 精簡為 3 個

| Job | 排程 | 職責 |
|-----|------|------|
| sys-health-30m (d869f2fd) | `*/30 * * * *` | 系統健康總覽 |
| 安全監控 (ccb8ff1e) | `*/10 * * * *` | 安全掃描 |
| Token實時監控 (42519b59) | `*/19 * * * *` | Token 用量 |

### 4. 健康閉環 — 每日 1 次

| Job | 排程 | 職責 |
|-----|------|------|
| cron-health-loop | `0 23 * * *` (LaunchAgent) | 評分 + 自動降級 + Telegram 報告 |

## 自動降級規則

| 條件 | 動作 |
|------|------|
| `consecutiveErrors >= 3` | 自動停用 + Telegram 通知 |
| `consecutiveErrors >= 5` | 自動停用 + 標記需人工檢查 |
| Always-skip 高頻 job | 清理時一次性停用 |
| 重複名稱 job | 保留最佳狀態的，停用其餘 |

## 已停用（2026-03-04 清理）

- 18 個重複名稱 jobs（Gmail摘要 x3→1, 美股觀察 x3→1 等）
- 10 個 AI閉環/閉環 重疊對（去重，保留 status=ok 版本）
- 7 個連續錯誤 ≥3 次的 jobs（照片生成/Skill升級等）
- 35 個 always-skip 高頻 jobs（向量庫/Session/Agent routing）
- 5 個冗餘監控 jobs（Heartbeat overhead/重複安全監控）
- 舊 結合-* hooks（Notion API 過期）
- 舊 RAG閉環 jobs（已替換為向量版本）

## 手動操作

```bash
# 重新啟用修復後的 job
openclaw cron edit <job-id> --enabled

# 查看 job 近期執行紀錄
openclaw cron runs <job-id>

# 手動執行健康檢查
node ~/.openclaw/workspace/scripts/cron_health_loop.js

# 查看健康歷史趨勢
tail -7 ~/.openclaw/cron/health-history.jsonl | python3 -m json.tool

# 一次性清理（已執行）
bash ~/.openclaw/workspace/scripts/cron_cleanup.sh --execute
```
