# OpenClaw 系統備份與恢復指南

> 最後更新：2026-03-01

---

## 概述

本文檔說明如何備份和恢復 AI 治理系統（OpenClaw）的數據和配置。

---

## 備份項目

| 項目 | 說明 | 優先級 |
|------|------|--------|
| openclaw.json | 系統配置 | P0 |
| agents/ | Agent 配置 | P0 |
| cron jobs | 定時任務 | P0 |
| skills/ | 自定義技能 | P1 |
| memory/ | 記憶數據 | P1 |
| hooks/ | 鉤子腳本 | P1 |

---

## 自動備份

系統已配置每日自動備份：

- **時間**：每日 03:00
- **位置**：`~/.openclaw/backup/YYYYMMDD/`
- **保留期**：7 天

---

## 手動備份命令

```bash
# 建立備份資料夾
mkdir -p ~/.openclaw/backup/$(date +%Y%m%d)

# 1. 備份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/backup/$(date +%Y%m%d)/

# 2. 備份 Agents
cp -r ~/.openclaw/agents ~/.openclaw/backup/$(date +%Y%m%d)/

# 3. 備份 Crons
openclaw cron list > ~/.openclaw/backup/$(date +%Y%m%d)/crons.txt

# 4. 備份 Skills
cp -r ~/.openclaw/workspace/skills ~/.openclaw/backup/$(date +%Y%m%d)/

# 5. 備份 Memory
cp -r ~/.openclaw/workspace/memory ~/.openclaw/backup/$(date +%Y%m%d)/
```

---

## 恢復步驟

### 步驟 1：確認備份存在

```bash
ls -la ~/.openclaw/backup/
```

選擇要恢復的日期（例如 20260301）。

### 步驟 2：恢復配置

```bash
# 停止 OpenClaw 服務
openclaw gateway stop

# 恢復配置
cp ~/.openclaw/backup/20260301/openclaw.json ~/.openclaw/

# 恢復 Agents
cp -r ~/.openclaw/backup/20260301/agents/ ~/.openclaw/

# 啟動 OpenClaw 服務
openclaw gateway start
```

### 步驟 3：恢復 Cron Jobs

Cron jobs 需要手動重建：

```bash
# 查看備份的 cron 清單
cat ~/.openclaw/backup/20260301/crons.txt
```

根據清單重新建立 cron jobs：

```bash
# 示例：建立每日備份 cron
openclaw cron add \
  --name "每日系統備份" \
  --cron "0 3 * * *" \
  --session main \
  --system-event "每日系統備份" \
  --description "每日自動備份系統配置"
```

### 步驟 4：恢復 Skills

```bash
cp -r ~/.openclaw/backup/20260301/skills/ ~/.openclaw/workspace/
```

### 步驟 5：恢復 Memory

```bash
cp -r ~/.openclaw/backup/20260301/memory/ ~/.openclaw/workspace/

# 重新向量化
openclaw memory index --force
```

---

## 緊急恢復清單

如果系統完全崩潰，按以下順序恢復：

| 順序 | 項目 | 命令 |
|------|------|------|
| 1 | 重新安裝 OpenClaw | 見官網安裝指南 |
| 2 | 恢復配置 | cp openclaw.json |
| 3 | 恢復 Agents | cp -r agents/ |
| 4 | 建立 Cron | openclaw cron add |
| 5 | 恢復 Skills | cp -r skills/ |
| 6 | 恢復 Memory | cp -r memory/ |
| 7 | 重建索引 | openclaw memory index --force |

---

## 雲端備份（可選）

建議同時使用雲端備份：

### iCloud Drive
```bash
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/OpenClawBackup ~/.openclaw/backup-cloud
```

### Google Drive
使用 Google Drive for Mac 同步備份資料夾。

### Time Machine
確保 OpenClaw 資料夾被 Time Machine 覆蓋：
```bash
tmutil addexclude ~/.openclaw/backup
# 注意：排除臨時備份，保留主要數據
```

---

## 驗證恢復

恢復完成後，運行以下命令驗證：

```bash
# 1. 檢查狀態
openclaw status

# 2. 檢查 Cron
openclaw cron list | wc -l

# 3. 檢查記憶
openclaw memory status

# 4. 檢查 Hooks
openclaw hooks list
```

---

## 聯繫支持

如有問題，請檢查：
- OpenClaw 文檔：https://docs.openclaw.ai
- 社區支援：https://discord.com/invite/clawd

---

*本文檔由 AI 治理系統自動生成*
