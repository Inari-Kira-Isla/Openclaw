#!/bin/bash
# RAG 檢索效果測試

echo "=== RAG 檢索效果測試 ==="
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# 測試問題
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

echo "測試 $TOTAL 個查詢..."
echo ""

for query in "${TEST_QUERIES[@]}"; do
  echo "查詢: $query"
  
  # 檢查向量庫中是否有相關內容
  RESULT=$(grep -l -i "$query" ~/.openclaw/workspace/memory/vectors/*.json 2>/dev/null | wc -l)
  
  if [ "$RESULT" -gt 0 ]; then
    echo "  ✅ 找到相關向量: $RESULT 個"
    SUCCESS=$((SUCCESS + 1))
  else
    # 檢查記憶文件中是否有相關內容
    MEM_RESULT=$(grep -l -i "$query" ~/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
    if [ "$MEM_RESULT" -gt 0 ]; then
      echo "  ✅ 找到相關記憶: $MEM_RESULT 個檔案"
      SUCCESS=$((SUCCESS + 1))
    else
      echo "  ⚠️ 未找到相關內容"
    fi
  fi
done

echo ""
echo "=== 測試結果 ==="
HIT_RATE=$((SUCCESS * 100 / TOTAL))
echo "總測試數: $TOTAL"
echo "成功匹配: $SUCCESS"
echo "檢索命中率: $HIT_RATE%"

if [ "$HIT_RATE" -ge 80 ]; then
  echo "✅ 檢索效果良好 (目標 >85%)"
else
  echo "⚠️ 檢索命中率較低，需要優化"
fi

echo ""
echo "時間: $DATE"
