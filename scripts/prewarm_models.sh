#!/bin/bash
# 模型預熱腳本
# 用途：定時預熱 Ollama 模型，減少首次加載時間

# 設定要預熱的模型（按優先順序）
MODELS=(
  "deepseek-coder:1.3b"  # 最快，先預熱
  "llama3"                # 日常使用
  "mistral"               # 備用
)

LOG_FILE="/tmp/ollama_prewarm.log"

echo "=== 模型預熱開始: $(date) ===" >> $LOG_FILE

for MODEL in "${MODELS[@]}"; do
  echo "預熱模型: $MODEL" >> $LOG_FILE
  
  # 發送請求預熱
  curl -s http://localhost:11434/api/generate \
    -d "{\"model\": \"$MODEL\", \"prompt\": \"hello\", \"stream\": false}" >> $LOG_FILE 2>&1
  
  if [ $? -eq 0 ]; then
    echo "✅ $MODEL 預熱成功" >> $LOG_FILE
  else
    echo "❌ $MODEL 預熱失敗" >> $LOG_FILE
  fi
done

echo "=== 預熱完成: $(date) ===" >> $LOG_FILE
echo "完成"
