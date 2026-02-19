#!/bin/bash
# Notion Sync Script (使用 curl)
# 版本: v1.1
# 修正 Database ID

NOTION_API_KEY="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"
# 正確的 Database ID - v1.1 修正
DATABASE_ID="30aa1238f49d817c8163dd76d1309240"
NOTION_VERSION="2025-09-03"

echo "========================================"
echo "Notion Sync Script v1.1"
echo "========================================"
echo "Database ID: $DATABASE_ID"
echo ""

# 測試連接
TEST_RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: $NOTION_VERSION" \
  -d "{
    \"parent\": {\"database_id\": \"$DATABASE_ID\"},
    \"properties\": {
      \"標題\": {\"title\": [{\"text\": {\"content\": \"測試筆記\"}}]},
      \"類型\": {\"select\": {\"name\": \"系統架構\"}},
      \"狀態\": {\"select\": {\"name\": \"已完成\"}}
    }
  }")

if echo "$TEST_RESPONSE" | grep -q '"id"'; then
    echo "✅ 連接測試成功！"
    PAGE_ID=$(echo "$TEST_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "   Page ID: $PAGE_ID"
    
    # 刪除測試頁面
    curl -s -X DELETE "https://api.notion.com/v1/blocks/$PAGE_ID" \
      -H "Authorization: Bearer $NOTION_API_KEY" \
      -H "Notion-Version: $NOTION_VERSION" > /dev/null
    echo "   (測試頁面已刪除)"
else
    echo "❌ 連接測試失敗"
    echo "$TEST_RESPONSE"
fi

echo ""
echo "使用方式:"
echo "  ./sync_to_notion.sh sync <markdown_file.md>"
echo ""
echo "範例:"
echo "  ./sync_to_notion.sh sync ~/notes/my_note.md"
