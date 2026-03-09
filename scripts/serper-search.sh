#!/bin/bash
# Serper Web Search Script
# 用法: ./serper-search.sh "關鍵詞" [數量]

API_KEY="***REMOVED***"
QUERY="$1"
COUNT="${2:-5}"

if [ -z "$QUERY" ]; then
    echo "用法: $0 <關鍵詞> [數量]"
    exit 1
fi

# URL encode the query
ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

# API 調用
response=$(curl -s "https://google.serper.dev/search?q=$ENCODED_QUERY&num=$COUNT" \
    -H "X-API-Key: $API_KEY")

# 解析結果
echo "$response" | python3 -c "
import json, sys

data = json.load(sys.stdin)
results = data.get('organic', [])

print(f'搜尋結果: $QUERY\n')
print('='*50)

for i, r in enumerate(results[:$COUNT], 1):
    title = r.get('title', 'N/A')[:60]
    url = r.get('url', 'N/A')
    snippet = r.get('snippet', 'N/A')[:100]
    print(f'{i}. {title}')
    print(f'   {snippet}...')
    print(f'   🔗 {url}')
    print()
"
