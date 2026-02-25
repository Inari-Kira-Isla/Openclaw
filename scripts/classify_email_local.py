#!/usr/bin/env python3
# Email 分類 - 使用本地 Ollama 模型

import os
import sys
import json
import subprocess

def classify_email(subject, content, model="llama3:latest"):
    prompt = f"""你是一個郵件分類助手。請根據以下郵件內容進行分類。

郵件標題: {subject}
郵件內容: {content}

請以 JSON 格式回覆分類結果：
{{"category": "分類", "priority": "優先級", "action": "動作"}}

分類: 重要/一般/促銷/垃圾/通知/待辦
優先級: 高/中/低"""

    try:
        # 呼叫 Ollama
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout
        
        # 嘗試提取 JSON
        import re
        match = re.search(r'\{[^}]+\}', output, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return data
        
        return {"raw": output[:200]}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    subject = sys.argv[1] if len(sys.argv) > 1 else "Test"
    content = sys.argv[2] if len(sys.argv) > 2 else "Test content"
    
    print("📧 郵件分類")
    print(f"標題: {subject}")
    print("---")
    
    result = classify_email(subject, content)
    
    if "error" in result:
        print(f"❌ 錯誤: {result['error']}")
    elif "category" in result:
        print("✅ 分類結果:")
        print(f"  類別: {result.get('category', 'N/A')}")
        print(f"  優先級: {result.get('priority', 'N/A')}")
        print(f"  動作: {result.get('action', 'N/A')}")
    else:
        print(result)
