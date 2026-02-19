#!/usr/bin/env python3
"""
ChromaDB 簡單測試 - 直接建立測試資料
"""

import os
import sys

sys.path.insert(0, os.path.expanduser("~/Desktop/chromadb-env/lib/python3.12/site-packages"))

import chromadb
from chromadb.config import Settings

CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-data")
os.makedirs(CHROMA_PATH, exist_ok=True)

# 初始化 client
client = chromadb.Client(Settings(
    persist_directory=CHROMA_PATH,
    anonymized_telemetry=False
))

# 建立 collection
collection = client.get_or_create_collection("notion-knowledge")

# 新增測試資料
test_docs = [
    {
        "id": "test_001",
        "content": "海膽市場分析：2026年A級馬糞海膽供應穩定，價格區間在每公斤800-1200元之間。主要產地為日本北海道和韓國。",
        "title": "海膽市場報告 2026",
        "tags": "海膽,市場,價格"
    },
    {
        "id": "test_002",
        "content": "OpenClaw 架構：Muse-Core 是中央治理核心，負責任務協調與 Agent 管理。支援多達 27 個 AI Agent。",
        "title": "OpenClaw 系統架構",
        "tags": "AI,系統,OpenClaw"
    },
    {
        "id": "test_003",
        "content": "n8n 自動化工作流：用於監控 Notion 頁面變動，觸發向量更新流程。可以設定定時同步。",
        "title": "n8n 工作流設定",
        "tags": "n8n,自動化,工作流"
    },
    {
        "id": "test_004",
        "content": "向量資料庫優化：使用 ChromaDB 進行本地向量儲存。支援語義檢索，提升 AI 理解能力。",
        "title": "ChromaDB 向量優化",
        "tags": "向量,資料庫,優化"
    },
    {
        "id": "test_005",
        "content": "Notion 筆記同步：將 Notion 筆記同步到本地向量資料庫。支援語義標籤自動生成。",
        "title": "Notion 同步設定",
        "tags": "Notion,同步,筆記"
    }
]

# 新增資料
for doc in test_docs:
    collection.upsert(
        ids=[doc["id"]],
        documents=[doc["content"]],
        metadatas=[{"title": doc["title"], "tags": doc["tags"]}]
    )
    print(f"✅ 新增: {doc['title']}")

print(f"\n📊 總文檔數: {collection.count()}")

# 測試查詢
print("\n" + "="*50)
queries = ["海膽價格", "AI 系統", "自動化工具"]

for query in queries:
    print(f"\n🔍 查詢: {query}")
    results = collection.query(query_texts=[query], n_results=3)
    
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        similarity = 1 - results["distances"][0][i]
        print(f"  {i+1}. {meta['title']} (相似度: {similarity:.2%})")

print("\n✅ 測試完成!")
