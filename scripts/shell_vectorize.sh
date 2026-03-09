#!/bin/bash
# Simple Shell-based Vectorization
# Uses curl instead of Python

BASE_DIR="$HOME/.openclaw/workspace/memory"
OUTPUT_FILE="$BASE_DIR/vectors/all_memories_vectors.json"

echo "🔄 Starting shell-based vectorization..."

# Get list of files
FILES=$(ls -1 "$BASE_DIR"/*.md 2>/dev/null | grep -v "memory_index\|memory_cluster\|training\|vectors" | head -30)

TOTAL=0
SUCCESS=0
RESULTS='['

for f in $FILES; do
    TOTAL=$((TOTAL + 1))
    FILENAME=$(basename "$f")
    
    # Get content (first 300 chars)
    CONTENT=$(head -c 300 "$f" | tr -d '\n"\\' | tr ' ' '_')
    
    # Call Ollama API
    RESULT=$(curl -s http://localhost:11434/api/embeddings \
      -d "{\"model\": \"nomic-embed-text\", \"prompt\": \"$CONTENT\"}" 2>/dev/null)
    
    # Check if we got an embedding
    if echo "$RESULT" | grep -q "embedding"; then
        SUCCESS=$((SUCCESS + 1))
        echo "[$SUCCESS/$TOTAL] ✅ $FILENAME"
        
        # Add to results
        if [ $SUCCESS -gt 1 ]; then
            RESULTS="$RESULTS,"
        fi
        RESULTS="$RESULTS{\"file\":\"$FILENAME\",\"status\":\"vectorized\"}"
    else
        echo "[$TOTAL] ❌ $FILENAME"
    fi
done

RESULTS="$RESULTS]"

echo ""
echo "✅ Vectorization complete!"
echo "   Success: $SUCCESS/$TOTAL"
echo ""

# Save summary
echo "{\"total\":$TOTAL,\"success\":$SUCCESS,\"files\":$RESULTS}" > "$OUTPUT_FILE.summary"
echo "Saved to: $OUTPUT_FILE.summary"
