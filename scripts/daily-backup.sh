#!/bin/bash
# Daily Backup Script - 每日數據備份

BACKUP_DIR="$HOME/openclaw-backups"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 創建備份目錄
mkdir -p "$BACKUP_DIR/$DATE"

echo "=== Daily Backup Started: $TIMESTAMP ==="

# 1. 備份 Memory 文件
echo "[1/7] Backing up Memory files..."
cp -r ~/.openclaw/workspace/memory "$BACKUP_DIR/$DATE/" 2>/dev/null
cp ~/.openclaw/workspace/MEMORY.md "$BACKUP_DIR/$DATE/" 2>/dev/null

# 2. 備份關鍵配置文件
echo "[2/7] Backing up config files..."
cp ~/.openclaw/workspace/AGENTS.md "$BACKUP_DIR/$DATE/" 2>/dev/null
cp ~/.openclaw/workspace/SOUL.md "$BACKUP_DIR/$DATE/" 2>/dev/null
cp ~/.openclaw/workspace/USER.md "$BACKUP_DIR/$DATE/" 2>/dev/null
cp ~/.openclaw/workspace/TOOLS.md "$BACKUP_DIR/$DATE/" 2>/dev/null

# 3. 備份 OpenClaw 配置
echo "[3/7] Backing up OpenClaw config..."
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/$DATE/" 2>/dev/null

# 4. 備份 Skills 目錄（完整備份）
echo "[4/7] Backing up skills directory..."
cp -r ~/.openclaw/workspace/skills "$BACKUP_DIR/$DATE/" 2>/dev/null

# 5. 備份 Scripts 目錄
echo "[5/7] Backing up scripts directory..."
cp -r ~/.openclaw/workspace/scripts "$BACKUP_DIR/$DATE/" 2>/dev/null

# 6. 備份 Config 和 Agents 目錄
echo "[6/7] Backing up config & agents..."
cp -r ~/.openclaw/workspace/config "$BACKUP_DIR/$DATE/" 2>/dev/null
cp -r ~/.openclaw/workspace/agents "$BACKUP_DIR/$DATE/" 2>/dev/null

# 7. 清理舊備份（保留 7 天）
echo "[7/7] Cleaning old backups (keeping 7 days)..."
find "$BACKUP_DIR" -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

echo ""
echo "=== Backup Completed ==="
echo "Location: $BACKUP_DIR/$DATE"
du -sh "$BACKUP_DIR/$DATE/"
