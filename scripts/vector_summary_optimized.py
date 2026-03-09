#!/usr/bin/env python3
"""
向量摘要優化流程 v2.0 - 本地優先 + 雲端驗證
優化策略：
1. 本地壓縮 - 用 Ollama 初步壓縮輸入
2. 本地向量化 - 用本地 embedding 模型
3. 智能分流 - 簡單查詢本地處理，複雜問題才調用 MiniMax
4. 快取機制 - 避免重複處理
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
import requests
import json
import hashlib
from datetime import datetime

# ChromaDB 路徑
CHROMA_PATH = os.path.expanduser("~/Desktop/chromadb-env")
CACHE_PATH = os.path.expanduser("~/.openclaw/workspace/.vector_cache")

# 確保快取目錄存在
os.makedirs(CACHE_PATH, exist_ok=True)

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

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

# ============================================================
# 優化 1: 快取機制
# ============================================================

def get_cache_key(text):
    """生成快取 key"""
    return hashlib.md5(text.encode()).hexdigest()

def get_from_cache(key):
    """從快取讀取"""
    cache_file = os.path.join(CACHE_PATH, f"{key}.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
                # 檢查是否過期 (24小時)
                if datetime.now().timestamp() - data.get('timestamp', 0) < 86400:
                    return data.get('result')
        except:
            pass
    return None

def save_to_cache(key, result):
    """儲存到快取"""
    cache_file = os.path.join(CACHE_PATH, f"{key}.json")
    try:
        with open(cache_file, 'w') as f:
            json.dump({'timestamp': datetime.now().timestamp(), 'result': result}, f)
    except:
        pass

# ============================================================
# 步驟 1: 本地壓縮 (使用 Ollama)
# ============================================================

def local_compress(text, mode="summary"):
    """使用本地 Ollama 壓縮文本"""
    import subprocess
    
    if mode == "summary":
        prompt = f"用30字以內精簡摘要以下內容的核心概念：\n\n{text[:500]}"
    elif mode == "keywords":
        prompt = f"提取以下內容的3-5個關鍵詞，以逗號分隔：\n\n{text[:300]}"
    else:
        prompt = f"簡化以下內容：\n\n{text[:500]}"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=20
        )
        
        if result.returncode == 0:
            return result.stdout.strip()[:50]
    except:
        pass
    
    # Fallback: 簡單截取
    return text[:30] if len(text) > 30 else text

# ============================================================
# 步驟 2: 本地向量化 (使用 Ollama)
# ============================================================

def get_local_embedding(text):
    """使用本地 Ollama 獲取 embedding"""
    import subprocess
    import re
    
    try:
        result = subprocess.run(
            ["ollama", "embeddings", "-m", "nomic-embed-text", "-p", text],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            match = re.search(r'\[([-\d.,]+)\]', result.stdout)
            if match:
                return [float(x) for x in match.group(1).split(',')]
    except:
        pass
    
    # Fallback: 簡單 hash embedding
    return [float(ord(c)) / 255 for c in text[:128]] + [0.0] * max(0, 128 - len(text))

# ============================================================
# 步驟 3: 智能分流 (本地 vs 雲端)
# ============================================================

def should_use_cloud(query, local_results):
    """判斷是否需要調用雲端 MiniMax"""
    
    # 複雜信號
    complex_signals = [
        "分析", "比較", "評估", "建議", "詳細",
        "為什麼", "如何", "解釋", "推理"
    ]
    
    # 簡單信號
    simple_signals = [
        "什麼", "誰", "哪裡", "何時", "是什麼",
        "定義", "列出", "查詢"
    ]
    
    query_lower = query.lower()
    
    # 如果本地結果已經很匹配，不需要雲端
    if local_results and any(r.get('score', 0) > 0.8 for r in local_results):
        return False
    
    # 檢查複雜信號
    if any(signal in query_lower for signal in complex_signals):
        return True
    
    # 檢查簡單信號
    if any(signal in query_lower for signal in simple_signals):
        return False
    
    # 默認先用本地結果
    return len(local_results) == 0

# ============================================================
# 步驟 4: 雲端驗證 (MiniMax) - 僅在需要時調用
# ============================================================

def cloud_verify(summary, original_text):
    """使用 MiniMax 驗證/優化摘要"""
    # 這個函數只在你確定需要雲端處理時才會被調用
    # 目前標記為預留，未來可以啟用
    pass

# ============================================================
# 文本切分
# ============================================================

def chunk_text(text, chunk_size=300):
    """將長文本切分成多個區塊"""
    chunks = []
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
# 主流程：優化版向量摘要
# ============================================================

def process_notion_page_optimized(page_id):
    """優化版處理流程"""
    print(f"\n{'='*60}")
    print(f"處理頁面: {page_id} (優化版)")
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
    
    # 檢查快取
    cache_key = get_cache_key(full_text)
    cached = get_from_cache(cache_key)
    if cached:
        print(f"  ⚡ 使用快取結果")
        return cached
    
    # ========== 步驟 1: 本地壓縮 ==========
    print(f"\n  📝 步驟 1: 本地壓縮 (Ollama)...")
    chunks = chunk_text(full_text, chunk_size=300)
    print(f"     切分為 {len(chunks)} 個區塊")
    
    # ========== 步驟 2: 本地生成摘要 ==========
    print(f"\n  📝 步驟 2: 本地生成摘要...")
    summaries = []
    for i, chunk in enumerate(chunks):
        # 使用快取 key
        chunk_cache = get_cache_key(chunk)
        chunk_cached = get_from_cache(chunk_cache)
        
        if chunk_cached:
            summary = chunk_cached
        else:
            summary = local_compress(chunk, mode="summary")
            save_to_cache(chunk_cache, summary)
        
        summaries.append(summary)
        print(f"     Chunk {i+1}: {summary[:40]}...")
    
    # ========== 步驟 3: 本地向量化 ==========
    print(f"\n  📝 步驟 3: 本地向量化...")
    embeddings = []
    for summary in summaries:
        embedding = get_local_embedding(summary)
        embeddings.append(embedding)
    print(f"     產生 {len(embeddings)} 個向量")
    
    # ========== 步驟 4: 存入 ChromaDB ==========
    print(f"\n  📝 步驟 4: 存入 ChromaDB...")
    store_in_chromadb(page_id, chunks, summaries, embeddings, full_text)
    
    # ========== 步驟 5: 更新 Notion ==========
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    vector_summary_text = " | ".join(summaries[:3])
    data = {
        "properties": {
            "向量摘要": {"rich_text": [{"text": {"content": vector_summary_text[:500]}}]},
            "向量狀態": {"select": {"name": "已向量化(優化版)"}},
            "語義標籤": {"multi_select": [{"name": f"Chunk_{len(chunks)}"}]}
        }
    }
    requests.patch(update_url, headers=headers, json=data)
    print(f"     ✅ Notion 已更新")
    
    # 儲存結果到快取
    result = {"chunks": len(chunks), "summaries": summaries}
    save_to_cache(cache_key, result)
    
    return result

def store_in_chromadb(doc_id, chunks, summaries, embeddings, source_text):
    """將摘要向量存入 ChromaDB"""
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    try:
        collection = client.get_collection("vector_summary_optimized")
    except:
        collection = client.create_collection("vector_summary_optimized")
    
    for i, (chunk, summary, embedding) in enumerate(zip(chunks, summaries, embeddings)):
        doc_id_chunk = f"{doc_id}_chunk_{i}"
        
        collection.add(
            ids=[doc_id_chunk],
            embeddings=[embedding],
            metadatas=[{
                "doc_id": doc_id,
                "chunk_index": i,
                "summary": summary,
                "source_chunk": chunk[:200],
                "full_source": source_text
            }],
            documents=[summary]
        )
    
    return len(chunks)

# ============================================================
# 優化版檢索流程
# ============================================================

def retrieve_optimized(query, top_k=3):
    """
    優化版檢索：
    1. 本地 embedding 匹配
    2. 智能分流 - 簡單查詢直接返回，複雜才調用雲端
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    try:
        collection = client.get_collection("vector_summary_optimized")
    except:
        # 嘗試舊 collection
        try:
            collection = client.get_collection("vector_summary")
        except:
            return []
    
    # 對查詢向量化 (本地)
    print(f"\n  🔍 本地 embedding 匹配...")
    query_embedding = get_local_embedding(query)
    
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
            distance = results['distances'][0][i] if 'distances' in results else 0
            retrieved.append({
                "id": doc_id,
                "summary": metadata.get('summary', ''),
                "source_chunk": metadata.get('source_chunk', ''),
                "full_source": metadata.get('full_source', ''),
                "score": 1 - distance  # 轉換距離為相似度
            })
    
    # 智能分流決策
    print(f"  📊 匹配分數: {retrieved[0]['score']:.2f}" if retrieved else "  ⚠️ 無結果")
    
    if should_use_cloud(query, retrieved):
        print(f"  ☁️ 複雜查詢，建議調用 MiniMax 深度處理")
        # 這裡可以擴展為調用雲端
    else:
        print(f"  ✅ 簡單查詢，本地處理即可")
    
    return retrieved

