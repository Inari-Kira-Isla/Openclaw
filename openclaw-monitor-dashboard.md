# 📊 OpenClaw 系統監控儀表板

**更新時間:** 2026-02-28 19:41 (Asia/Macau)

---

## 🚀 系統概覽

| 項目 | 狀態 | 數值 |
|------|------|------|
| Gateway | 🟢 運行中 | 21ms 延遲 |
| Session 數量 | 🟢 | 383 active |
| 模型 | 🟢 | MiniMax-M2.5 (200k ctx) |
| Memory | 🟢 | 114 files, 210 chunks |
| Node 服務 | ⚪ | 未安裝 |

---

## ⚠️ 安全警示 (9 嚴重 / 2 警告 / 2 提示)

### 嚴重問題
1. **小型模型風險** - ollama/qwen2.5:7b 需啟用 sandbox
2. **開放群組政策** - groupPolicy="open" 需改為 allowlist
3. **配置檔案權限** - chmod 600 ~/.openclaw/openclaw.json

---

## 📈 Session 狀態 (Top 10)

| Session | Age | Model | Tokens |
|---------|-----|-------|--------|
| agent:cynthia:group | just now | MiniMax-M2.5 | 137k/200k (69%) |
| agent:team:group | just now | MiniMax-M2.5 | 165k/200k (82%) |
| agent:main:group | 1m ago | MiniMax-M2.5 | **184k/200k (92%)** ⚠️ |
| agent:slime:group | 1m ago | MiniMax-M2.5 | 159k/200k (80%) |
| agent:evolution:group | 1m ago | MiniMax-M2.5 | **182k/200k (91%)** ⚠️ |

---

## 🔧 Channel 狀態

| Channel | Enabled | State |
|---------|---------|-------|
| Telegram | ON WARN (groupPolicy | ⚠️ 需修復) |

---

## 💡 建議行動

- [ ] 修復 groupPolicy 為 allowlist
- [ ] 設定 config 檔案權限 600
- [ ] 為高風險 session (92%, 91%) 壓縮上下文
- [ ] 啟用心跳監控

---

## 🔗 快速連結

- Dashboard: http://127.0.0.1:18789/
- 狀態命令: `openclaw status`
- 安全審計: `openclaw security audit`

---

*自動更新於 cron:5c949e8d-658b-47d4-b93d-1d356fe3e71b*
