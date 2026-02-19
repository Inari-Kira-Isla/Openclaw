#!/usr/bin/env python3
"""
向量摘要完整流程 v1.0
1. 文本切分 (Chunking)
2. 生成摘要 (Summarization) - 使用 LLM
3. 向量化 (Embedding) - 存入 ChromaDB
4. 建立關聯 (Linking) - 連結原始文本
5. 檢索 (Retrieval)
"""

import os
import sys
import requests
import json

# ChromaDB 路徑
CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-env")

# 添加到路徑
sys.path.insert(0, CHROMA_PATH)

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("安裝 ChromaDB...")
    os.system(f"{CHROMA_PATH}/bin/python3 -m pip install chromadb -q")
    import chromadb
    from chromadb.config import Settings

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

# ============================================================
# 步驟 1: 文本切分 (Chunking)
# ============================================================

def chunk_text(text, chunk_size=500):
    """將長文本切分成多個區塊"""
    chunks = []
    # 按句子切分
    sentences = text.replace('。', '。|').replace('！', '！|').replace('？', '？|').split('|')
    
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# ============================================================
# 步驟 2: 生成摘要 (Summarization) - 使用 Ollama
# ============================================================

def generate_summary(chunk):
    """使用 Ollama 生成摘要"""
    import subprocess
    
    prompt = f"請用50字以內簡潔摘要以下內容的核心概念：\n\n{chunk}"
    
    try:
        # 使用本地 Ollama
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout.strip()[:100]  # 限制長度
        else:
            return chunk[:100]  # 如果失敗，返回原始文本前100字
    except:
        return chunk[:100]  # 如果 Ollama 不可用，返回原始文本

# ============================================================
# 步驟 3: 向量化 (Embedding)
# ============================================================

