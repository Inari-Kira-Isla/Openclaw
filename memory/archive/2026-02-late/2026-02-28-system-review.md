# 2026-02-28 系統審視與優化討論

## 審視日期
2026-02-28 3:30 PM (Asia/Macau)

## 系統現狀

### 1. 排程狀態 (Scheduling)
- **Heartbeat**: 大多數 Bot 的 heartbeat 已被 disabled
  - 啟用: main (30m)
  - 禁用: slime, team, evolution, cynthia, knowledge-agent 等 30+ agents
- **Cron**: 正常運作中（此次即為 cron 觸發）

### 2. 記憶層 (Memory)
- 101 files, 189 chunks
- Vector search enabled
- FTS enabled

### 3. Notion 整合
- 已配置但未見自動同步狀態

---

## 選擇的質疑問題

**Heartbeat 全面關閉導致自動化排程失效**

### 現況
- 5 個關鍵 Bot 的 heartbeat 全部 disabled
- 系統無法自動執行定時任務（BNI 提醒、知識庫更新等）

### 分析

#### 為何 heartbeat 被關閉？
1. **安全考量**: OpenClaw 安全審計顯示多個 CRITICAL 警告
   - groupPolicy="open" 允許任何群成員觸發
   - 小模型 (qwen2.5:7b) 缺乏沙箱保護
   - 可能因此全面關閉主動式 heartbeat 降低風險

2. **資源考量**: heartbeat 每次觸發消耗 context tokens
   - 當前 sessions 顯示 60-70% context 使用率
   - 大量 heartbeat 可能導致 context 爆炸

3. **穩定性問題**: 可能曾發生過度觸發或迴圈

#### 重啟 heartbeat 的風險
- 未授权任务触发（groupPolicy 問題未解決前）
- 資源競爭（多個 heartbeat 同時搶 context）
- 安全性漏洞擴大

#### 替代方案
1. **使用 Cron 取代 Heartbeat**
   - 更可控的調度頻率
   - 可隔離執行環境
   - 符合 USER.md 中 "Wave 1: BNI 提醒" 需求

2. **設定嚴格 heartbeat 白名單**
   - 只對關鍵 Bot（Team, Kira）啟用 heartbeat
   - 配合 groupPolicy="allowlist"

3. **使用 n8n 工作流**
   - 參考 TOOLS.md: "n8n — 未安裝，改用 OpenClaw Cron"
   - 但可考慮安裝 n8n 作為排程協調層

---

## 建議行動

| 優先級 | 行動 | 負責 Bot |
|--------|------|----------|
| P0 | 修復 groupPolicy="open" 安全性問題 | Kira |
| P1 | 選擇性啟用 Team/Evolution heartbeat | Team |
| P2 | 評估 n8n 安裝必要性 | Evolution |
| P3 | 建立 Cron 任務清單（BNI 提醒等） | Team |

---

## 結論

Heartbeat 關閉是合理的暫時安全措施，但長期來看需要：
1. 先解決安全漏洞（groupPolicy）
2. 再選擇性恢復 heartbeat
3. 補充 Cron 作為備用排程方案

**短期可用 Cron 實現基礎自動化，無需等待 heartbeat 恢復。**
