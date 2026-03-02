#!/bin/bash
# OpenClaw 自動備份腳本
# 每日 03:00 執行

BACKUP_DIR="$HOME/.openclaw/backup"
DATE=$(date +%Y%m%d)
KEEP_DAYS=7

# 建立當日備份資料夾
mkdir -p "$BACKUP_DIR/$DATE"

# 1. 備份配置
cp "$HOME/.openclaw/openclaw.json" "$BACKUP_DIR/$DATE/" 2>/dev/null

# 2. 備份 Agents
cp -r "$HOME/.openclaw/agents" "$BACKUP_DIR/$DATE/" 2>/dev/null

# 3. 備份 Skills
cp -r "$HOME/.openclaw/workspace/skills" "$BACKUP_DIR/$DATE/" 2>/dev/null

# 4. 備份 Memory
cp -r "$HOME/.openclaw/workspace/memory" "$BACKUP_DIR/$DATE/" 2>/dev/null

# 5. 備份 Crons
openclaw cron list > "$BACKUP_DIR/$DATE/crons.txt" 2>/dev/null

# 6. 清理舊備份（保留 7 天）
find "$BACKUP_DIR" -maxdepth 1 -type d -name "20*" -mtime +$KEEP_DAYS -exec rm -rf {} \; 2>/dev/null

echo "✅ 備份完成: $DATE"
