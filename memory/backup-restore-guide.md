# 系統備份與恢復指南

**建立日期**: 2026-03-01  
**適用系統**: OpenClaw AI 治理系統

---

## 📋 概述

本文件提供 OpenClaw 系統各组件的備份與恢復流程。

---

## 1. OpenClaw 設定備份與恢復

### 1.1 設定檔位置

| 項目 | 路徑 |
|------|------|
| 主配置 | `~/.openclaw/openclaw.json` |
| Workspace | `~/.openclaw/workspace/` |
| Skills | `~/.openclaw/workspace/skills/` |
| 向量庫 | `~/.openclaw/memory/` |

### 1.2 備份腳本

```bash
#!/bin/bash
# backup-openclaw.sh

BACKUP_DIR=~/backups/openclaw
DATE=$(date +%Y-%m-%d)

mkdir -p $BACKUP_DIR/$DATE

# 備份設定檔
cp ~/.openclaw/openclaw.json $BACKUP_DIR/$DATE/

# 備份 workspace
cp -r ~/.openclaw/workspace $BACKUP_DIR/$DATE/

# 備份向量庫
cp -r ~/.openclaw/memory $BACKUP_DIR/$DATE/

echo "Backup completed: $BACKUP_DIR/$DATE"
```

### 1.3 恢復流程

```bash
# 1. 停止 OpenClaw 服務
openclaw gateway stop

# 2. 恢復設定檔
cp ~/backups/openclaw/YYYY-MM-DD/openclaw.json ~/.openclaw/

# 3. 恢復 workspace
cp -r ~/backups/openclaw/YYYY-MM-DD/workspace ~/.openclaw/

# 4. 重新建立向量索引
openclaw memory index --force

# 5. 重啟服務
openclaw gateway start
```

---

## 2. 記憶庫 (Memory) 備份與恢復

### 2.1 記憶庫結構

```
~/.openclaw/workspace/
├── MEMORY.md              # 總索引
├── memory/
│   ├── YYYY-MM-DD.md      # 每日筆記
│   ├── archive/           # 歸檔
│   └── capsules/          # 知識膠囊
└── skills/                # 技能庫
```

### 2.2 備份記憶庫

```bash
# 備份 memory 目錄
tar -czvf memory-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/memory/

# 備份單一筆記
cp ~/.openclaw/workspace/MEMORY.md ~/backups/
```

### 2.3 恢復向量索引

```bash
# 強制重建向量索引
openclaw memory index --force

# 檢查索引狀態
openclaw memory status
```

---

## 3. Agent 設定恢復

### 3.1 已註冊 Agents (27個)

| 類別 | Agents |
|------|--------|
| 核心 | muse-core, workflow-orchestrator, skill-creator, mcp-builder |
| 專業 | analytics-agent, knowledge-agent, governance-agent, lifeos-agent |
| 記憶 | memory-agent, self-evolve-agent, skill-slime-agent, verification-agent |
| 團隊 | alice, bob, carol, dave, eva, georgia, isla |
| 其他 | note-taker, statistics-analyzer, code-master, design-master, writing-master, evaluator, agent-builder |

### 3.2 恢復 Agent 註冊

```bash
# 重新註冊單一 Agent
openclaw agents register <agent-name>

# 列出可用 Agents
openclaw agents list
```

---

## 4. Cron Jobs 恢復

### 4.1 主要定時任務

| 時間 | 任務 | 狀態 |
|------|------|------|
| 07:00 | 起床提醒 | ✅ |
| 09:00 | GitHub Releases 檢查 (週一至五) | ✅ |
| 10:00 | 每日 Agent 學習升級 | ✅ |
| 12:00 | 系統健康檢查 | ✅ |
| 18:00 | 照片生成提醒 | ✅ |

### 4.2 恢復 Cron Jobs

```bash
# 列出所有 Cron Jobs
openclaw cron list

# 重新啟用特定 Job
openclaw cron enable <job-id>

# 檢查 Cron 狀態
openclaw status
```

---

## 5. Notion 同步恢復

### 5.1 Notion 設定

- **Page ID**: `311a1238-f49d-81a2-bcf7-d34d1a037833`
- **同步時間**: 每日 12:00

### 5.2 恢復同步

```bash
# 測試 Notion 連接
openclaw notion test

# 執行手動同步
openclaw notion sync
```

---

## 6. 緊急恢復清單

### 發生災難時的復原順序

1. **優先恢復**:
   - [ ] OpenClaw Gateway 服務
   - [ ] 向量索引
   - [ ] 核心 Cron Jobs

2. **次要恢復**:
   - [ ] Agents 註冊
   - [ ] Notion 同步
   - [ ] 記憶庫

3. **最後確認**:
   - [ ] Health check 通過
   - [ ] 所有 Agents 運行正常
   - [ ] 向量搜尋正常

---

## 7. 快速恢復命令

```bash
# 完整系統恢復
openclaw gateway restart
openclaw memory index --force
openclaw cron list
openclaw status
```

---

## 📞 支援

如需協助，請聯繫 Kira (@KiraIsla_bot)

---

_最後更新: 2026-03-01_
