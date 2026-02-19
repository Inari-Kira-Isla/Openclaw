#!/usr/bin/env python3
"""
Notion Sync Script v1.5 - 修復重複頁面問題
- 檢查頁面是否已存在
- 更新現有頁面而非建立新頁面
"""

import os
import requests
from datetime import datetime

NOTION_API_KEY = "***REMOVED***"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def get_all_pages():
    """取得所有頁面"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    
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
            break
    
    return all_pages

def find_page_by_title(title):
    """根據標題找頁面"""
    pages = get_all_pages()
    for page in pages:
        page_title = page["properties"].get("標題", {}).get("title", [{}])[0].get("plain_text", "")
        if page_title == title:
            return page["id"]
    return None

def get_page_content(page_id):
    """取得頁面內容"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    response = requests.get(url, headers=headers)
    return response.json().get("results", [])

def extract_metadata(content):
    """從內容提取元數據"""
    lines = content.split('\n')
    
    # 提取重點 (# 標題)
    key_point = ""
    for line in lines:
        if line.startswith('# ') and len(line) > 2:
            key_point = line[2:100].strip()
            break
    
    # 提取語義標籤 (## 標題)
    semantic_tags = []
    for line in lines:
        if line.startswith('## ') and len(line) > 3:
            tag = line[3:30].strip()
            if tag and len(semantic_tags) < 5 and tag not in semantic_tags:
                semantic_tags.append(tag)
    
    # 提取應用 (根據關鍵詞)
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
    elif '行銷' in content or '銷售' in content_lower:
        application = '行銷'
    
    # 提取來源
    source = "系統筆記"
    if 'telegram' in content_lower:
        source = "Telegram 對話"
    elif 'slack' in content_lower:
        source = "Slack 對話"
    elif 'notion' in content_lower:
        source = "Notion 筆記"
    
    return {
        "key_point": key_point,
        "semantic_tags": semantic_tags,
        "application": application,
        "source": source,
        "vector_summary": content[:300] if content else ""
    }

def update_page_properties(page_id, metadata, content):
    """更新頁面屬性"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    properties = {}
    
    # 重點
    if metadata.get("key_point"):
        properties["重點"] = {"rich_text": [{"text": {"content": metadata["key_point"]}}]}
    
    # 語義標籤
    if metadata.get("semantic_tags"):
        properties["語義標籤"] = {"multi_select": [{"name": tag} for tag in metadata["semantic_tags"]]}
        properties["標籤"] = {"multi_select": [{"name": tag} for tag in metadata["semantic_tags"][:5]]}
    
    # 應用
    if metadata.get("application"):
        properties["應用"] = {"rich_text": [{"text": {"content": metadata["application"]}}]}
    
    # 向量摘要
    if metadata.get("vector_summary"):
        properties["向量摘要"] = {"rich_text": [{"text": {"content": metadata["vector_summary"]}}]}
    
    # 向量狀態
    properties["向量狀態"] = {"select": {"name": "已向量化"}}
    
    # 來源
    properties["來源"] = {"rich_text": [{"text": {"content": metadata.get("source", "系統筆記")}}]}
    
    if not properties:
        return True
    
    data = {"properties": properties}
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"更新錯誤: {e}")
        return False

def sync_file(filepath):
    """同步單個檔案"""
    print(f"\n📄 處理: {filepath}")
    
    # 讀取檔案
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 取得標題
    title = os.path.basename(filepath).replace('.md', '')
    
    # 提取元數據
    metadata = extract_metadata(content)
    
    print(f"   標題: {title}")
    print(f"   重點: {metadata['key_point'][:30] if metadata['key_point'] else '空'}...")
    print(f"   標籤: {metadata['semantic_tags']}")
    print(f"   應用: {metadata['application']}")
    
    # 檢查頁面是否存在
    page_id = find_page_by_title(title)
    
    if page_id:
        print(f"   📝 頁面已存在: {page_id}")
        # 更新現有頁面
        if update_page_properties(page_id, metadata, content):
            print(f"   ✅ 頁面更新成功")
            return page_id
        else:
            print(f"   ❌ 頁面更新失敗")
            return None
    else:
        print(f"   🆕 頁面不存在，需要手動建立")
        return None

def main():
    print("=" * 60)
    print("Notion Sync v1.5 - 修復重複頁面")
    print("=" * 60)
    
    # 測試一個檔案
    test_file = "learning/parenting-emotion-management.md"
    if os.path.exists(test_file):
        sync_file(test_file)

if __name__ == "__main__":
    main()
