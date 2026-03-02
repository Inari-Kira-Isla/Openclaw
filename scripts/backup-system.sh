#!/bin/bash
# 系統備份腳本

DATE=$(date +%Y%m%d)
BACKUP_DIR="$HOME/.openclaw/backup/$DATE"

echo "=== 系統備份開始: $DATE ==="

# 1. 建立備份目錄
mkdir -p $BACKUP_DIR
echo "1. 建立備份目錄: $BACKUP_DIR"

# 2. 備份配置
cp ~/.openclaw/openclaw.json $BACKUP_DIR/
echo "2. 配置: openclaw.json ✅"

# 3. 備份 Agents
cp -r ~/.openclaw/agents $BACKUP_DIR/
echo "3. Agents ✅"

# 4. 備份 Skills
cp -r ~/.openclaw/workspace/skills $BACKUP_DIR/
echo "4. Skills ✅"

# 5. 備份 Memory
cp -r ~/.openclaw/workspace/memory $BACKUP_DIR/
echo "5. Memory ✅"

# 6. 備份 Crons (export)
openclaw cron list > $BACKUP_DIR/crons.txt 2>/dev/null
echo "6. Crons: crons.txt ✅"

# 7. 清理舊備份（保留7日）
find $HOME/.openclaw/backup -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
echo "7. 清理舊備份 ✅"

echo ""
echo "=== 備份完成 ==="
echo "位置: $BACKUP_DIR"
