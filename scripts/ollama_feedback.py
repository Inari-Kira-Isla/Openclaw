#!/usr/bin/env python3
"""
Ollama 反饋學習系統
追蹤檢索準確率，讓 Ollama 學習並優化
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/Desktop/chromadb-env/lib/python3.12/site-packages"))

import chromadb
from chromadb.config import Settings

CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-data")

def init_feedback_db():
    """初始化反饋資料庫"""
    os.makedirs(CHROMA_PATH, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    ))
    
    # 建立反饋 collection
    try:
        feedback = client.get_collection("retrieval_feedback")
        print("✅ 取得已有反饋資料庫")
    except:
        feedback = client.create_collection("retrieval_feedback")
        print("✅ 建立新反饋資料庫")
    
    return client, feedback

def log_retrieval(feedback, query, results, relevance_scores):
    """
    記錄檢索結果與相關性評分
    
    relevance_scores: [
        {"doc_id": "xxx", "relevant": True/False, "rating": 1-5}
    ]
    """
    entry = {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "results_count": len(results),
        "relevant_count": sum(1 for r in relevance_scores if r.get("relevant", False)),
        "avg_rating": sum(r.get("rating", 0) for r in relevance_scores) / len(relevance_scores) if relevance_scores else 0
    }
    
    feedback.add(
        ids=[f"log_{datetime.now().timestamp()}"],
        documents=[str(entry)],
        metadatas=[{
            "query": query,
            "timestamp": entry["timestamp"],
            "relevant": entry["relevant_count"],
            "rating": entry["avg_rating"]
        }]
    )
    
    return entry

def get_popular_tags(feedback, limit=10):
    """分析熱門標籤"""
    # 獲取所有反饋
    all_data = feedback.get()
    
    tag_counts = {}
    for meta in all_data.get("metadatas", []):
        query = meta.get("query", "")
        # 簡單關鍵詞提取
        words = query.split()
        for word in words:
            if len(word) > 2:
                tag_counts[word] = tag_counts.get(word, 0) + 1
    
    # 排序
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_tags[:limit]

def analyze_performance(feedback):
    """分析檢索效能"""
    all_data = feedback.get()
    
    if not all_data.get("metadatas"):
        return {
            "total_queries": 0,
            "avg_relevant": 0,
            "avg_rating": 0,
            "popular_queries": []
        }
    
    total = len(all_data["metadatas"])
    total_relevant = sum(m.get("relevant", 0) for m in all_data["metadatas"])
    total_rating = sum(m.get("rating", 0) for m in all_data["metadatas"])
    
    # 熱門查詢
    query_counts = {}
    for m in all_data["metadatas"]:
        q = m.get("query", "")
        query_counts[q] = query_counts.get(q, 0) + 1
    
    popular = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_queries": total,
        "avg_relevant": total_relevant / total if total > 0 else 0,
        "avg_rating": total_rating / total if total > 0 else 0,
        "popular_queries": popular
    }

def improve_retrieval(feedback):
    """根據反饋優化檢索"""
    print("\n" + "="*60)
    print("🧠 Ollama 學習與優化")
    print("="*60)
    
    # 1. 效能分析
    perf = analyze_performance(feedback)
    print(f"\n📊 效能報告:")
    print(f"  總查詢數: {perf['total_queries']}")
    print(f"  平均相關: {perf['avg_relevant']:.1f}")
    print(f"  平均評分: {perf['avg_rating']:.2f}/5")
    
    if perf['popular_queries']:
        print(f"\n🔥 熱門查詢:")
        for q, c in perf['popular_queries']:
            print(f"  - {q} ({c}次)")
    
    # 2. 熱門標籤
    tags = get_popular_tags(feedback)
    if tags:
        print(f"\n🏷️ 熱門標籤:")
        for tag, count in tags:
            print(f"  - {tag} ({count}次)")
    
    # 3. 優化建議
    print(f"\n💡 優化建議:")
    if perf['avg_rating'] < 3:
        print("  ⚠️ 評分較低，建議：")
        print("  - 增加訓練數據")
        print("  - 調整向量模型參數")
        print("  - 增加語義標籤")
    else:
        print("  ✅ 檢索效能良好")
    
    return perf

def add_sample_feedback(feedback):
    """新增範例反饋數據"""
    samples = [
        {
            "query": "海膽市場價格",
            "results": ["doc1", "doc2", "doc3"],
            "relevance": [
                {"doc_id": "doc1", "relevant": True, "rating": 5},
                {"doc_id": "doc2", "relevant": True, "rating": 4},
                {"doc_id": "doc3", "relevant": False, "rating": 2}
            ]
        },
        {
            "query": "AI 系統架構",
            "results": ["doc4", "doc5"],
            "relevance": [
                {"doc_id": "doc4", "relevant": True, "rating": 5},
                {"doc_id": "doc5", "relevant": True, "rating": 5}
            ]
        },
        {
            "query": "n8n 工作流",
            "results": ["doc6"],
            "relevance": [
                {"doc_id": "doc6", "relevant": True, "rating": 4}
            ]
        }
    ]
    
    for sample in samples:
        log_retrieval(feedback, sample["query"], sample["results"], sample["relevance"])
        print(f"✅ 記錄反饋: {sample['query']}")

def main():
    print("="*60)
    print("📈 Ollama 反饋學習系統")
    print("="*60)
    
    client, feedback = init_feedback_db()
    
    # 新增範例數據（首次運行）
    count = feedback.count()
    if count == 0:
        print("\n📝 新增範例反饋數據...")
        add_sample_feedback(feedback)
    
    # 效能分析與優化
    improve_retrieval(feedback)
    
    print("\n" + "="*60)
    print("✅ 反饋系統就緒！")
    print("="*60)

if __name__ == "__main__":
    main()
