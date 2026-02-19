#!/usr/bin/env python3
"""
更新現有 Notion 頁面的向量欄位 - 完整版
"""

import requests
import os

NOTION_API_KEY = "***REMOVED***"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def get_all_pages(limit=50):
    """取得所有頁面"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
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
    """取得頁面內容"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    blocks = response.json().get("results", [])
    
    content_lines = []
    for block in blocks:
        if "paragraph" in block:
            text = block["paragraph"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content_lines.append(t["plain_text"])
        elif "heading_1" in block:
            text = block["heading_1"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content_lines.append("# " + t["plain_text"])
        elif "heading_2" in block:
            text = block["heading_2"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content_lines.append("## " + t["plain_text"])
        elif "heading_3" in block:
            text = block["heading_3"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content_lines.append("### " + t["plain_text"])
    
    return "\n".join(content_lines)

def extract_metadata(content):
    """從內容提取元數據"""
    lines = content.split('\n')
    
    # 提取重點 (第一個標題)
    key_point = ""
    for line in lines:
        if line.startswith('# '):
            key_point = line[2:100].strip()
            break
    
    # 提取語義標籤 (## 標題)
    semantic_tags = []
    for line in lines:
        if line.startswith('## '):
            tag = line[3:30].strip()
            if tag and len(semantic_tags) < 5:
                semantic_tags.append(tag)
    
    # 提取應用場景 (根據關鍵詞)
    application = ""
    content_lower = content.lower()
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
    else:
        application = '一般'
    
    # 提取來源
    source = "系統筆記"
    if 'telegram' in content_lower:
        source = "Telegram 對話"
    elif 'slack' in content_lower:
        source = "Slack 對話"
    elif '學習' in content_lower:
        source = "學習筆記"
    
    return {
        "key_point": key_point,
        "semantic_tags": semantic_tags,
        "application": application,
        "source": source,
        "vector_summary": content[:200] if content else ""
    }

def update_page(page_id, metadata):
    """更新頁面"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    properties = {}
    
    # 重點
    if metadata.get("key_point"):
        properties["重點"] = {
            "rich_text": [{"text": {"content": metadata["key_point"]}}]
        }
    
    # 語義標籤
    if metadata.get("semantic_tags"):
        properties["語義標籤"] = {
            "multi_select": [{"name": tag} for tag in metadata["semantic_tags"]]
        }
        properties["標籤"] = {
            "multi_select": [{"name": tag} for tag in metadata["semantic_tags"][:5]]
        }
    
    # 應用
    if metadata.get("application"):
        properties["應用"] = {
            "select": {"name": metadata["application"]}
        }
    
    # 向量摘要
    if metadata.get("vector_summary"):
        properties["向量摘要"] = {
            "rich_text": [{"text": {"content": metadata["vector_summary"]}}]
        }
    
    # 向量狀態
    properties["向量狀態"] = {"select": {"name": "已向量化"}}
    
    if not properties:
        return True
    
    data = {"properties": properties}
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def main():
    print("=" * 60)
    print("更新 Notion 頁面 - 完整元數據")
    print("=" * 60)
    
    pages = get_all_pages()
    print(f"\n找到 {len(pages)} 個頁面")
    
    updated = 0
    for page in pages:
        page_id = page["id"]
        props = page.get("properties", {})
        
        # 取得標題
        title = props.get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")[:40]
        
        # 取得內容
        content = get_page_content(page_id)
        
        # 提取元數據
        metadata = extract_metadata(content)
        
        # 更新
        print(f"\n🔄 更新: {title}")
        if update_page(page_id, metadata):
            print(f"  ✅ 完成")
            print(f"     重點: {metadata['key_point'][:30] if metadata['key_point'] else '空'}...")
            print(f"     語義標籤: {metadata['semantic_tags']}")
            print(f"     應用: {metadata['application']}")
            updated += 1
        else:
            print(f"  ❌ 失敗")
    
    print(f"\n✅ 總共更新 {updated} 個頁面")

if __name__ == "__main__":
    main()
