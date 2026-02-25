#!/usr/bin/env python3
"""
Email 本地分類器 - 使用 deepseek-coder:1.3b
快速、免費、離線
"""

import json
import subprocess
import os

MODEL = "deepseek-coder:1.3b"  # 776MB, 最快

def classify_email(subject: str, content: str) -> dict:
    """使用本地模型分類郵件"""
    
    prompt = f"""Subject: {subject}
Content: {content}

分類這個郵件，只需要回答以下格式:
CATEGORY|Priority
例如: important|high

分類:
- important (重要)
- general (一般)  
- promotion (促銷)
- spam (垃圾)
- todo (待辦)
- notification (通知)

Priority: high/medium/low

回答:"""

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout.strip()
        
        # 解析結果
        parts = output.split("|")
        if len(parts) >= 2:
            return {
                "category": parts[0].strip().lower(),
                "priority": parts[1].strip().lower(),
                "raw": output
            }
        
        return {"category": "general", "priority": "medium", "raw": output}
        
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "category": "general", "priority": "medium"}
    except Exception as e:
        return {"error": str(e), "category": "general", "priority": "medium"}

def main():
    import sys
    
    # 測試
    test_emails = [
        ("安全性快訊", "Google 帳戶登入異常"),
        ("促銷優惠", "全場半價優惠僅限今日"),
        ("Newsletter", "本週技術新聞"),
    ]
    
    print("📧 Email 本地分類器")
    print("=" * 40)
    print(f"模型: {MODEL}")
    print("=" * 40)
    
    for subject, content in test_emails:
        print(f"\n標題: {subject}")
        result = classify_email(subject, content)
        
        if "error" in result:
            print(f"❌ 錯誤: {result['error']}")
        else:
            print(f"✅ 分類: {result.get('category', 'N/A')} | 優先級: {result.get('priority', 'N/A')}")

if __name__ == "__main__":
    main()
