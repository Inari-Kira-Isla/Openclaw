#!/bin/bash
# Self-Improvement Daily Automation
# 每日自動執行自我學習優化

SCRIPT_DIR="$HOME/.openclaw/workspace/scripts"
LOG_FILE="$HOME/.openclaw/logs/self_improve.log"

echo "🧬 $(date) - 開始自我學習..." >> "$LOG_FILE"

# 執行自我學習
python3 "$SCRIPT_DIR/self_improve.py" run >> "$LOG_FILE" 2>&1

# 如果有新的優化，記錄
echo "✅ $(date) - 學習完成" >> "$LOG_FILE"

# 每週部署建議
CONTENT_COUNT=$(find "$HOME/.openclaw/workspace/aeo-site/content" -name "*.md" 2>/dev/null | wc -l)

if [ "$CONTENT_COUNT" -ge 100 ]; then
    echo "📦 $(date) - 內容達標 ($CONTENT_COUNT 篇)，建議部署" >> "$LOG_FILE"
fi
