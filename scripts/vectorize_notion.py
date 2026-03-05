#!/usr/bin/env python3
"""
[DEPRECATED 2026-03-04] 已被 SQLite 本地方案取代，不再使用 Notion API。
Notion 筆記向量化腳本
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
import requests

NOTION_KEY = os.environ.get("NOTION_API_KEY", "")
DB_ID = "30aa1238f49d817c8163dd76d1309240"

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_pending_pages():
    """獲取待處理的筆記"""
    response = requests.post(
        f"https://api.notion.com/v1/databases/{DB_ID}/query",
        headers=HEADERS,
        json={"page_size": 100}
    )
    pages = response.json()["results"]
    pending = []
    for p in pages:
        status = p.get("properties", {}).get("向量狀態", {}).get("select", {}).get("name", "")
        if status == "待處理":
            page_id = p["id"]
            title = p.get("properties", {}).get("標題", {}).get("title", [{}])[0].get("plain_text", "Untitled")
            pending.append({"id": page_id, "title": title})
    return pending

def get_page_content(page_id):
    """獲取頁面內容"""
    # 獲取 blocks
    response = requests.get(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=HEADERS,
        params={"page_size": 100}
    )
    
    content = ""
    if response.status_code == 200:
        blocks = response.json()["results"]
        for block in blocks:
            block_type = block.get("type")
            if block_type == "paragraph":
                text = block.get("paragraph", {}).get("rich_text", [])
                content += "".join([t.get("plain_text", "") for t in text]) + "\n"
            elif block_type == "heading_2":
                text = block.get("heading_2", {}).get("rich_text", [])
                content += "## " + "".join([t.get("plain_text", "") for t in text]) + "\n"
            elif block_type == "heading_3":
                text = block.get("heading_3", {}).get("rich_text", [])
                content += "### " + "".join([t.get("plain_text", "") for t in text]) + "\n"
            elif block_type == "bulleted_list_item":
                text = block.get("bulleted_list_item", {}).get("rich_text", [])
                content += "- " + "".join([t.get("plain_text", "") for t in text]) + "\n"
    
    return content[:5000]  # 限制長度

def get_embedding(text):
    """使用 Ollama 生成 embedding"""
    import urllib.request
    import urllib.error
    
    req = urllib.request.Request(
        "http://localhost:11434/api/embeddings",
        data=json.dumps({"model": "nomic-embed-text:latest", "prompt": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("embedding", [])
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def main():
    # 確保目錄存在
    os.makedirs(os.path.expanduser("~/.openclaw/vectors/notion-knowledge"), exist_ok=True)
    
    # 獲取待處理筆記
    pending = get_pending_pages()
    print(f"📋 找到 {len(pending)} 篇待處理筆記\n")
    
    # 處理每篇
    success = 0
    for i, page in enumerate(pending):
        print(f"[{i+1}/{len(pending)}] 處理: {page['title'][:40]}...")
        
        # 獲取內容
        content = get_page_content(page["id"])
        
        if not content:
            print(f"  ⚠️ 無內容")
            continue
        
        # 生成 embedding
        embedding = get_embedding(content)
        
        if embedding:
            # 儲存
            record = {
                "id": page["id"],
                "title": page["title"],
                "content_preview": content[:500],
                "embedding": embedding
            }
            
            file_path = os.path.expanduser("~/.openclaw/vectors/notion-knowledge/embeddings.jsonl")
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            
            print(f"  ✅ 完成")
            success += 1
        else:
            print(f"  ❌ Embedding 失敗")
    
    print(f"\n🎉 完成！成功處理 {success}/{len(pending)} 篇")

if __name__ == "__main__":
    main()
