#!/usr/bin/env python3
"""
Ollama 模型預熱服務
保持模型在內存中，減少加載時間
"""

import requests
import time
import threading
from typing import List

OLLAMA_URL = "http://localhost:11434"

# 預熱的模型列表（按優先順序）
WARM_MODELS = [
    "deepseek-coder:1.3b",  # 最快 - 優先預熱
    "llama3",               # 日常使用
]

def prewarm_model(model_name: str) -> bool:
    """預熱單個模型"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": "hi",
                "stream": False
            },
            timeout=60
        )
        return response.status_code == 200
    except Exception as e:
        print(f"❌ {model_name}: {e}")
        return False

def keep_warm(model_name: str, interval: int = 300):
    """定時觸發模型保持熱度"""
    while True:
        prewarm_model(model_name)
        time.sleep(interval)

def main():
    print("🚀 開始模型預熱...")
    
    # 優先預熱快速模型
    for model in WARM_MODELS:
        print(f"預熱 {model}...")
        if prewarm_model(model):
            print(f"✅ {model} 預熱成功")
    
    print("✅ 預熱完成！")

if __name__ == "__main__":
    main()
