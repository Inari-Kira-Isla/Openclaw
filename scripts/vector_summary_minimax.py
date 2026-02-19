#!/usr/bin/env python3
"""
向量摘要 - MiniMax 版本
用 MiniMax 生成高質量摘要
"""

import requests
import json

# MiniMax API
MINIMAX_API_KEY = "Your API Key"
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def generate_summary_minimax(chunk):
    """使用 MiniMax 生成摘要"""
    url = f"{MINIMAX_BASE_URL}/text/chatcompletion_pro"
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""你是一個專業的文本摘要專家。請用 30 字以內精簡摘要以下內容的核心概念，只返回摘要文字，不要其他說明：

{chunk[:200]}"""
    
    data = {
        "model": "MiniMax-M2.5",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()[:80]
    except Exception as e:
        print(f"   MiniMax 錯誤: {e}")
    
    # Fallback
    return chunk[:50]

def chunk_text(text, chunk_size=250):
    sentences = text.replace('。', '。|').replace('！', '！|').replace('？', '？|').replace('\n', ' ').split('|')
    chunks, current = [], ''
    for s in sentences:
        if len(current) + len(s) < chunk_size:
            current += s
        else:
            if current.strip(): chunks.append(current.strip())
            current = s
    if current.strip(): chunks.append(current.strip())
    return [c for c in chunks if len(c) > 20]

def process_page(page_id, title):
    """處理頁面"""
    print(f"\n處理: {title[:30]}")
    
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    
    # 取得內容
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(blocks_url, headers=headers)
    blocks = response.json().get("results", [])
    
    full_text = ""
    for block in blocks:
        for bt in ["paragraph", "heading_1", "heading_2", "heading_3"]:
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
    chunks = chunk_text(full_text)
    print(f"  切分為 {len(chunks)} 區塊")
    
    # MiniMax 生成摘要
    print("  使用 MiniMax 生成摘要...")
    summaries = []
    for i, chunk in enumerate(chunks[:6]):
        summary = generate_summary_minimax(chunk)
        summaries.append(summary)
        print(f"    Chunk {i+1}: {summary[:40]}")
    
    # 更新 Notion
    vector_summary = " | ".join(summaries[:3])
    data = {
        "properties": {
            "向量摘要": {"rich_text": [{"text": {"content": vector_summary[:500]}}]},
            "向量狀態": {"select": {"name": "已向量化(MiniMax)"}},
            "語義標籤": {"multi_select": [{"name": f"Chunk_{len(chunks)}"}]},
            "重點": {"rich_text": [{"text": {"content": summaries[0][:50] if summaries else title[:30]}}]}
        }
    }
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
    
    print("  ✅ 完成")
    return len(chunks)

def main():
    print("="*50)
    print("向量摘要 - MiniMax 版本")
    print("="*50)
    
    # 測試
    test_text = "向量摘要是一種優化資料檢索的進階技術。它不是直接將原始長文本轉為向量，而是先將文本進行摘要化，再將這份摘要轉化為向量存入資料庫。"
    
    print("\n測試 MiniMax 摘要:")
    summary = generate_summary_minimax(test_text)
    print(f"  結果: {summary}")
    
    # 處理最新頁面
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, json={"page_size": 3})
    pages = response.json().get("results", [])
    
    for page in pages:
        title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")
        vs = page["properties"].get("向量狀態", {})
        status = vs.get("select", {}).get("name", "") if vs else ""
        
        if "MiniMax" not in status:
            process_page(page["id"], title)
            break

if __name__ == "__main__":
    main()
