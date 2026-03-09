#!/bin/bash
# Notion 向量資料庫 Heartbeat 觸發腳本
# 輸出檢查結果作為 systemEvent 回覆

RESULT=$(python3 /Users/ki/.openclaw/workspace/scripts/check_notion_vector.py 2>&1)

# 擷取關鍵資訊
TOTAL=$(echo "$RESULT" | grep "總筆記數:" | sed 's/.*: //')
VECTORIZED=$(echo "$RESULT" | grep "已向量化:" | sed 's/.*: //')
PENDING=$(echo "$RESULT" | grep "待處理:" | sed 's/.*: //')

echo "📊 Notion 向量資料庫狀態"
echo ""
echo "總筆記數: $TOTAL"
echo "已向量化: $VECTORIZED"
echo "待處理: $PENDING"

# 如果有待處理，列出清單
if echo "$RESULT" | grep -q "待處理筆記:"; then
    echo ""
    echo "待處理筆記:"
    echo "$RESULT" | grep "^-" | head -5
fi
