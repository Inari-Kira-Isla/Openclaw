#!/usr/bin/env python3
"""
Ollama Semantic Tagging - 檢索測試腳本
測試語義標籤對檢索精準度的提升
"""

import os
import sys

# 添加虛擬環境路徑
sys.path.insert(0, os.path.expanduser("~/Desktop/chromadb-env/lib/python3.12/site-packages"))

import chromadb
from chromadb.config import Settings
import json
from datetime import datetime

# ChromaDB 設定
CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-data")

def init_chromadb():
    """初始化 ChromaDB"""
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    ))
    return client

def get_collection(client, name="notion-knowledge"):
    """取得 collection"""
    return client.get_collection(name)

def test_semantic_search(collection, queries):
    """測試語義檢索"""
    results = []
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"🔍 查詢: {query}")
        print('='*50)
        
        # 執行檢索
        search_results = collection.query(
            query_texts=[query],
            n_results=5
        )
        
        # 整理結果
        query_result = {
            "query": query,
            "results": []
        }
        
        for i, (doc, meta, dist) in enumerate(zip(
            search_results["documents"][0],
            search_results["metadatas"][0],
            search_results["distances"][0]
        )):
            # 計算相似度 (distance 越低越相似)
            similarity = 1 - dist
            
            print(f"\n結果 {i+1}:")
            print(f"  標題: {meta.get('title', 'N/A')}")
            print(f"  相似度: {similarity:.2%}")
            print(f"  標籤: {meta.get('tags', 'N/A')}")
            print(f"  內容預覽: {doc[:100]}...")
            
            query_result["results"].append({
                "title": meta.get('title', 'N/A'),
                "similarity": similarity,
                "tags": meta.get('tags', 'N/A'),
                "content_preview": doc[:150]
            })
        
        results.append(query_result)
    
    return results

def test_keyword_vs_semantic(collection):
    """對比關鍵字 vs 語義檢索"""
    print("\n" + "="*60)
    print("🔬 關鍵字 vs 語義檢索 對比測試")
    print("="*60)
    
    # 測試查詢
    test_queries = [
        "海膽市場價格",
        "AI 系統架構",
        "n8n 自動化工作流",
        "記憶向量優化"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"🔍 查詢: {query}")
        print('='*50)
        
        # 語義檢索
        semantic_results = collection.query(
            query_texts=[query],
            n_results=3
        )
        
        print("\n📊 語義檢索結果:")
        for i, (doc, meta) in enumerate(zip(
            semantic_results["documents"][0],
            semantic_results["metadatas"][0]
        )):
            similarity = 1 - semantic_results["distances"][0][i]
            print(f"  {i+1}. {meta.get('title', 'N/A')} (相似度: {similarity:.2%})")

def generate_report(results):
    """生成測試報告"""
    report = []
    report.append("="*60)
    report.append("📊 檢索測試報告")
    report.append("="*60)
    report.append(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"總測試數: {len(results)}")
    report.append("")
    
    for result in results:
        report.append(f"\n🔍 查詢: {result['query']}")
        report.append("-"*40)
        
        for i, r in enumerate(result['results']):
            report.append(f"  {i+1}. {r['title']}")
            report.append(f"     相似度: {r['similarity']:.2%}")
            report.append(f"     標籤: {r['tags']}")
    
    return "\n".join(report)

def main():
    print("="*60)
    print("🔬 Ollama 語義標籤 - 檢索測試")
    print("="*60)
    
    # 初始化
    client = init_chromadb()
    collection = get_collection(client)
    
    # 顯示統計
    count = collection.count()
    print(f"\n📊 ChromaDB 統計:")
    print(f"  總文檔數: {count}")
    
    # 測試查詢
    test_queries = [
        "海膽市場價格趨勢",
        "AI Agent 系統架構",
        "Notion 筆記同步",
        "OpenClaw 工作流",
        "向量資料庫優化"
    ]
    
    # 執行測試
    results = test_semantic_search(collection, test_queries)
    
    # 對比測試
    test_keyword_vs_semantic(collection)
    
    # 生成報告
    report = generate_report(results)
    print("\n" + report)
    
    # 儲存報告
    report_path = os.path.expanduser("~/Desktop/chromadb-data/search-test-report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 報告已儲存: {report_path}")

if __name__ == "__main__":
    main()