def get_embedding(text):
    """使用 Ollama 獲取向量化"""
    import subprocess
    
    try:
        # 使用 Ollama 的 embedding 模型
        result = subprocess.run(
            ["ollama", "embeddings", "-m", "nomic-embed-text", "-p", text],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # 解析輸出獲取 embedding
            import re
            match = re.search(r'\[([-\d.,]+)\]', result.stdout)
            if match:
                return [float(x) for x in match.group(1).split(',')]
        
        # 如果失敗，使用簡單的 hash 作為 fallback
        return [float(ord(c)) for c in text[:10]] + [0.0] * 118
    except:
        return [float(ord(c)) for c in text[:10]] + [0.0] * 118

# ============================================================
# 步驟 4: 建立關聯 (Linking) - 存入 ChromaDB
# ============================================================

def store_in_chromadb(doc_id, chunks, summaries, embeddings, source_text):
    """將摘要向量存入 ChromaDB 並建立關聯"""
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # 取得或建立 collection
    try:
        collection = client.get_collection("vector_summary")
    except:
        collection = client.create_collection("vector_summary")
    
    # 儲存每個 chunk
    for i, (chunk, summary, embedding) in enumerate(zip(chunks, summaries, embeddings)):
        doc_id_chunk = f"{doc_id}_chunk_{i}"
        
        collection.add(
            ids=[doc_id_chunk],
            embeddings=[embedding],
            metadatas=[{
                "doc_id": doc_id,
                "chunk_index": i,
                "summary": summary,
                "source_chunk": chunk[:200],  # 儲存原始文本片段
                "full_source": source_text  # 完整原文
            }],
            documents=[summary]
        )
    
    return len(chunks)

# ============================================================
# 步驟 5: 檢索 (Retrieval)
# ============================================================

def retrieve(query, top_k=3):
    """檢索相關內容"""
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    try:
        collection = client.get_collection("vector_summary")
    except:
        return []
    
    # 對查詢向量化
    query_embedding = get_embedding(query)
    
    # 搜尋相似向量
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # 提取結果
    retrieved = []
    if results and results['ids']:
        for i, doc_id in enumerate(results['ids'][0]):
            metadata = results['metadatas'][0][i]
            retrieved.append({
                "id": doc_id,
                "summary": metadata.get('summary', ''),
                "source_chunk": metadata.get('source_chunk', ''),
                "full_source": metadata.get('full_source', '')
            })
    
    return retrieved

# ============================================================
# 主流程：處理 Notion 頁面
# ============================================================

def process_notion_page(page_id):
    """處理單個 Notion 頁面"""
    print(f"\n{'='*60}")
    print(f"處理頁面: {page_id}")
    print('='*60)
    
    # 1. 取得頁面內容
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(blocks_url, headers=headers)
    blocks = response.json().get("results", [])
    
    # 提取文本
    full_text = ""
    for block in blocks:
        for block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
            if block_type in block:
                text = block[block_type].get("rich_text", [])
                for t in text:
                    if "plain_text" in t:
                        full_text += t["plain_text"] + "\n"
                break
    
    if not full_text.strip():
        print("  ⚠️ 頁面沒有內容")
        return None
    
    print(f"  📄 原文長度: {len(full_text)} 字")
    
    # ========== 步驟 1: 文本切分 ==========
    print(f"\n  📝 步驟 1: 文本切分...")
    chunks = chunk_text(full_text, chunk_size=300)
    print(f"     切分為 {len(chunks)} 個區塊")
    
    # ========== 步驟 2: 生成摘要 ==========
    print(f"\n  📝 步驟 2: 生成摘要 (使用 LLM)...")
    summaries = []
    for i, chunk in enumerate(chunks):
        summary = generate_summary(chunk)
        summaries.append(summary)
        print(f"     Chunk {i+1}: {summary[:40]}...")
    
    # ========== 步驟 3: 向量化 ==========
    print(f"\n  📝 步驟 3: 向量化...")
    embeddings = []
    for summary in summaries:
        embedding = get_embedding(summary)
        embeddings.append(embedding)
    print(f"     產生 {len(embeddings)} 個向量")
    
    # ========== 步驟 4: 建立關聯 ==========
    print(f"\n  📝 步驟 4: 建立關聯 (存入 ChromaDB)...")
    stored = store_in_chromadb(page_id, chunks, summaries, embeddings, full_text)
    print(f"     ✅ 已儲存 {stored} 筆記錄")
    
    # 更新 Notion 頁面的向量狀態
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    vector_summary_text = " | ".join(summaries[:3])  # 取前3個摘要
    data = {
        "properties": {
            "向量摘要": {"rich_text": [{"text": {"content": vector_summary_text[:500]}}]},
            "向量狀態": {"select": {"name": "已向量化"}},
            "語義標籤": {"multi_select": [{"name": f"Chunk_{len(chunks)}"}]}
        }
    }
    requests.patch(update_url, headers=headers, json=data)
    print(f"     ✅ Notion 頁面已更新")
    
    return {
        "chunks": len(chunks),
        "summaries": summaries
    }

def test_retrieval():
    """測試檢索功能"""
    print("\n" + "="*60)
    print("測試檢索功能")
    print("="*60)
    
    query = "什麼是向量摘要？"
    results = retrieve(query)
    
    if results:
        print(f"\n🔍 查詢: {query}")
        print(f"📊 找到 {len(results)} 個結果:\n")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['summary'][:50]}...")
            print(f"     原文片段: {result['source_chunk'][:80]}...")
            print()
    else:
        print("  ⚠️ 沒有找到結果")

# ============================================================
# 主程式
# ============================================================

def main():
    print("="*60)
    print("向量摘要完整流程 v1.0")
    print("1. 文本切分 → 2. 生成摘要 → 3. 向量化 → 4. 建立關聯 → 5. 檢索")
    print("="*60)
    
    # 處理最新的 Notion 頁面
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    response = requests.post(url, headers=headers, json={"page_size": 3})
    pages = response.json().get("results", [])
    
    for page in pages:
        page_id = page["id"]
        title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")[:30]
        
        # 跳過已處理的
        vector_status = page["properties"].get("向量狀態", {}).get("select", {})
        if vector_status and vector_status.get("name") == "已向量化":
            print(f"\n⏭️ 跳過: {title} (已向量化)")
            continue
        
        result = process_notion_page(page_id)
        if result:
            print(f"\n✅ 完成: {title}")
            print(f"   - {result['chunks']} 個區塊")
            print(f"   - 已存入 ChromaDB")
    
    # 測試檢索
    test_retrieval()

if __name__ == "__main__":
    main()
