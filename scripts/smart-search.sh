#!/bin/bash
# Smart Web Search - 智能搜尋
# 自動選擇最佳 API

# 配置
YOU_KEY="ydc-sk-012c54cca1816737-aC1gwULfPnTDet57Kd0pe1Yqd7qEWPvQ-70b0f8e7"
SERPER_KEY="e453bc1a8492931b36d78e6fe2d6bbcd8a14cd2b"

search() {
    local QUERY="$1"
    local COUNT="${2:-5}"
    
    # URL encode
    ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")
    
    # 使用 Serper (品質較好)
    echo "🔍 使用 Serper..."
    response=$(curl -s "https://google.serper.dev/search?q=$ENCODED_QUERY&num=$COUNT" \
        -H "X-API-Key: $SERPER_KEY")
    
    echo "$response" | python3 -c "
import json, sys
data = json.load(sys.stdin)
results = data.get('organic', [])
print('='*50)
for i, r in enumerate(results[:$COUNT], 1):
    print(f\"{i}. {r.get('title', 'N/A')[:60]}\")
    print(f\"   {r.get('snippet', 'N/A')[:80]}...\")
    print('')
"
}

# 執行
if [ -z "$1" ]; then
    echo "用法: $0 <關鍵詞> [數量]"
    exit 1
fi

search "$1" "${2:-5}"
