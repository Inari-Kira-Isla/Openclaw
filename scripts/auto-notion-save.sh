#!/bin/bash
# 自動儲存文章到 Notion 鉤子 (修復版)

MEMORY_DIR="$HOME/.openclaw/workspace/memory"
NOTION_DB="30aa1238f49d817c8163dd76d1309240"
NOTION_TOKEN="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"
NOTION_VERSION="2025-09-03"

echo "=== 🚀 自動 Notion 儲存鉤子 ==="

# 取得要處理的檔案
if [ -n "$1" ]; then
    TARGET_FILE="$1"
else
    TARGET_FILE=$(find "$MEMORY_DIR" -name "*.md" -type f -mmin -30 | head -1)
fi

if [ -z "$TARGET_FILE" ] || [ ! -f "$TARGET_FILE" ]; then
    echo "❌ 無新文章"
    exit 0
fi

echo "📂 處理: $(basename "$TARGET_FILE")"

# 提取標題
TITLE=$(grep -m1 "^# " "$TARGET_FILE" | sed 's/^# //')
[ -z "$TITLE" ] && TITLE=$(basename "$TARGET_FILE" .md)
echo "📝 標題: $TITLE"

# 讀取內容 (去除 frontmatter)
CONTENT=$(sed -n '/^---$/,/^---$/d;p' "$TARGET_FILE")

# 建立 JSON payload
PAYLOAD=$(cat <<EOF
{
  "parent": {"database_id": "$NOTION_DB"},
  "properties": {
    "標題": {"title": [{"text": {"content": "$TITLE"}}]},
    "來源": {"rich_text": [{"text": {"content": "auto-save"}}]},
    "日期": {"date": {"start": "$(date +%Y-%m-%d)"}}
  }
}
EOF
)

# 建立頁面
RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: $NOTION_VERSION" \
    -d "$PAYLOAD")

PAGE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)

if [ -z "$PAGE_ID" ]; then
    echo "❌ 建立頁面失敗"
    echo "$RESPONSE"
    exit 1
fi

echo "✅ 頁面建立: $PAGE_ID"

# 構建區塊
BLOCKS="["
while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    if [[ "$line" =~ ^### ]]; then
        BLOCKS+=$(printf '{"type":"heading_3","heading_3":{"rich_text":[{"type":"text","text":{"content":"%s"}}]}},' "${line:4}")
    elif [[ "$line" =~ ^## ]]; then
        BLOCKS+=$(printf '{"type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":"%s"}}]}},' "${line:3}")
    elif [[ "$line" =~ ^#\  ]]; then
        BLOCKS+=$(printf '{"type":"heading_1","heading_1":{"rich_text":[{"type":"text","text":{"content":"%s"}}]}},' "${line:2}")
    else
        ESCAPED=$(echo "$line" | sed 's/\\/\\\\/g; s/"/\\"/g')
        BLOCKS+=$(printf '{"type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"%s"}}]}},' "$ESCAPED")
    fi
done <<< "$CONTENT"
BLOCKS="${BLOCKS%,}]"

# 發送區塊
curl -s -X PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: $NOTION_VERSION" \
    -d "$BLOCKS" > /dev/null

echo "✅ 內容已同步"
echo "🔗 https://notion.so/$PAGE_ID"
echo "=== ✅ 完成 ==="
