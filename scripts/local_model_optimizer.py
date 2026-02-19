#!/usr/bin/env python3
"""
本地模型優化系統 - MiniMax 驗證反饋
"""

import subprocess
import requests
import json
import os
from datetime import datetime

# 配置
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
VECTOR_DB_PATH = os.path.expanduser("~/Desktop/vector-db/")
FEEDBACK_FILE = os.path.expanduser("~/Desktop/local-model-feedback.json")

# 模型選擇
MODELS = {
    "llama3": "llama3",
    "mistral": "mistral",
    "codellama": "codellama",
    "deepseek-coder": "deepseek-coder"
}

def generate_local(prompt, model="llama3"):
    """使用本地模型生成"""
    try:
        result = subprocess.run(
            ["ollama", "run", MODELS.get(model, model), prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"本地模型錯誤: {e}")
    return None

def generate_minimax(prompt):
    """使用 MiniMax 驗證"""
    if not MINIMAX_API_KEY:
        return None
    
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
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"MiniMax 錯誤: {e}")
    return None

def calculate_similarity(text1, text2):
    """簡單相似度計算"""
    if not text1 or not text2:
        return 0
    
    # 簡單字詞重疊率
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0
    
    intersection = words1 & words2
    union = words1 | words2
    
    return len(intersection) / len(union)

def process_task(prompt, task_type="general", primary_model="llama3"):
    """處理任務並驗證"""
    print(f"\n{'='*50}")
    print(f"任務類型: {task_type}")
    print(f"使用模型: {primary_model}")
    print(f"{'='*50}")
    
    # 1. 本地模型生成
    print("\n1. 本地模型生成中...")
    local_output = generate_local(prompt, primary_model)
    
    if not local_output:
        print("本地模型失敗，切換到 MiniMax")
        return generate_minimax(prompt), "minimax_fallback"
    
    print(f"本地輸出: {local_output[:100]}...")
    
    # 2. MiniMax 驗證 (複雜任務)
    need_verify = task_type in ["程式碼", "複雜推理", "分析"]
    
    if need_verify:
        print("\n2. MiniMax 驗證中...")
        minimax_output = generate_minimax(prompt)
        
        if minimax_output:
            similarity = calculate_similarity(local_output, minimax_output)
            print(f"相似度: {similarity:.2%}")
            
            # 記錄反饋
            record_feedback(task_type, primary_model, local_output, minimax_output, similarity)
            
            if similarity < 0.7:
                print("⚠️ 相似度低，返回 MiniMax 結果")
                return minimax_output, "verified_minimax"
            
            return local_output, "verified_local"
    
    return local_output, "local_only"

def record_feedback(task_type, model, local_output, minimax_output, similarity):
    """記錄反饋"""
    feedback = {
        "timestamp": datetime.now().isoformat(),
        "task_type": task_type,
        "model": model,
        "similarity": similarity,
        "local_length": len(local_output),
        "minimax_length": len(minimax_output) if minimax_output else 0
    }
    
    # 讀取現有記錄
    feedbacks = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            feedbacks = json.load(f)
    
    feedbacks.append(feedback)
    
    # 保存
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)
    
    print(f"\n📝 反饋已記錄: {similarity:.2%}")

def weekly_report():
    """每週報告"""
    if not os.path.exists(FEEDBACK_FILE):
        print("無反饋數據")
        return
    
    with open(FEEDBACK_FILE, 'r') as f:
        feedbacks = json.load(f)
    
    if not feedbacks:
        return
    
    # 統計
    total = len(feedbacks)
    avg_similarity = sum(f["similarity"] for f in feedbacks) / total
    
    by_model = {}
    for f in feedbacks:
        model = f["model"]
        if model not in by_model:
            by_model[model] = []
        by_model[model].append(f["similarity"])
    
    print("\n" + "="*50)
    print("每週模型報告")
    print("="*50)
    print(f"總驗證次數: {total}")
    print(f"平均相似度: {avg_similarity:.2%}")
    print("\n各模型表現:")
    for model, scores in by_model.items():
        avg = sum(scores) / len(scores)
        print(f"  {model}: {avg:.2%} ({len(scores)}次)")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            weekly_report()
        else:
            prompt = " ".join(sys.argv[1:])
            result, source = process_task(prompt)
            if result:
                print(f"\n結果來源: {source}")
                print(f"輸出: {result[:200] if len(result) > 200 else result}...")
            else:
                print("\n結果: 無輸出")
    else:
        print("用法:")
        print("  python local_model_optimizer.py <prompt>")
        print("  python local_model_optimizer.py --report")
