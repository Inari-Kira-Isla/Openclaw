#!/bin/bash
# Web Search 追蹤與反饋腳本
# 用法: ./track-search.sh "主題" "評分(1-5)" "備註"

SEARCH_LOG="/Users/ki/.openclaw/workspace/logs/web-search-usage.md"
TOPIC="$1"
SCORE="$2"
NOTE="$3"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

# 評估有效性
if [ "$SCORE" -ge 4 ]; then
    EFFECTIVENESS="✅ 高價值"
elif [ "$SCORE" -ge 2 ]; then
    EFFECTIVENESS="⚠️ 中價值"
else
    EFFECTIVENESS="❌ 低價值"
fi

# 記錄
echo "| $DATE $TIME | $TOPIC | $SCORE/5 | $EFFECTIVENESS | $NOTE |" >> "$SEARCH_LOG"

echo "✅ 已記錄: $TOPIC - $SCORE/5 - $EFFECTIVENESS"
echo ""
echo "今日記錄:"
tail -5 "$SEARCH_LOG"
