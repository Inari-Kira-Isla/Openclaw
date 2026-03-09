#!/bin/bash
# 每小時對話摘要

DATE=$(date +%Y-%m-%d)
HOUR=$(date +%H)

echo "=== 對話摘要 $DATE $HOUR:00 ==="

# 1. 獲取對話數量
echo "1. 檢查對話..."
sqlite3 ~/.openclaw/memory/memory.db "SELECT COUNT(*) FROM conversations;"

# 2. 提取最後一小時對話
echo "2. 提取對話..."
LAST_HOUR=$(date -v-1H +%Y-%m-%d\ %H:%M:%S)

# 3. 存儲為摘要
echo "3. 存儲摘要..."
SUMMARY_FILE=~/.openclaw/workspace-evolution/memory/dialogue-$DATE-$HOUR.md
echo "# 對話摘要 $DATE $HOUR:00" > $SUMMARY_FILE
echo "" >> $SUMMARY_FILE
echo "生成時間: $(date)" >> $SUMMARY_FILE

echo "=== 完成 ==="
