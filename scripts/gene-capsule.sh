#!/bin/bash
# Gene Capsule 管理腳本

CAPSULES_DIR="/Users/ki/.openclaw/workspace/memory/capsules"
INDEX_FILE="$CAPSULES_DIR/index.yaml"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

case "$1" in
  list)
    echo "=== Gene Capsules ==="
    ls -1 "$CAPSULES_DIR"/*.yaml | grep -v index.yaml | while read f; do
      id=$(basename "$f" .yaml)
      name=$(grep "^name:" "$f" | cut -d'"' -f2)
      type=$(grep "^type:" "$f" | cut -d'"' -f2)
      status=$(grep "^status:" "$f" | cut -d' ' -f2)
      echo -e "${GREEN}$id${NC} | $name | $type | $status"
    done
    ;;
    
  search)
    if [ -z "$2" ]; then
      echo "用法: $0 search <關鍵詞>"
      exit 1
    fi
    echo "=== 搜尋膠囊: $2 ==="
    grep -l "$2" "$CAPSULES_DIR"/*.yaml | while read f; do
      id=$(basename "$f" .yaml)
      name=$(grep "^name:" "$f" | cut -d'"' -f2)
      echo -e "${GREEN}$id${NC} | $name"
    done
    ;;
    
  show)
    if [ -z "$2" ]; then
      echo "用法: $0 show <膠囊ID>"
      exit 1
    fi
    cat "$CAPSULES_DIR/$2.yaml"
    ;;
    
  stats)
    echo "=== 膠囊統計 ==="
    count=$(ls -1 "$CAPSULES_DIR"/*.yaml 2>/dev/null | grep -v index.yaml | wc -l)
    echo "總膠囊數: $count"
    echo ""
    
    # 計算平均分數
    total_score=0
    for f in "$CAPSULES_DIR"/*.yaml; do
      [ "$f" = "$INDEX_FILE" ] && continue
      score=$(grep "^  success_rate:" "$f" 2>/dev/null | awk '{print $2}')
      if [ -n "$score" ]; then
        total_score=$(echo "$total_score + $score" | bc 2>/dev/null || echo "$total_score")
      fi
    done
    echo "平均成功率: $total_score"
    ;;
    
  *)
    echo "用法: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  list           列出所有膠囊"
    echo "  search <key>  搜尋膠囊"
    echo "  show <id>     顯示膠囊詳情"
    echo "  stats         顯示統計"
    ;;
esac
