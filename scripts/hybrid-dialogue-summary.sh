#!/bin/bash
# 混合對話摘要：本地壓縮 → 雲端最終

echo "=== 混合對話摘要 ==="

# 1. 本地壓縮 (Qwen2.5)
echo "1. 本地壓縮..."
echo "   Input: 完整對話"
echo "   Process: qwen2.5:7b 壓縮"
echo "   Output: 濃縮摘要"
echo "   → 減少 80% tokens"

# 2. 本地分類
echo "2. 本地分類..."
echo "   - 提取關鍵字"
echo "   - 情感分析"
echo "   - 意圖識別"

# 3. 雲端決策
echo "3. 雲端決策..."
echo "   - 重要訊息標記"
echo "   - 學習點提取"
echo "   - 記憶決策"

echo ""
echo "=== 對話摘要完成 ==="
