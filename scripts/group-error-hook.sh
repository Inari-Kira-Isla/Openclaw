#!/bin/bash
# 群組錯誤自動恢復鉤子
# 觸發詞：群組錯誤

echo "=== 群組錯誤檢測 ==="
echo "時間: $(date)"

# 1. 檢測最近的備份
BACKUP_DIR=~/.openclaw/backup
LATEST=$(ls -1t $BACKUP_DIR/202* | head -1)

if [ -z "$LATEST" ]; then
    echo "沒有找到備份"
    exit 1
fi

DATE=$(basename $LATEST)
echo "找到備份: $DATE"

# 2. 還原配置
echo "還原配置..."
cp $LATEST/openclaw.json ~/.openclaw/openclaw.json

# 3. 還原Agents
echo "還原Agents..."
rm -rf ~/.openclaw/agents
cp -r $LATEST/agents ~/.openclaw/agents

# 4. 重啟服務
echo "重啟服務..."
openclaw restart

echo "=== 恢復完成 ==="
