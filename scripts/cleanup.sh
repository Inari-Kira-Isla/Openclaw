#!/bin/bash
# OpenClaw Cleanup Script
# 清理暫存，釋放空間

echo "🧹 OpenClaw 清理開始..."
echo "========================"

# 1. Docker 清理
echo ""
echo "1. Docker 清理..."
docker system prune -f --volumes 2>/dev/null
docker builder prune -f 2>/dev/null

# 2. Temp files
echo ""
echo "2. 暫存檔案清理..."
rm -rf /tmp/claude-* 2>/dev/null
rm -rf /tmp/*.md 2>/dev/null

# 3. Ollama 清理 (保留主要模型)
echo ""
echo "3. Ollama 模型..."
# 顯示使用空間
ollama list

# 4. OpenClaw logs
echo ""
echo "4. OpenClaw 日誌..."
find ~/.openclaw/logs -name "*.log" -mtime +7 -delete 2>/dev/null

# 5. 向量資料庫優化
echo ""
echo "5. 向量資料庫..."
# 清理舊的向量緩存
rm -rf ~/.openclaw/vectors/*/cache 2>/dev/null

echo ""
echo "========================"
echo "✅ 清理完成！"

# 顯示最終空間
echo ""
echo "📊 Docker 空間："
docker system df
