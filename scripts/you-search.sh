#!/bin/bash
# You.com Web Search Script
# 用法: ./you-search.sh "查詢關鍵詞"

API_KEY="ydc-sk-012c54cca1816737-aC1gwULfPnTDet57Kd0pe1Yqd7qEWPvQ-70b0f8e7"
QUERY="$1"
COUNT="${2:-5}"

if [ -z "$QUERY" ]; then
    echo "用法: $0 <關鍵詞> [數量]"
    exit 1
fi

# API 調用
response=$(curl -s "https://you.com/api/search?q=$QUERY&count=$COUNT" \
    -H "Authorization: Bearer $API_KEY")

# 解析結果
echo "$response" | python3 -c "
import json, sys

data = json.load(sys.stdin)
results = data.get('searchResults', {}).get('mainline', {}).get('third_party_search_results', [])

print(f'搜尋結果: {sys.argv[1]}\n' if len(sys.argv) > 1 else '搜尋結果:\n')
print('='*50)

for i, r in enumerate(results[:5], 1):
    print(f'{i}. {r.get(\"name\", \"N/A\")}')
    print(f'   {r.get(\"url\", \"N/A\")}')
    print(f'   {r.get(\"snippet\", \"N/A\")[:100]}...')
    print('')
" "$QUERY" 2>/dev/null

# 如果 python 解析失敗，直接輸出原始結果
if [ $? -ne 0 ]; then
    echo "$response"
fi
