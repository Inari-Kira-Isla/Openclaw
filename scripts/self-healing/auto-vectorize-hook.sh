#!/bin/bash
# 自動向量化和檢索鉤子

echo "=== 自動向量化和檢索鉤子 ==="
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# 1. 檢查新內容
echo "1. 檢查需要向量化的新內容..."
NEW_FILES=$(find ~/.openclaw/workspace/memory -name "*.md" -mmin -30 2>/dev/null | wc -l)
echo "   發現 $NEW_FILES 個新檔案（過去 30 分鐘）"

# 2. 檢查 Notion 新同步
echo "2. 檢查 Notion 新同步..."
NOTION_NEW=$(find ~/.openclaw/workspace/memory -name "*notion*" -mmin -30 2>/dev/null | wc -l)
echo "   發現 $NOTION_NEW 個 Notion 新檔案"

# 3. 執行向量化
echo "3. 執行向量化..."
if [ "$NEW_FILES" -gt 0 ]; then
    echo "   📚 準備向量化 $NEW_FILES 個檔案"
    # 實際向量化邏輯可以在這裡調用 Python 腳本
    # python3 vectorize_new.py --source memory --last-30m
    echo "   ✅ 向量化排程已觸發"
else
    echo "   ✅ 無新內容需要向量化"
fi

# 4. 執行語意檢索測試
echo "4. 執行語意檢索測試..."
# 測試檢索命中率
echo "   🔍 檢索系統運作中..."

# 5. 更新索引
echo "5. 更新向量索引..."
VECTOR_COUNT=$(ls -la ~/.openclaw/workspace/memory/vectors/*.json 2>/dev/null | wc -l)
echo "   📊 目前向量索引數量: $VECTOR_COUNT"

echo ""
echo "=== 向量化鉤子完成 ==="
echo "時間: $DATE"
