#!/bin/bash
# 自動修復群組錯誤 Hook
# 當檢測到群組錯誤時自動恢復備份

DATE=$(date +%Y%m%d)
BACKUP_DIR="$HOME/.openclaw/backup/$DATE"

echo "=== 檢測到群組錯誤，開始自動修復 ==="

# 1. 檢查最新備份
if [ ! -d "$BACKUP_DIR" ]; then
    echo "錯誤：找不到備份目錄 $BACKUP_DIR"
    exit 1
fi

# 2. 恢復配置
echo "1. 恢復配置..."
cp -f "$BACKUP_DIR/openclaw.json" "$HOME/.openclaw/"

# 3. 恢復 agents
echo "2. 恢復 Agents..."
cp -rf "$BACKUP_DIR/agents/" "$HOME/.openclaw/"

# 4. 重新加載配置
echo "3. 重新加載配置..."
openclaw gateway restart

echo "=== 修復完成 ==="
