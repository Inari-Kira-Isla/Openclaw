#!/usr/bin/env python3
"""
Notion Sync v1.4 - 支援向量欄位自動填充
"""

import os
import sys
import json
import requests
from datetime import datetime

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"

def read_markdown(filepath):
    """讀取 Markdown 檔案"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_metadata(content):
    """從 Markdown 提取元數據"""
    metadata = {
        "來源": "系統筆記",
        "標籤": [],
        "重點": "",
        "向量摘要": "",
        "向量狀態": "待處理",
        "語義標籤": [],
        "應用": ""
    }
    
    lines = content.split('\n')
    
    # 提取標題
    for line in lines:
        if line.startswith('# '):
            metadata["重點"] = line[2:100]
            break
    
    # 提取標籤
    for line in lines:
        if '## ' in line:
            tag = line.replace('## ', '').strip()
            if len(tag) < 20:
                metadata["標籤"].append(tag)
                metadata["語義標籤"].append(tag)
    
    # 生成向量摘要 (取前200字)
    content_without_headers = '\n'.join([l for l in lines if not l.startswith('#')])
    metadata["向量摘要"] = content_without_headers[:200]
    
    return metadata

def get_page_title(page):
    """取得頁面標題"""
    if "properties" in page:
        for key, prop in page["properties"].items():
            if prop.get("type") == "title":
                title_list = prop.get("title", [])
                if title_list:
                    return title_list[0].get("plain_text", "Untitled")
    return "Untitled"

def update_page_properties(page_id, metadata):
    """更新頁面屬性"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    properties = {}
    
    # 向量摘要 (rich_text)
    if metadata.get("向量摘要"):
        properties["向量摘要"] = {
            "rich_text": [{"text": {"content": metadata["向量摘要"]}}]
        }
    
    # 向量狀態 (select)
    if metadata.get("向量狀態"):
        properties["向量狀態"] = {
            "select": {"name": metadata["向量狀態"]}
        }
    
    # 標籤 (multi_select)
    if metadata.get("標籤"):
        properties["標籤"] = {
            "multi_select": [{"name": tag} for tag in metadata["標籤"][:5]]
        }
    
    # 語義標籤 (multi_select)
    if metadata.get("語義標籤"):
        properties["語義標籤"] = {
            "multi_select": [{"name": tag} for tag in metadata["語義標籤"][:5]]
        }
    
    # 重點 (rich_text)
    if metadata.get("重點"):
        properties["重點"] = {
            "rich_text": [{"text": {"content": metadata["重點"]}}]
        }
    
    # 應用 (select)
    if metadata.get("應用"):
        properties["應用"] = {
            "select": {"name": metadata["應用"]}
        }
    
    if not properties:
        return True
    
    data = {"properties": properties}
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"  ✅ 更新屬性成功")
            return True
        else:
            print(f"  ❌ 更新屬性失敗: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ 錯誤: {e}")
        return False

def add_content_blocks(page_id, content):
    """新增內容區塊"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # 將內容分段
    lines = content.split('\n')
    blocks = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('# '):
            blocks.append({"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]}})
        elif line.startswith('## '):
            blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]}})
        elif line.startswith('### '):
            blocks.append({"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": line[4:]}}]}})
        elif line.startswith('- '):
            blocks.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:]}}]}})
        elif line.startswith('|'):
            blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": line}}]}})
        else:
            blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": line[:2000]}}]}})
    
    # 分批發送 (每次100個區塊)
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        try:
            response = requests.post(url, headers=headers, json={"children": batch})
            if response.status_code != 200:
                print(f"  ⚠️ 區塊部分失敗: {response.status_code}")
        except Exception as e:
            print(f"  ⚠️ 區塊錯誤: {e}")
    
    return len(blocks)

def create_page(title, content, metadata):
    """建立 Notion 頁面"""
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    properties = {
        "標題": {"title": [{"text": {"content": title}}]},
        "來源": {"rich_text": [{"text": {"content": metadata.get("來源", "系統筆記")}}]},
        "日期": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "向量狀態": {"select": {"name": metadata.get("向量狀態", "待處理")}},
    }
    
    # 標籤
    if metadata.get("標籤"):
        properties["標籤"] = {"multi_select": [{"name": tag} for tag in metadata["標籤"][:5]]}
    
    # 語義標籤
    if metadata.get("語義標籤"):
        properties["語義標籤"] = {"multi_select": [{"name": tag} for tag in metadata["語義標籤"][:5]]}
    
    # 向量摘要
    if metadata.get("向量摘要"):
        properties["向量摘要"] = {"rich_text": [{"text": {"content": metadata["向量摘要"]}}]}
    
    # 重點
    if metadata.get("重點"):
        properties["重點"] = {"rich_text": [{"text": {"content": metadata["重點"]}}]}
    
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            page_id = response.json()["id"]
            print(f"✅ 頁面建立成功: {page_id}")
            
            # 新增內容區塊
            block_count = add_content_blocks(page_id, content)
            print(f"✅ 新增 {block_count} 個區塊")
            
            return page_id
        else:
            print(f"❌ 建立失敗: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return None

def sync_file(filepath):
    """同步單個檔案"""
    print(f"\n📄 處理: {filepath}")
    
    # 讀取內容
    content = read_markdown(filepath)
    
    # 提取元數據
    metadata = extract_metadata(content)
    print(f"  📊 元數據: 向量狀態={metadata['向量狀態']}, 標籤={len(metadata['標籤'])}個")
    
    # 建立頁面 (包含元數據)
    page_id = create_page(os.path.basename(filepath), content, metadata)
    
    return page_id

def main():
    if len(sys.argv) < 2:
        print("用法: python sync_to_notion_v1.4.py <markdown_file.md>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print("=" * 50)
    print("Notion Sync Script v1.4 - 向量欄位優化版")
    print("=" * 50)
    
    if os.path.isfile(filepath):
        sync_file(filepath)
    elif os.path.isdir(filepath):
        for f in os.listdir(filepath):
            if f.endswith('.md'):
                sync_file(os.path.join(filepath, f))
    else:
        print(f"❌ 檔案不存在: {filepath}")

if __name__ == "__main__":
    main()
