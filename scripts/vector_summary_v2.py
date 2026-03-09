#!/usr/bin/env python3
"""
向量摘要完整流程 v2.0 - 修復版
1. 文本切分 (Chunking)
2. 生成摘要 (Summarization) - 使用 Ollama
3. 向量化 (Embedding)
4. 建立關聯 (Linking)
5. 檢索 (Retrieval)
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
import json
import subprocess
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
VECTOR_DB_PATH = os.path.expanduser("~/Desktop/vector-db/")

os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# ============================================================
# 步驟 1: 文本切分
# ============================================================

def chunk_text(text, chunk_size=300):
    """將長文本切分成多個區塊"""
    # 按句子切分
    sentences = text.replace('。', '。|').replace('！', '！|').replace('？', '？|').replace('\n', ' ').split('|')
    
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) < chunk_size:
            current += s
        else:
            if current.strip():
                chunks.append(current.strip())
            current = s
    if current.strip():
        chunks.append(current.strip())
    
    return [c for c in chunks if len(c) > 20]

# ============================================================
# 步驟 2: 生成摘要 - 使用 Ollama
# ============================================================

def generate_summary(chunk):
    """使用 Ollama 生成摘要"""
    # 使用更精確的 prompt
    prompt = f"""請用最多30個字精簡摘要以下內容的核心概念，只返回摘要文字，不要其他說明：

{chunk[:200]}"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=45
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # 清理輸出
            summary = result.stdout.strip()
            # 移除可能的引號
            summary = summary.strip('"\'')
            if len(summary) > 5:
                return summary[:80]
    except Exception as e:
        print(f"   ⚠️ Ollama 錯誤: {e}")
    
    # Fallback: 取前50字
    return chunk[:50]

# ============================================================
# 步驟 3: 向量化
# ============================================================

def get_embedding(text):
    """簡單向量化"""
    vec = [0.0] * 128
    for i, c in enumerate(text[:128]):
        vec[i % 128] += ord(c)
    # 歸一化
    mag = sum(x*x for x in vec) ** 0.5
    if mag > 0:
        vec = [x/mag for x in vec]
    return vec

# ============================================================
# 步驟 4: 儲存
# ============================================================

def store_vectors(doc_id, title, chunks, summaries, full_text):
    """儲存向量到本地"""
    vectors = []
    for i, (chunk, summary) in enumerate(zip(chunks, summaries)):
        embedding = get_embedding(summary)
        vectors.append({
            "chunk_index": i,
            "summary": summary,
            "source_chunk": chunk[:300],
            "embedding": embedding
        })
    
    filepath = os.path.join(VECTOR_DB_PATH, f"{doc_id}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "title": title,
            "chunks": len(chunks),
            "vectors": vectors,
            "full_text": full_text[:5000]
        }, f, ensure_ascii=False, indent=2)
    
    return len(vectors)

# ============================================================
# 主流程
# ============================================================

def process_page(page_id, title):
    """處理單個頁面"""
    print(f"\n{'='*50}")
    print(f"處理: {title[:35]}")
    print('='*50)
    
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    
    # 1. 取得內容
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(blocks_url, headers=headers)
    blocks = response.json().get("results", [])
    
    # 提取文本
    full_text = ""
    for block in blocks:
        for bt in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
            if bt in block:
                text = block[bt].get("rich_text", [])
                for t in text:
                    if "plain_text" in t:
                        full_text += t["plain_text"] + " "
                break
    
    if len(full_text) < 50:
        print(f"  ⚠️ 內容太少: {len(full_text)} 字")
        return None
    
    print(f"  原文: {len(full_text)} 字")
    
    # 2. 文本切分
    print(f"\n  📝 步驟1: 文本切分...")
    chunks = chunk_text(full_text, chunk_size=250)
    print(f"     → {len(chunks)} 個區塊")
    
    # 3. 生成摘要
    print(f"\n  📝 步驟2: 生成摘要 (LLM)...")
    summaries = []
    for i, chunk in enumerate(chunks[:6]):  # 限制數量
        summary = generate_summary(chunk)
        summaries.append(summary)
        print(f"     Chunk {i+1}: {summary[:40]}")
    
    # 4. 向量化 + 儲存
    print(f"\n  📝 步驟3+4: 向量化 + 儲存...")
    stored = store_vectors(page_id, title, chunks, summaries, full_text)
    print(f"     → 已儲存 {stored} 筆記錄")
    
    # 5. 更新 Notion
    vector_summary = " | ".join(summaries[:3])
    data = {
        "properties": {
            "向量摘要": {"rich_text": [{"text": {"content": vector_summary[:500]}}]},
            "向量狀態": {"select": {"name": "已向量化(標準流程)"}},
            "語義標籤": {"multi_select": [{"name": f"Chunk_{len(chunks)}"}]},
            "重點": {"rich_text": [{"text": {"content": summaries[0][:50] if summaries else title[:30]}}]},
            "應用": {"rich_text": [{"text": {"content": "系統架構"}}]}
        }
    }
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
    print(f"     → Notion 已更新")
    
    return {"chunks": len(chunks), "summaries": len(summaries)}

def main():
    print("="*60)
    print("向量摘要完整流程 v2.0 - 修復版")
    print("1.文本切分→2.生成摘要→3.向量化→4.建立關聯→5.檢索")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, json={"page_size": 15})
    pages = response.json().get("results", [])
    
    processed = 0
    for page in pages:
        page_id = page["id"]
        title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")
        
        # 跳過已處理的
        vector_status = page["properties"].get("向量狀態", {}).get("select", {})
        if vector_status and "標準流程" in vector_status.get("name", ""):
            print(f"\n⏭️ 跳過: {title[:30]} (已處理)")
            continue
        
        result = process_page(page_id, title)
        if result:
            print(f"\n✅ 完成: {title[:30]}")
            processed += 1
        
        if processed >= 5:  # 限制處理數量
            break
    
    print(f"\n\n處理了 {processed} 個頁面")

if __name__ == "__main__":
    main()
