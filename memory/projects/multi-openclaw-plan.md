# 009: 多 OpenClaw 協作同步計劃

## 目標
建立龍蝦貓家族跨機協作與同步機制

---

## 成員現況 (2026-02-25)

### Tailscale 網路
| 成員 | 主機名 | Tailscale IP | 遠端網址 | 狀態 |
|------|--------|--------------|----------|-------|
| 大姊 | Mac mini (kiramac-mini) | 100.113.134.56 | https://kiramac-mini.taild5212b.ts.net/ | ✅ |
| 大妹 | Kiras-MacBook-Pro | 100.94.237.207 | - | ✅ |
| 小妹 | Kiras-iPad | 100.106.160.212 | - | ✅ |

### OpenClaw Gateway
- 本機: 127.0.0.1:18789 ✅
- 遠端: Tailscale Serve 已啟動 ✅

---

## 本機配置 (Mac mini)

### ✅ 已完成
- Tailscale VPN 安裝與登入
- Gateway 服務運行 (127.0.0.1:18789)
- Tailscale Serve 遠端連線

### ⏳ 待處理
| 項目 | 優先級 | 說明 |
|------|--------|------|
| Git Repo 同步 | P1 | workspace 同步至 Git |
| iCloud 擴展 | P2 | iCloud Drive 同步 memory/ |
| Syncthing 安裝 | P2 | 檔案同步備選方案 |
| 自動化腳本 | P1 | 自動同步流程 |

---

## 技能傳承

### 實現方式
```
方案 A: Git-based 同步
- ~/.openclaw/workspace/ 放 Git
- 大姊 push → 大妹小妹 pull

方案 B: OpenClaw Cron + API
- 大姊定時廣播可用技能
- 大妹小妹透過 API 請求技能
```

---

## 知識共享

### 實現方式
```
方案 A: Notion 為中樞 (現有)
- 所有記憶寫入 Notion
- 各機從 Notion 讀取

方案 B: iCloud 同步 (推薦)
- memory/ 放 iCloud Drive
- 跨設備自動同步

方案 C: Syncthing
- 點對點檔案同步
```

---

## 快照備份

### 需備份項目
- ~/.openclaw/config/      # 設定
- ~/.openclaw/workspace/  # 技能與記憶
- ~/.openclaw/memory/     # 向量資料庫
- OpenClaw Gateway 狀態

### 備份位置
- 本地: Time Machine / 外接硬碟
- 雲端: iCloud Drive / Dropbox

### 腳本實現
```bash
# backup-openclaw.sh
DATE=$(date +%Y%m%d)
tar -czf ~/Backups/openclaw-$DATE.tar.gz \
  ~/.openclaw/config \
  ~/.openclaw/workspace \
  ~/.openclaw/memory
```

---

## 遠端遙控

### SSH 測試
```bash
ssh jam@100.113.134.56  # → 大姊 (Mac mini)
ssh jam@100.94.237.207  # → 大妹 (MacBook Pro)
```

### Tailscale Serve
- 大姊: https://kiramac-mini.taild5212b.ts.net/

---

## 優先順序

| 優先級 | 項目 | 狀態 |
|--------|------|-------|
| P0 | Tailscale + Gateway | ✅ 完成 |
| P1 | Git Repo 同步 | ⏳ 待處理 |
| P1 | 自動化腳本 | ⏳ 待處理 |
| P2 | iCloud 擴展 | ⏳ 待處理 |
| P2 | Syncthing 安裝 | ⏳ 待處理 |
| P3 | 技能傳承 | 📋 規劃中 |
| P3 | 知識共享 | 📋 規劃中 |
| P3 | 快照備份 | 📋 規劃中 |

---

## 待處理摘要

### Git Repo 同步
```bash
# 選項 1: GitHub 托管
git init ~/.openclaw/workspace
git add .
git commit -m "OpenClaw workspace backup"
git remote add origin https://github.com/user/repo.git

# 選項 2: 同步到另一台 Mac
rsync -avz --exclude node_modules ~/.openclaw/workspace/ jam@100.94.237.207:~/openclaw/
```

### iCloud 擴展
```bash
# 將 memory 連結到 iCloud
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/OpenClaw/memory ~/.openclaw/memory-icloud
```

---

_Last updated: 2026-02-25_
