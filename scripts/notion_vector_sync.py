#!/usr/bin/env python3
"""
Notion Vector Sync - 將 Notion 筆記同步到 ChromaDB
"""

import os
import sys

# 添加虛擬環境路徑
sys.path.insert(0, os.path.expanduser("~/Desktop/chromadb-env/lib/python3.12/site-packages"))

import chromadb
from chromadb.config import Settings
import json
from datetime import datetime

# Notion 資料
NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

# ChromaDB 設定
CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-data")

def init_chromadb():
    """初始化 ChromaDB"""
    os.makedirs(CHROMA_PATH, exist_ok=True)
    
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    ))
    
    return client

def create_collection(client, name="notion-knowledge"):
    """建立或取得 collection"""
    try:
        collection = client.get_collection(name)
        print(f"✅ 取得已有 collection: {name}")
    except:
        collection = client.create_collection(name)
        print(f"✅ 建立新 collection: {name}")
    
    return collection

def add_sample_data(collection):
    """新增範例資料"""
    sample_data = [
        {
            "id": "doc_001",
            "content": "海膽市場分析：2026年A級馬糞海膽供應穩定，價格區間在每公斤800-1200元之間。",
            "metadata": {"category": "海膽", "year": "2026", "source": "市場報告"}
        },
        {
            "id": "doc_002", 
            "content": "OpenClaw 架構：Muse-Core 是中央治理核心，負責任務協調與 Agent 管理。",
            "metadata": {"category": "AI", "year": "2026", "source": "系統架構"}
        },
        {
            "id": "doc_003",
            "content": "n8n 自動化：可用於監控 Notion 頁面變動，觸發向量更新流程。",
            "metadata": {"category": "系統", "year": "2026", "source": "工作流"}
        }
    ]
    
    for doc in sample_data:
        collection.add(
            ids=[doc["id"]],
            documents=[doc["content"]],
            metadatas=[doc["metadata"]]
        )
        print(f"✅ 新增文檔: {doc['id']}")
    
    return len(sample_data)

def query_similar(collection, query_text, n_results=3):
    """查詢相似文檔"""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results

def main():
    print("=" * 50)
    print("Notion Vector Sync - ChromaDB")
    print("=" * 50)
    
    # 初始化
    client = init_chromadb()
    collection = create_collection(client, "notion-knowledge")
    
    # 新增範例資料
    count = add_sample_data(collection)
    print(f"\n✅ 總共新增 {count} 筆資料")
    
    # 測試查詢
    print("\n" + "=" * 50)
    print("測試查詢：海膽市場")
    print("=" * 50)
    
    results = query_similar(collection, "海膽市場價格")
    
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"\n結果 {i+1}:")
        print(f"  內容: {doc}")
        print(f"  分類: {meta.get('category', 'N/A')}")
        print(f"  來源: {meta.get('source', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("✅ ChromaDB 設定完成！")
    print(f"資料儲存位置: {CHROMA_PATH}")
    print("=" * 50)

if __name__ == "__main__":
    main()
