#!/bin/bash
# 自動同步文章到 Notion

NOTION_DB="30aa1238f49d817c8163dd76d1309240"
NOTION_TOKEN="***REMOVED***"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"

# 找出最近 1 小時內修改的文章
RECENT_FILES=$(find $MEMORY_DIR -name "*.md" -type f -mmin -60)

if [ -z "$RECENT_FILES" ]; then
    echo "無新文章需要同步"
    exit 0
fi

for FILE in $RECENT_FILES; do
    # 提取標題（第一行 # 開頭的）
    TITLE=$(head -5 "$FILE" | grep "^# " | sed 's/^# //' | head -1)
    
    # 檢查是否已同步（通過標題查詢）
    CHECK=$(curl -s "https://api.notion.com/v1/databases/$NOTION_DB/query" \
        -H "Authorization: Bearer $NOTION_TOKEN" \
        -H "Notion-Version: 2022-06-28" \
        -d "{\"filter\": {\"property\": \"標題\", \"title\": {\"equals\": \"$TITLE\"}}}" | \
        python3 -c "import json,sys; d=json.load(sys.stdin); print('EXISTS' if d.get('results') else 'NEW')")
    
    if [ "$CHECK" = "NEW" ] && [ -n "$TITLE" ]; then
        echo "同步新文章: $TITLE"
        
        # 發送到 Notion
        curl -s -X POST "https://api.notion.com/v1/pages" \
            -H "Authorization: Bearer $NOTION_TOKEN" \
            -H "Content-Type: application/json" \
            -H "Notion-Version: 2022-06-28" \
            -d "{
                \"parent\": { \"database_id\": \"$NOTION_DB\" },
                \"properties\": {
                    \"標題\": { \"title\": [{ \"text\": { \"content\": \"$TITLE\" } }] },
                    \"來源\": { \"rich_text\": [{ \"text\": { \"content\": \"自動同步\" } }] },
                    \"向量狀態\": { \"select\": { \"name\": \"待處理\" } }
                }
            }" > /dev/null
        
        echo "✅ 已同步: $TITLE"
    fi
done
