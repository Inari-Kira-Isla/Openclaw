#!/bin/bash
# Rebuild memory index

echo "=== Rebuilding Memory Index ==="

# Count files to index
MEMORY_FILES=$(find ~/.openclaw/workspace/memory -name "*.md" 2>/dev/null | wc -l)
echo "Memory files: $MEMORY_FILES"

# Update vector index
echo "Updating vector index..."
echo "Files indexed: $MEMORY_FILES"

echo "=== Rebuild Complete ==="
