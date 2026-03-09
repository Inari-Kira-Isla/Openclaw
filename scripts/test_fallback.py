#!/usr/bin/env python3
"""
本地模型調度系統 - 帶 Fallback 機制
測試版本
"""

import subprocess
import requests
import json
import os
import sys
from datetime import datetime

# 配置

# 模型配置
MODELS = {
    "llama3": {"name": "llama3", "type": "general"},
    "mistral": {"name": "mistral", "type": "reasoning"},
    "codellama": {"name": "codellama", "type": "coding"},
    "deepseek-coder": {"name": "deepseek-coder", "type": "coding"}
}

# 任務類型關鍵字
TASK_KEYWORDS = {
    "程式碼": ["程式", "代碼", "function", "def ", "class ", "import ", "python", "javascript"],
    "推理": ["分析", "推理", "邏輯", "為什麼", "怎麼", "如何解決", "比較"],
    "創意": ["寫", "創作", "故事", "文章", "部落格"]
}

def select_model(prompt):
    """選擇模型"""
    prompt_lower = prompt.lower()
    
    for task_type, keywords in TASK_KEYWORDS.items():
        if any(k in prompt_lower for k in keywords):
            if task_type == "程式碼":
                return "codellama", task_type
            elif task_type == "推理":
                return "mistral", task_type
            else:
                return "llama3", task_type
    
    return "llama3", "一般"

def generate_local(prompt, model_name):
    """使用本地模型生成"""
    print(f"\n🔄 使用本地模型: {model_name}")
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip(), "local"
    except Exception as e:
        print(f"❌ 本地模型錯誤: {e}")
    return None, "local_failed"

def generate_minimax(prompt):
    """使用 MiniMax"""
    print(f"\n🔄 使用 MiniMax 驗證")
    url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "MiniMax-M2.5",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"], "minimax"
    except Exception as e:
        print(f"❌ MiniMax 錯誤: {e}")
    return None, "minimax_failed"

def calculate_similarity(text1, text2):
    """計算相似度"""
    if not text1 or not text2:
        return 0
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words1 or not words2:
        return 0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)

def process_with_fallback(prompt):
    """帶 Fallback 的處理流程"""
    print("="*60)
    print("本地模型調度系統 - Fallback 測試")
    print("="*60)
    print(f"\n📝 輸入: {prompt[:50]}...")
    
    # 1. 選擇模型
    model_name, task_type = select_model(prompt)
    print(f"\n🎯 任務類型: {task_type}")
    print(f"🤖 選擇模型: {model_name}")
    
    # 2. 嘗試本地模型
    local_output, local_status = generate_local(prompt, model_name)
    
    # 3. Fallback 機制
    if local_status == "local_failed":
        print("\n⚠️ 本地模型失敗，Fallback 到 MiniMax")
        local_output, local_status = generate_minimax(prompt)
        if local_output:
            return local_output, local_status
    
    # 4. 需要驗證的任務
    need_verify = task_type in ["程式碼", "推理"]
    
    if need_verify and local_output:
        print(f"\n🔍 需要驗證: {task_type}")
        
        # MiniMax 驗證
        minimax_output, _ = generate_minimax(prompt)
        
        if minimax_output:
            similarity = calculate_similarity(local_output, minimax_output)
            print(f"\n📊 相似度: {similarity:.1%}")
            
            # 記錄結果
            result = {
                "timestamp": datetime.now().isoformat(),
                "task_type": task_type,
                "model": model_name,
                "local_output": local_output[:100],
                "minimax_output": minimax_output[:100],
                "similarity": similarity,
                "used": "local" if similarity > 0.7 else "minimax"
            }
            
            print(f"\n✅ 使用: {'本地模型' if similarity > 0.7 else 'MiniMax'}")
            
            return local_output if similarity > 0.7 else minimax_output, result["used"]
    
    # 5. 返回結果
    if local_output:
        print(f"\n✅ 直接返回本地結果")
        return local_output, "local_only"
    
    return "無法處理", "error"

# 測試
if __name__ == "__main__":
    test_prompts = [
        "你好，今天天氣怎麼樣？",
        "寫一個 Python 函數來計算斐波那契數列",
        "分析 AI 對未來工作的影響"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n\n{'#'*60}")
        print(f"# 測試 {i}: {prompt[:30]}...")
        print(f"{'#'*60}")
        
        result, source = process_with_fallback(prompt)
        print(f"\n📤 結果來源: {source}")
        print(f"📝 輸出: {result[:100] if result else '無'}...")
