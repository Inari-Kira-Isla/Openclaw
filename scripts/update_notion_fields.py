#!/usr/bin/env python3
"""
更新現有 Notion 頁面的向量欄位
"""

import requests
import os

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def get_all_pages():
    """取得所有頁面"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
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

def get_page_title(page):
    """取得頁面標題"""
    if "properties" in page:
        for key, prop in page["properties"].items():
            if prop.get("type") == "title":
                title_list = prop.get("title", [])
                if title_list:
                    return title_list[0].get("plain_text", "Untitled")
    return "Untitled"

def get_page_content(page_id):
    """取得頁面內容"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    blocks = response.json().get("results", [])
    
    content = []
    for block in blocks:
        if "paragraph" in block:
            text = block["paragraph"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content.append(t["plain_text"])
        elif "heading_1" in block:
            text = block["heading_1"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content.append("# " + t["plain_text"])
        elif "heading_2" in block:
            text = block["heading_2"].get("rich_text", [])
            for t in text:
                if "plain_text" in t:
                    content.append("## " + t["plain_text"])
    
    return "\n".join(content)

def extract_tags(content):
    """提取標籤"""
    tags = []
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('## '):
            tag = line.replace('## ', '').strip()
            if len(tag) < 20 and len(tags) < 5:
                tags.append(tag)
    
    return tags

def update_page(page_id, content):
    """更新頁面向量欄位"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # 提取標籤
    tags = extract_tags(content)
    
    # 提取重點 (第一個標題)
    key_point = ""
    for line in content.split('\n'):
        if line.startswith('# '):
            key_point = line[2:100]
            break
    
    # 向量摘要
    summary = content[:200] if content else ""
    
    properties = {
        "向量狀態": {"select": {"name": "已向量化"}},
    }
    
    if tags:
        properties["語義標籤"] = {"multi_select": [{"name": tag} for tag in tags]}
        properties["標籤"] = {"multi_select": [{"name": tag} for tag in tags[:5]]}
    
    if key_point:
        properties["重點"] = {"rich_text": [{"text": {"content": key_point}}]}
    
    if summary:
        properties["向量摘要"] = {"rich_text": [{"text": {"content": summary}}]}
    
    if not properties:
        return True
    
    data = {"properties": properties}
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return True
        else:
            print(f"  ❌ 更新失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 錯誤: {e}")
        return False

def main():
    print("=" * 50)
    print("更新現有 Notion 頁面向量欄位")
    print("=" * 50)
    
    pages = get_all_pages()
    print(f"\n📄 找到 {len(pages)} 個頁面")
    
    updated = 0
    for page in pages:
        page_id = page["id"]
        title = get_page_title(page)
        
        # 檢查是否需要更新
        props = page.get("properties", {})
        vector_status_prop = props.get("向量狀態")
        
        if vector_status_prop and vector_status_prop.get("select"):
            vector_status = vector_status_prop.get("select", {}).get("name", "")
        else:
            vector_status = ""
        
        if vector_status != "已向量化":
            print(f"\n🔄 更新: {title}")
            content = get_page_content(page_id)
            if update_page(page_id, content):
                print(f"  ✅ 完成")
                updated += 1
        else:
            print(f"  ⏭️ 跳過: {title} (已是已向量化)")
    
    print(f"\n✅ 總共更新 {updated} 個頁面")

if __name__ == "__main__":
    main()
