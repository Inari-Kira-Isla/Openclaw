#!/bin/bash
echo "=== RAG 檢索效果測試 v2 ==="

TEST_QUERIES=(
  "閉環系統"
  "Kira 決策"
  "Neicheok 裁決"
  "Cynthia 知識庫"
  "Evolution 質疑"
  "Slime 學習"
  "社群營銷"
  "Notion 同步"
  "Session 清理"
  "向量檢索"
)

TOTAL=${#TEST_QUERIES[@]}
SUCCESS=0

for query in "${TEST_QUERIES[@]}"; do
  # Search in memory files
  RESULT=$(grep -l -i "$query" ~/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
  
  if [ "$RESULT" -gt 0 ]; then
    echo "✅ $query (找到 $RESULT 個檔案)"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "⚠️ $query"
  fi
done

echo ""
HIT_RATE=$((SUCCESS * 100 / TOTAL))
echo "檢索命中率: $HIT_RATE% ($SUCCESS/$TOTAL)"

if [ "$HIT_RATE" -ge 80 ]; then
  echo "✅ 檢索效果良好達標！"
else
  echo "⚠️ 還需要優化"
fi
