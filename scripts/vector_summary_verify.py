#!/usr/bin/env python3
"""
向量摘要 - MiniMax 驗證版
使用 MiniMax 驗證並改善 Ollama 生成的摘要
"""

import requests
import json
import subprocess
import os

NOTION_API_KEY = "***REMOVED***"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
VECTOR_DB_PATH = os.path.expanduser("~/Desktop/vector-db/")

# MiniMax API
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

def generate_summary_ollama(chunk):
    """使用 Ollama 生成摘要"""
    prompt = f"用30字以內摘要核心概念：{chunk[:200]}"
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True, text=True, timeout=45
        )
        if result.returncode == 0:
            return result.stdout.strip()[:80]
    except:
        pass
    return chunk[:50]

def generate_summary_minimax(chunk):
    """使用 MiniMax 生成更高質量摘要"""
    if not MINIMAX_API_KEY:
        return None
    
    url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""你是一個專業的文本摘要專家。請用 30 字以內精簡摘要以下內容的核心概念，只返回摘要文字：

{chunk[:250]}"""
    
    data = {
        "model": "MiniMax-M2.5",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()[:80]
    except:
        pass
    return None

def compare_summaries(ollama_sum, minimax_sum):
    """比較並選擇更好的摘要"""
    if not minimax_sum:
        return ollama_sum
    
    # MiniMax 通常更精煉
    if len(minimax_sum) < len(ollama_sum):
        return minimax_sum
    return ollama_sum

def process_page(page_id, title):
    """處理頁面"""
    print(f"\n處理: {title[:35]}")
    
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    
    # 取得內容
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(blocks_url, headers=headers)
    blocks = response.json().get("results", [])
    
    # 提取文本
    full_text = ""
    for block in blocks:
        for bt in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item"]:
            if bt in block:
                text = block[bt].get("rich_text", [])
                for t in text:
                    if "plain_text" in t:
                        full_text += t["plain_text"] + " "
                break
    
    if len(full_text) < 50:
        print("  內容不足")
        return None
    
    # 文本切分
    sentences = full_text.replace('。', '。|').replace('！', '！|').replace('？', '？|').replace('\n', ' ').split('|')
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) < 250:
            current += s
        else:
            if current.strip():
                chunks.append(current.strip())
            current = s
    if current.strip():
        chunks.append(current.strip())
    chunks = [c for c in chunks if len(c) > 20][:6]
    
    print(f"  區塊: {len(chunks)}")
    
    # 生成摘要
    summaries = []
    for i, chunk in enumerate(chunks):
        # 先用 Ollama
        ollama_sum = generate_summary_ollama(chunk)
        
        # 再用 MiniMax 驗證
        minimax_sum = generate_summary_minimax(chunk)
        
        # 選擇更好的
        best_sum = compare_summaries(ollama_sum, minimax_sum)
        summaries.append(best_sum)
        
        print(f"    Chunk {i+1}: {best_sum[:35]}")
        if minimax_sum:
            print(f"           (MiniMax: {minimax_sum[:25]})")
    
    # 更新 Notion
    vector_summary = " | ".join(summaries[:3])
    data = {
        "properties": {
            "向量摘要": {"rich_text": [{"text": {"content": vector_summary[:500]}}]},
            "向量狀態": {"select": {"name": "已向量化(Ollama+MiniMax)"}},
            "語義標籤": {"multi_select": [{"name": f"Chunk_{len(chunks)}"}]},
            "重點": {"rich_text": [{"text": {"content": summaries[0][:50] if summaries else title[:30]}}]}
        }
    }
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
    
    print(f"  ✅ 完成")
    return len(chunks)

def main():
    print("="*60)
    print("向量摘要 - Ollama + MiniMax 驗證版")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, json={"page_size": 10})
    pages = response.json().get("results", [])
    
    for page in pages:
        title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")
        vs = page["properties"].get("向量狀態", {})
        status = vs.get("select", {}).get("name", "") if vs else ""
        
        # 處理未處理或需要驗證的
        if "Ollama+MiniMax" not in status:
            process_page(page["id"], title)
            break

if __name__ == "__main__":
    main()
