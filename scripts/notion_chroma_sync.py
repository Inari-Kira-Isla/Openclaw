#!/usr/bin/env python3
"""
[DEPRECATED 2026-03-04] 已被 SQLite 本地方案取代，不再使用 Notion API。
Notion to ChromaDB Sync - 完整同步腳本
"""

import os

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
import sys
import json
import requests
from datetime import datetime

# 添加虛擬環境路徑
sys.path.insert(0, os.path.expanduser("~/Desktop/chromadb-env/lib/python3.12/site-packages"))

import chromadb
from chromadb.config import Settings

# Notion 設定
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

# ChromaDB 設定
CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-data")

def get_notion_pages():
    """從 Notion 取得所有頁面"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if "results" in data:
            all_pages.extend(data["results"])
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        else:
            print(f"Error: {data}")
            break
    
    return all_pages

def extract_page_content(page):
    """從 Notion 頁面提取內容"""
    page_id = page["id"]
    
    # 取得頁面內容
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    blocks = response.json().get("results", [])
    
    # 提取文字內容
    content = []
    for block in blocks:
        if "paragraph" in block:
            text = block["paragraph"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content.append(t["plain_text"])
    
    full_content = " ".join(content)
    
    # 取得標題
    title = "Untitled"
    if "properties" in page:
        for key, prop in page["properties"].items():
            if prop.get("type") == "title":
                title_list = prop.get("title", [])
                if title_list:
                    title = title_list[0].get("plain_text", "Untitled")
                break
    
    # 取得標籤
    tags = []
    if "properties" in page:
        for key, prop in page["properties"].items():
            if prop.get("type") == "multi_select":
                tags = [item["name"] for item in prop.get("multi_select", [])]
    
    return {
        "id": page_id,
        "title": title,
        "content": full_content[:2000],  # 限制長度
        "tags": tags,
        "url": page.get("url", "")
    }

def sync_to_chromadb():
    """同步 Notion 到 ChromaDB"""
    print("=" * 50)
    print("Notion → ChromaDB 同步")
    print("=" * 50)
    
    # 初始化 ChromaDB
    os.makedirs(CHROMA_PATH, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    ))
    
    # 取得或建立 collection
    try:
        collection = client.get_collection("notion-knowledge")
        print("✅ 取得已有 collection")
    except:
        collection = client.create_collection("notion-knowledge")
        print("✅ 建立新 collection")
    
    # 取得 Notion 頁面
    print("\n📥 取得 Notion 頁面...")
    pages = get_notion_pages()
    print(f"✅ 取得 {len(pages)} 個頁面")
    
    # 同步每個頁面
    synced = 0
    for i, page in enumerate(pages):
        try:
            content = extract_page_content(page)
            
            if content["content"]:  # 只同步有內容的頁面
                collection.upsert(
                    ids=[content["id"]],
                    documents=[content["content"]],
                    metadatas=[{
                        "title": content["title"],
                        "tags": ",".join(content["tags"]),
                        "url": content["url"]
                    }]
                )
                synced += 1
                print(f"  [{i+1}/{len(pages)}] 同步: {content['title'][:30]}...")
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\n✅ 同步完成！總共 {synced} 個頁面")
    
    # 顯示統計
    print("\n" + "=" * 50)
    print("📊 ChromaDB 統計")
    print("=" * 50)
    count = collection.count()
    print(f"總文檔數: {count}")
    
    return count

def query_vector(query_text, n=5):
    """查詢向量"""
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    ))
    collection = client.get_collection("notion-knowledge")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n
    )
    
    return results

if __name__ == "__main__":
    count = sync_to_chromadb()
    
    # 測試查詢
    print("\n" + "=" * 50)
    print("🔍 測試查詢")
    print("=" * 50)
    
    results = query_vector("AI 系統架構")
    
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"\n結果 {i+1}:")
        print(f"  標題: {meta.get('title', 'N/A')}")
        print(f"  內容: {doc[:100]}...")
    
    print("\n" + "=" * 50)
    print("✅ 同步完成！")
    print("=" * 50)
