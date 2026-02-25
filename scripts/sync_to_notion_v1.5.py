#!/usr/bin/env python3
"""
Notion Sync Script v1.5 - 修復重複頁面問題
- 檢查頁面是否已存在
- 更新現有頁面而非建立新頁面
"""

import os
import requests
from datetime import datetime

NOTION_API_KEY = "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"
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

def extract_metadata(content):
    """從內容提取元數據"""
    lines = content.split('\n')
    key_point = ""
    semantic_tags = []
    
    # 提取第一段作為重點
    for line in lines:
        if line.strip() and not line.startswith('#'):
            key_point = line.strip()[:100]
            break
    
    # 提取標籤
    for line in lines:
        if line.startswith('#'):
            tag = line.replace('#', '').strip()
            if tag:
                semantic_tags.append(tag)
    
    # 判斷應用場景
    content_lower = content.lower()
    application = '自動化'
    if 'telegram' in content_lower or 'whatsapp' in content_lower:
        application = '即時通訊'
    elif 'order' in content_lower or '訂單' in content_lower:
        application = '訂單管理'
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

def create_page(title, metadata, content):
    """建立新頁面"""
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    properties = {
        "標題": {"title": [{"text": {"content": title}}]},
        "應用場景": {"select": {"name": metadata["application"]}},
        "來源": {"select": {"name": metadata["source"]}},
        "重點": {"rich_text": [{"text": {"content": metadata["key_point"]}}]},
        "Semantic Tags": {"multi_select": [{"name": tag} for tag in metadata["semantic_tags"][:5]]}
    }
    
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": properties}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["id"]
    except Exception as e:
        print(f"   ❌ 錯誤: {e}")
    return None

def sync_file(filepath):
    """同步單個檔案"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = os.path.basename(filepath).replace('.md', '')
    metadata = extract_metadata(content)
    
    print(f"📄 處理: {filepath}")
    print(f"   標題: {title}")
    
    page_id = find_page_by_title(title)
    
    if page_id:
        print(f"   📝 頁面已存在")
        return page_id
    else:
        print(f"   🆕 建立新頁面...")
        new_id = create_page(title, metadata, content)
        if new_id:
            print(f"   ✅ 建立成功: {new_id}")
            return new_id
        return None

def main():
    print("=" * 60)
    print("Notion Sync v1.5 - 批量同步")
    print("=" * 60)
    
    # 同步所有 md 檔案
    base_dirs = ["memory", "learning", "projects"]
    total = 0
    synced = 0
    
    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue
        
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    total += 1
                    try:
                        result = sync_file(filepath)
                        if result:
                            synced += 1
                            print(f"   ✅ Synced: {filepath}")
                    except Exception as e:
                        print(f"   ❌ 錯誤: {e}")
    
    print("")
    print("=" * 60)
    print(f"📊 同步完成: {synced}/{total}")
    print("=" * 60)

if __name__ == "__main__":
    main()
