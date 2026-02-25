#!/bin/bash
# Email 分類腳本 - 使用本地 Ollama 模型

# 設定
MODEL="llama3:latest"
EMAIL_SUBJECT="${1:-Test Email}"
EMAIL_CONTENT="${2:-Test content}"

#  Prompt
PROMPT="你是一個郵件分類助手。請根據以下郵件內容進行分類。

郵件標題: $EMAIL_SUBJECT
郵件內容: $EMAIL_CONTENT

請以 JSON 格式回覆分類結果：
{
  \"category\": \"分類類別\",
  \"priority\": \"優先級\",
  \"action\": \"建議動作\",
  \"summary\": \"簡短摘要\"
}

分類類別可選: 重要, 一般, 促銷, 垃圾, 通知, 待辦
優先級可選: 高, 中, 低
"

# 呼叫本地模型
echo "正在分析郵件..."
echo "標題: $EMAIL_SUBJECT"

RESPONSE=$(ollama run "$MODEL" "$PROMPT" 2>/dev/null)

echo "---"
echo "$RESPONSE"
echo "---"

# 嘗試提取 JSON
echo "$RESPONSE" | python3 -c "
import json,sys
import re

text = sys.stdin.read()
# 嘗試找到 JSON
match = re.search(r'\{[^}]+\}', text, re.DOTALL)
if match:
    try:
        data = json.loads(match.group())
        print('✅ 分類結果:')
        print(f'  類別: {data.get(\"category\", \"N/A\")}')
        print(f'  優先級: {data.get(\"priority\", \"N/A\")}')
        print(f'  動作: {data.get(\"action\", \"N/A\")}')
    except:
        print(text)
else:
    print(text)
" 2>/dev/null || echo "$RESPONSE"
