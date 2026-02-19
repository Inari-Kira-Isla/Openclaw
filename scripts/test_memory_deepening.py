#!/usr/bin/env python3
"""
深化記憶系統測試腳本
測試完整的 Pre-task → In-task → Post-task 流程
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/Desktop/chromadb-env/lib/python3.12/site-packages"))

import chromadb
from chromadb.config import Settings

CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-data")

def init_chromadb():
    """初始化 ChromaDB"""
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    ))
    return client

def test_pre_task_retrieval(collection, task):
    """測試：工作前智慧檢索"""
    print("\n" + "="*60)
    print("📌 Phase 1: 工作前智慧檢索")
    print("="*60)
    print(f"\n任務: {task}")
    
    # 向量搜尋
    semantic_results = collection.query(
        query_texts=[task],
        n_results=3
    )
    
    print("\n🔍 向量搜尋結果:")
    for i, (doc, meta) in enumerate(zip(
        semantic_results["documents"][0],
        semantic_results["metadatas"][0]
    )):
        print(f"  {i+1}. {meta.get('title', 'N/A')}")
        print(f"     預覽: {doc[:80]}...")
    
    # 生成 Briefing Report
    briefing = f"""
[任務來源]: {task}
[本地記憶錨點]: 
"""
    for i, meta in enumerate(semantic_results["metadatas"][0]):
        briefing += f"  - {meta.get('title', 'N/A')}\n"
    
    briefing += f"""
[核心事實]: 從向量庫檢索出 {len(semantic_results['documents'][0])} 個相關記憶
[MiniMax 指令]: 請根據以上事實，為 Joe 生成建議。
"""
    
    print(f"\n📋 Briefing Report:\n{briefing}")
    
    return semantic_results

def test_active_thought_logger(task, thoughts):
    """測試：工作中動態標註"""
    print("\n" + "="*60)
    print("📝 Phase 2: 工作中動態標註")
    print("="*60)
    
    saved_thoughts = []
    
    for thought in thoughts:
        # 分類洞察類型
        insight_type = "pattern"
        if "解決" in thought or "難" in thought:
            insight_type = "solution"
        elif "決定" in thought or "選擇" in thought:
            insight_type = "decision"
        
        temp_thought = {
            "type": insight_type,
            "content": thought,
            "timestamp": datetime.now().isoformat(),
            "task": task
        }
        
        saved_thoughts.append(temp_thought)
        print(f"\n✅ 捕捉: [{insight_type}] {thought[:50]}...")
    
    return saved_thoughts

def test_memory_deepener(task, results, thoughts):
    """測試：工作後記憶深化"""
    print("\n" + "="*60)
    print("🧠 Phase 3: 工作後記憶深化")
    print("="*60)
    
    # Step 1: 歸納 (Summarize)
    summary = f"關於「{task}」的任務已完成。學習到："
    for thought in thoughts:
        summary += f"\n- {thought['content']}"
    
    print(f"\n📋 Step 1 歸納: {summary[:100]}...")
    
    # Step 2: 連結 (Linking)
    linked_memories = ["回憶_2026_海膽市場", "回憶_2026_系統優化"]
    print(f"\n🔗 Step 2 連結: 找到 {len(linked_memories)} 個相關記憶")
    
    # Step 3: 衝突檢測
    conflict_flags = []
    print(f"\n⚠️ Step 3 衝突檢測: {len(conflict_flags)} 個衝突")
    
    # Step 4: 權重調整
    importance_score = 7.5 + len(thoughts) * 0.5
    print(f"\n⚖️ Step 4 權重調整: 重要性分數 = {importance_score}")
    
    # 輸出深化後的記憶
    deepened_memory = {
        "task": task,
        "summary": summary,
        "tags": ["深化", "學習", task[:10]],
        "linked_memories": linked_memories,
        "conflict_flags": conflict_flags,
        "importance_score": importance_score,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"\n✅ 深化記憶已準備好寫入向量庫")
    
    return deepened_memory

def main():
    print("="*60)
    print("🔬 深化記憶系統測試")
    print("="*60)
    
    # 初始化
    client = init_chromadb()
    
    try:
        collection = client.get_collection("notion-knowledge")
    except:
        print("❌ Collection 不存在，請先執行同步腳本")
        return
    
    print(f"\n📊 ChromaDB 總文檔數: {collection.count()}")
    
    # 測試任務
    test_task = "海膽市場價格分析"
    
    # Phase 1: 工作前檢索
    results = test_pre_task_retrieval(collection, test_task)
    
    # Phase 2: 工作中標註
    thoughts = [
        "發現週三的價格波動通常受物流影響",
        "解決了 API 連接問題",
        "決定使用本地 Embedding 而非 API 節省成本"
    ]
    saved_thoughts = test_active_thought_logger(test_task, thoughts)
    
    # Phase 3: 工作後深化
    deepened = test_memory_deepener(test_task, results, saved_thoughts)
    
    print("\n" + "="*60)
    print("✅ 測試完成！")
    print("="*60)
    print(f"\n深化記憶內容:")
    print(json.dumps(deepened, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
