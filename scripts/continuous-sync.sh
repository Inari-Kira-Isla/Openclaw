#!/bin/bash
# 持續同步 Pipeline

echo "=== 持續同步 Pipeline ==="

# 1. 檢查新 embeddings
echo "1. 檢查新 embeddings..."
NEW_COUNT=$(openclaw memory status 2>&1 | grep "Embedding cache" | awk '{print $3}')
echo "   新 embeddings: $NEW_COUNT"

# 2. 同步到 RAG
echo "2. 同步到 RAG..."
openclaw memory index --force 2>&1 | tail -5

# 3. 驗證
echo "3. 驗證同步..."
SYNCED=$(openclaw memory status 2>&1 | grep "chunks" | head -1 | awk '{print $5}')
echo "   已同步: $SYNCED"

echo ""
echo "=== 同步完成 ==="
