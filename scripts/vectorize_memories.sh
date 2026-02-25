#!/bin/bash
# 向量化所有記憶和Skills
# 將記憶檔案轉為向量格式

MEMORY_DIR="/Users/ki/.openclaw/workspace/memory"
SKILLS_DIR="/Users/ki/.openclaw/workspace/skills"
OUTPUT_DIR="/Users/ki/.openclaw/workspace/memory/vectors"

mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "  記憶向量化工具"
echo "========================================"

# 1. 收集所有 md 檔案
echo ""
echo "📂 收集記憶檔案..."
MEMORY_FILES=$(find "$MEMORY_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
echo "   找到 $MEMORY_FILES 個記憶檔案"

# 2. 收集所有 Skills
echo ""
echo "📂 收集 Skills..."
SKILLS_FILES=$(find "$SKILLS_DIR" -name "SKILL.md" -type f 2>/dev/null | wc -l)
echo "   找到 $SKILLS_FILES 個 Skills"

# 3. 創建索引檔案
echo ""
echo "📝 建立索引..."

INDEX_FILE="$OUTPUT_DIR/index.md"

cat > "$INDEX_FILE" << 'EOF'
# 向量化索引

## 記憶檔案

| # | 檔案 | 日期 | 狀態 |
|---|------|------|------|
EOF

# 添加記憶檔案
i=1
find "$MEMORY_DIR" -name "*.md" -type f -newer "$OUTPUT_DIR/../2026-02-19.md" 2>/dev/null | while read f; do
    filename=$(basename "$f")
    echo "| $i | $filename | 2026-02-20 | ⏳ 待處理 |" >> "$INDEX_FILE"
    ((i++))
done

# 添加 Skills
echo "" >> "$INDEX_FILE"
echo "## Skills" >> "$INDEX_FILE"
echo "" >> "$INDEX_FILE"
echo "| # | Skill | 狀態 |" >> "$INDEX_FILE"
echo "|---|------|------|" >> "$INDEX_FILE"

i=1
find "$SKILLS_DIR" -name "SKILL.md" -type f 2>/dev/null | while read f; do
    skillname=$(dirname "$f" | xargs basename)
    echo "| $i | $skillname | ⏳ 待處理 |" >> "$INDEX_FILE"
    ((i++))
done

# 4. 建立向量格式
echo ""
echo "📦 建立向量格式..."

VECTOR_FILE="$OUTPUT_DIR/vectors.json"

cat > "$VECTOR_FILE" << 'EOF'
{
  "version": "1.0",
  "created": "2026-02-20",
  "documents": [
EOF

# 添加記憶到向量
first=true
find "$MEMORY_DIR" -name "*.md" -type f 2>/dev/null | while read f; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> "$VECTOR_FILE"
    fi
    
    filename=$(basename "$f")
    # 簡單提取標題
    title=$(head -1 "$f" | sed 's/# //')
    
    echo "    {" >> "$VECTOR_FILE"
    echo "      \"type\": \"memory\"," >> "$VECTOR_FILE"
    echo "      \"source\": \"$filename\"," >> "$VECTOR_FILE"
    echo "      \"title\": \"$title\"" >> "$VECTOR_FILE"
    echo -n "    }" >> "$VECTOR_FILE"
done

echo "" >> "$VECTOR_FILE"
echo "  ]" >> "$VECTOR_FILE"
echo "}" >> "$VECTOR_FILE"

# 5. 完成
echo ""
echo "========================================"
echo "✅ 向量化索引建立完成"
echo "========================================"
echo ""
echo "📁 輸出位置: $OUTPUT_DIR/"
echo "   - index.md (索引)"
echo "   - vectors.json (向量資料)"
echo ""
echo "📊 統計:"
echo "   - 記憶檔案: $MEMORY_FILES"
echo "   - Skills: $SKILLS_FILES"
echo ""
echo "⚠️ 注意: 需要執行實際向量化才能使用"
echo "   下一步: 使用 embedding 模型生成向量"
