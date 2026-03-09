#!/bin/bash
# 自動恢復鉤子
# 當檢測到錯誤信號時自動恢復

echo "=== 自動恢復鉤子 ==="

# 1. 找最新既備份
LATEST_BACKUP=$(ls -t ~/.openclaw/backup/ 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ 沒有找到備份"
    exit 1
fi

echo "使用備份: $LATEST_BACKUP"

# 2. 恢復配置
if [ -f ~/.openclaw/backup/$LATEST_BACKUP/openclaw.json ]; then
    cp ~/.openclaw/backup/$LATEST_BACKUP/openclaw.json ~/.openclaw/
    echo "✅ 配置已恢復"
fi

# 3. 恢復 Skills
if [ -d ~/.openclaw/backup/$LATEST_BACKUP/skills ]; then
    cp -r ~/.openclaw/backup/$LATEST_BACKUP/skills ~/.openclaw/workspace/
    echo "✅ Skills 已恢復"
fi

# 4. 恢復 Memory
if [ -d ~/.openclaw/backup/$LATEST_BACKUP/memory ]; then
    cp -r ~/.openclaw/backup/$LATEST_BACKUP/memory ~/.openclaw/workspace/
    echo "✅ Memory 已恢復"
fi

# 5. 重新啟動 Gateway
openclaw gateway restart
echo "✅ Gateway 已重啟"

echo ""
echo "=== 自動恢復完成 ==="
