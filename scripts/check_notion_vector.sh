#!/bin/bash
# Notion 向量資料庫檢查腳本
# 檢查 Notion AI Agent 系統架構學習筆記 資料庫狀態

export NOTION_API_KEY="***REMOVED***"
DB_ID="30aa1238f49d817c8163dd76d1309240"

echo "========================================"
echo "  Notion 向量資料庫檢查"
echo "========================================"

# 查詢資料庫
RESULT=$(curl -s -X POST "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 100}')

# 統計 - 使用 Python 處理
echo "$RESULT" | python3 << 'PYEOF'
import json
import sys

d = json.load(sys.stdin)
results = d.get('results', [])

total = len(results)
pending = 0
vectorized = 0

for r in results:
    props = r.get('properties', {})
    if not props:
        continue
    status = props.get('向量狀態', {})
    if not status:
        continue
    status_name = status.get('select', {}).get('name', '')
    if status_name == '待處理':
        pending += 1
    elif '已向量化' in status_name:
        vectorized += 1

print(f"總筆記數:{total}")
print(f"已向量化:{vectorized}")
print(f"待處理:{pending}")

if total > 0:
    percent = int(vectorized * 100 / total)
    print(f"進度:{percent}%")
PYEOF

echo ""
echo "========================================"
