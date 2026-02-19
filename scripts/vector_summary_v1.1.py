#!/usr/bin/env python3
"""
向量摘要完整流程 v1.1 - 簡化版
1. 文本切分 (Chunking)
2. 生成摘要 (Summarization) - 使用 Ollama
3. 向量化 (Embedding) - 使用 Ollama
4. 建立關聯 (Linking) - 存入 JSON 檔案
5. 檢索 (Retrieval)
"""

import os
import json
import subprocess
import requests

NOTION_API_KEY = "***REMOVED***"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
VECTOR_DB_PATH = os.path.expanduser("~/Desktop/vector-db/")

# 建立目錄
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# ============================================================
# 步驟 1: 文本切分 (Chunking)
# ============================================================

def chunk_text(text, chunk_size=300):
    """將長文本切分成多個區塊"""
    chunks = []
    # 按句子切分
    sentences = text.replace('。', '。|').replace('！', '！|').replace('？', '？|').replace('\n', ' ').split('|')
    
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
    
    return [c for c in chunks if c]  # 移除空字符串

# ============================================================
# 步驟 2: 生成摘要 (Summarization)
# ============================================================

def generate_summary(chunk):
    """使用 Ollama 生成摘要"""
    prompt = f"請用30字以內精簡摘要以下內容的核心概念：\n\n{chunk}"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=60,
            shell=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()[:80]
    except Exception as e:
        print(f"   ⚠️ Ollama 不可用: {e}")
    
    # Fallback: 返回關鍵句
    lines = chunk.split('\n')
    for line in lines[:3]:
        if len(line) > 10:
            return line[:80]
    return chunk[:80]

# ============================================================
# 步驟 3: 向量化 (Embedding)
# ============================================================

def get_embedding(text):
    """使用 Ollama 獲取向量化"""
    try:
        # 嘗試使用 nomic-embed-text
        result = subprocess.run(
            ["ollama", "embeddings", "-p", text],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import re
            match = re.search(r'\[([-\d.,]+)\]', result.stdout)
            if match:
                return [float(x) for x in match.group(1).split(',')]
    except:
        pass
    
    # Fallback: 簡單 hash 向量
    vec = [0.0] * 128
    for i, c in enumerate(text[:128]):
        vec[i % 128] += ord(c)
    # 歸一化
    mag = sum(x*x for x in vec) ** 0.5
    if mag > 0:
        vec = [x/mag for x in vec]
    return vec

# ============================================================
# 步驟 4: 建立關聯 (Linking)
# ============================================================

def store_vectors(doc_id, title, chunks, summaries, source_text):
    """將向量存入 JSON 檔案"""
    
    vectors = []
    for i, (chunk, summary) in enumerate(zip(chunks, summaries)):
        embedding = get_embedding(summary)
        
        vectors.append({
            "doc_id": doc_id,
            "chunk_index": i,
            "summary": summary,
            "source_chunk": chunk[:200],
            "full_source": source_text,
            "embedding": embedding
        })
    
    # 儲存
    filepath = os.path.join(VECTOR_DB_PATH, f"{doc_id}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "title": title,
            "chunks": len(chunks),
            "vectors": vectors
        }, f, ensure_ascii=False, indent=2)
    
    return len(vectors)

# ============================================================
# 步驟 5: 檢索 (Retrieval)
# ============================================================

def cosine_similarity(a, b):
    """計算餘弦相似度"""
    dot = sum(x*y for x, y in zip(a, b))
    mag_a = sum(x*x for x in a) ** 0.5
    mag_b = sum(x*x for x in b) ** 0.5
    if mag_a * mag_b == 0:
        return 0
    return dot / (mag_a * mag_b)

def retrieve(query, top_k=3):
    """檢索相關內容"""
    
    query_embedding = get_embedding(query)
    results = []
    
    # 搜尋所有向量檔案
    for filename in os.listdir(VECTOR_DB_PATH):
        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(VECTOR_DB_PATH, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for vec in data.get('vectors', []):
            similarity = cosine_similarity(query_embedding, vec['embedding'])
            results.append({
                "doc_id": data.get('title', 'Unknown'),
                "summary": vec['summary'],
                "source_chunk": vec['source_chunk'],
                "similarity": similarity
            })
    
    # 排序並返回 top_k
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]

# ============================================================
# 主流程
# ============================================================

def process_page(page_id, title):
    """處理單個頁面"""
    print(f"\n{'='*50}")
    print(f"處理: {title}")
    print('='*50)
    
    # 1. 取得內容
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
        print("  ⚠️ 沒有內容")
        return None
    
    print(f"  原文長度: {len(full_text)} 字")
    
    # 2. 文本切分
    print(f"\n  📝 步驟1: 文本切分...")
    chunks = chunk_text(full_text, chunk_size=300)
    print(f"     → {len(chunks)} 個區塊")
    
    # 3. 生成摘要
    print(f"\n  📝 步驟2: 生成摘要 (LLM)...")
    summaries = []
    for i, chunk in enumerate(chunks):
        summary = generate_summary(chunk)
        summaries.append(summary)
        print(f"     Chunk {i+1}: {summary[:40]}...")
    
    # 4. 向量化 + 建立關聯
    print(f"\n  📝 步驟3+4: 向量化 + 儲存...")
    stored = store_vectors(page_id, title, chunks, summaries, full_text)
    print(f"     → 已儲存 {stored} 筆記錄")
    
    # 5. 更新 Notion
    vector_summary = " | ".join(summaries[:3])
    data = {
        "properties": {
            "向量摘要": {"rich_text": [{"text": {"content": vector_summary[:500]}}]},
            "向量狀態": {"select": {"name": "已向量化"}},
            "語義標籤": {"multi_select": [{"name": f"Chunk_{len(chunks)}"}]}
        }
    }
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
    
    return {"chunks": len(chunks), "summaries": len(summaries)}

def main():
    print("="*60)
    print("向量摘要完整流程 v1.1")
    print("1.文本切分→2.生成摘要→3.向量化→4.建立關聯→5.檢索")
    print("="*60)
    
    # 處理最新頁面
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, json={"page_size": 3})
    pages = response.json().get("results", [])
    
    for page in pages:
        page_id = page["id"]
        title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")
        
        # 跳過已處理的
        vector_status = page["properties"].get("向量狀態", {}).get("select", {})
        if vector_status and vector_status.get("name") == "已向量化":
            print(f"\n⏭️ 跳過: {title[:30]} (已向量化)")
            continue
        
        result = process_page(page_id, title)
        if result:
            print(f"\n✅ 完成: {title[:30]}")
    
    # 測試檢索
    print("\n" + "="*60)
    print("測試檢索")
    print("="*60)
    
    query = "什麼是向量摘要？"
    results = retrieve(query)
    
    if results:
        print(f"\n🔍 查詢: {query}")
        for i, r in enumerate(results, 1):
            print(f"\n  {i}. {r['doc_id'][:30]}")
            print(f"     摘要: {r['summary'][:50]}...")
            print(f"     相似度: {r['similarity']:.3f}")
    else:
        print("  ⚠️ 沒有結果")

if __name__ == "__main__":
    main()
