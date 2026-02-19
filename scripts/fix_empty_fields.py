#!/usr/bin/env python3
"""
修補所有 Notion 頁面的空欄位
"""

import requests

NOTION_API_KEY = "***REMOVED***"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def get_all_pages():
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

def get_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
    response = requests.get(url, headers=headers)
    blocks = response.json().get("results", [])
    
    content_lines = []
    for block in blocks:
        for block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item"]:
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
    
    # 重點
    key_point = ""
    for line in lines:
        if line.startswith('# ') and len(line) > 2:
            key_point = line[2:100].strip()
            break
    
    # 語義標籤
    semantic_tags = []
    for line in lines:
        if line.startswith('## ') and len(line) > 3:
            tag = line[3:30].strip()
            if tag and len(semantic_tags) < 5 and tag not in semantic_tags:
                semantic_tags.append(tag)
    
    # 應用
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
    
    # 向量摘要
    vector_summary = content[:300] if content else ""
    
    return {
        "key_point": key_point,
        "semantic_tags": semantic_tags,
        "application": application,
        "vector_summary": vector_summary
    }

def update_page(page_id, metadata):
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
    
    if not properties:
        return True
    
    try:
        response = requests.patch(url, headers=headers, json={"properties": properties})
        return response.status_code == 200
    except:
        return False

def main():
    print("=" * 60)
    print("修補 Notion 頁面空欄位")
    print("=" * 60)
    
    pages = get_all_pages()
    print(f"\n總頁數: {len(pages)}")
    
    updated = 0
    for page in pages:
        page_id = page["id"]
        props = page.get("properties", {})
        title = props.get("標題", {}).get("title", [{}])[0].get("plain_text", "N/A")[:35]
        
        # 檢查是否需要更新
        needs_update = False
        vector_summary = props.get("向量摘要", {}).get("rich_text", [])
        semantic_tags = props.get("語義標籤", {}).get("multi_select", [])
        
        if not vector_summary or not semantic_tags:
            needs_update = True
        
        if needs_update:
            print(f"\n🔄 更新: {title}")
            
            # 取得內容
            content = get_page_content(page_id)
            metadata = extract_metadata(content)
            
            if update_page(page_id, metadata):
                print(f"   ✅ 完成")
                print(f"      重點: {metadata['key_point'][:25] if metadata['key_point'] else '-'}")
                print(f"      標籤: {metadata['semantic_tags'][:3] if metadata['semantic_tags'] else '-'}")
                print(f"      應用: {metadata['application']}")
                updated += 1
            else:
                print(f"   ❌ 失敗")
    
    print(f"\n✅ 總共更新 {updated} 個頁面")

if __name__ == "__main__":
    main()