# ============================================================
# 主程式
# ============================================================

def main():
    print("="*60)
    print("向量摘要優化流程 v2.0")
    print("本地優先 + 智能分流 + 快取機制")
    print("="*60)
    
    # 測試檢索
    query = "什麼是向量摘要？"
    print(f"\n🔍 測試檢索: {query}")
    results = retrieve_optimized(query)
    
    if results:
        print(f"\n📊 找到 {len(results)} 個結果:")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r['summary'][:50]}... (匹配度: {r['score']:.2f})")
    else:
        print("  ⚠️ 沒有找到結果 (需要先處理 Notion 頁面)")
        
    # 處理 Notion 頁面
    print("\n" + "="*60)
    print("處理 Notion 頁面...")
    print("="*60)
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    response = requests.post(url, headers=headers, json={"page_size": 3})
    pages = response.json().get("results", [])
    
    for page in pages:
        page_id = page["id"]
        title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")[:30]
        
        # 跳過已處理的
        vector_status = page["properties"].get("向量狀態", {}).get("select", {})
        if vector_status and "已向量化" in vector_status.get("name", ""):
            print(f"\n⏭️ 跳過: {title} ({vector_status.get('name')})")
            continue
        
        result = process_notion_page_optimized(page_id)
        if result:
            print(f"\n✅ 完成: {title}")
            print(f"   - {result['chunks']} 個區塊")
            print(f"   - 已存入 ChromaDB (優化版)")

if __name__ == "__main__":
    main()
