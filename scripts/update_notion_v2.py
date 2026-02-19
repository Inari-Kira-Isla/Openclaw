#!/usr/bin/env python3
"""
更新現有 Notion 頁面的向量欄位 - 修正版
"""

import requests
import os

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def get_all_pages(limit=60):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more and len(all_pages) < limit:
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
            break
    return all_pages

def get_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    response = requests.get(url, headers=headers)
    blocks = response.json().get("results", [])
    content_lines = []
    for block in blocks:
        for block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
            if block_type in block:
                text = block[block_type].get("rich_text", [])
                for t in text:
                    if "plain_text" in t:
                        prefix = "# " if block_type == "heading_1" else "## " if block_type == "heading_2" else "### " if block_type == "heading_3" else ""
                        content_lines.append(prefix + t["plain_text"])
                break
    return "\n".join(content_lines)

def extract_metadata(content):
    lines = content.split('\n')
    key_point = ""
    for line in lines:
        if line.startswith('# '):
            key_point = line[2:100].strip()
            break
    
    semantic_tags = []
    for line in lines:
        if line.startswith('## '):
            tag = line[3:30].strip()
            if tag and len(semantic_tags) < 5:
                semantic_tags.append(tag)
    
    content_lower = content.lower()
    application = "一般"
    if '自動化' in content or 'workflow' in content_lower:
        application = '自動化'
    elif '分析' in content or '數據' in content_lower:
        application = '數據分析'
    elif '學習' in content or '筆記' in content_lower:
        application = '學習筆記'
    elif '系統' in content or '架構' in content_lower:
        application = '系統架構'
    elif '錯誤' in content or '修復' in content_lower:
        application = '錯誤修復'
    
    source = "系統筆記"
    if 'telegram' in content_lower:
        source = "Telegram 對話"
    elif 'slack' in content_lower:
        source = "Slack 對話"
    
    return {
        "key_point": key_point,
        "semantic_tags": semantic_tags,
        "application": application,
        "source": source,
        "vector_summary": content[:200] if content else ""
    }

def update_page(page_id, metadata):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
    
    properties = {}
    if metadata.get("key_point"):
        properties["重點"] = {"rich_text": [{"text": {"content": metadata["key_point"]}}]}
    if metadata.get("semantic_tags"):
        properties["語義標籤"] = {"multi_select": [{"name": tag} for tag in metadata["semantic_tags"]]}
        properties["標籤"] = {"multi_select": [{"name": tag} for tag in metadata["semantic_tags"][:5]]}
    if metadata.get("application"):
        properties["應用"] = {"rich_text": [{"text": {"content": metadata["application"]}}]}
    if metadata.get("vector_summary"):
        properties["向量摘要"] = {"rich_text": [{"text": {"content": metadata["vector_summary"]}}]}
    properties["向量狀態"] = {"select": {"name": "已向量化"}}
    
    if not properties:
        return True
    try:
        response = requests.patch(url, headers=headers, json={"properties": properties})
        return response.status_code == 200
    except:
        return False

def main():
    print("=" * 50)
    print("更新 Notion 頁面元數據 (修正版)")
    print("=" * 50)
    
    pages = get_all_pages()
    print(f"\\n找到 {len(pages)} 個頁面")
    
    updated = 0
    for page in pages:
        page_id = page["id"]
        props = page.get("properties", {})
        title = props.get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")[:35]
        
        content = get_page_content(page_id)
        metadata = extract_metadata(content)
        
        print(f"\\n🔄 {title}")
        if update_page(page_id, metadata):
            print(f"  ✅ {metadata['key_point'][:20] if metadata['key_point'] else '-'} | {metadata['semantic_tags'][:2] if metadata['semantic_tags'] else '-'} | {metadata['application']}")
            updated += 1
    
    print(f"\\n✅ 完成 {updated} 個頁面")

if __name__ == "__main__":
    main()
