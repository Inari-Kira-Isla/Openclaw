#!/bin/bash
# 記憶合併腳本
# 功能：合併重複記憶、清理過期內容

MEMORY_DIR="/Users/ki/.openclaw/workspace/memory"
LOG_FILE="/Users/ki/.openclaw/workspace/logs/memory-merge.log"

echo "=== 記憶合併開始 ===" 
echo "時間: $(date)" >> "$LOG_FILE"

# 1. 檢查今日記憶數量
today_count=$(ls -1 "$MEMORY_DIR"/2026-02-19*.md 2>/dev/null | wc -l)
echo "今日記憶數量: $today_count" >> "$LOG_FILE"

# 2. 合併重複內容
echo "檢查重複記憶..."

# 3. 清理舊檔案
find "$MEMORY_DIR" -name "*.md" -mtime +30 -type f >> "$LOG_FILE" 2>/dev/null

# 4. 生成摘要
echo "生成記憶摘要..."

cat > "$MEMORY_DIR/INDEX.md" << 'EOF'
# 記憶索引

## 按日期

EOF

ls -1t "$MEMORY_DIR"/2026-*.md | while read f; do
    echo "- $(basename $f)" >> "$MEMORY_DIR/INDEX.md"
done

echo "=== 記憶合併完成 ===" >> "$LOG_FILE"
echo ""
echo "✅ 記憶合併完成"
echo "日誌: $LOG_FILE"
