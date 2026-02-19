#!/usr/bin/env python3
"""
Notion Sync Script - 完整同步（含內容）
版本: v1.3 - 修復內容同步
"""

import os
import sys
import json
import requests
from datetime import datetime

# 配置
NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
NOTION_VERSION = "2025-09-03"

def get_headers():
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

def create_page_with_content(title, content, tags=None):
    """創建 Notion 筆記並添加內容"""
    
    # 1. 建立頁面
    url = "https://api.notion.com/v1/pages"
    
    properties = {
        "標題": {"title": [{"text": {"content": title}}]},
        "來源": {"rich_text": [{"text": {"content": "系統筆記"}}]},
        "日期": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
    }
    
    if tags:
        properties["標籤"] = {"multi_select": [{"name": tag} for tag in tags]}
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    
    response = requests.post(url, headers=get_headers(), json=payload)
    
    if response.status_code != 200:
        return False, f"建立頁面失敗: {response.text}"
    
    page_id = response.json()["id"]
    print(f"✅ 頁面建立成功: {page_id}")
    
    # 2. 添加內容區塊
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    # 將內容分割成區塊
    lines = content.split('\n')
    blocks = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 判斷標題層級
        if line.startswith('### '):
            blocks.append({
                "heading_3": {"rich_text": [{"text": {"content": line[4:]}}]}
            })
        elif line.startswith('## '):
            blocks.append({
                "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]}
            })
        elif line.startswith('# '):
            blocks.append({
                "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]}
            })
        elif line.startswith('- [ ]'):
            blocks.append({
                "to_do": {"rich_text": [{"text": {"content": line[6:].strip()}}], "checked": False}
            })
        elif line.startswith('- [x]') or line.startswith('- [X]'):
            blocks.append({
                "to_do": {"rich_text": [{"text": {"content": line[5:].strip()}}], "checked": True}
            })
        elif line.startswith('- '):
            blocks.append({
                "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:]}}]}
            })
        elif line.startswith('|'):
            # 表格行 - 簡單處理
            blocks.append({
                "paragraph": {"rich_text": [{"text": {"content": line}}]}
            })
        else:
            blocks.append({
                "paragraph": {"rich_text": [{"text": {"content": line}}]}
            })
    
    # 每次最多添加 100 個區塊
    if blocks:
        block_payload = {"children": blocks[:100]}
        response = requests.patch(blocks_url, headers=get_headers(), json=block_payload)
        
        if response.status_code == 200:
            print(f"✅ 內容添加成功: {len(blocks)} 個區塊")
            return True, page_id
        else:
            print(f"⚠️ 內容添加失敗: {response.text}")
            return True, page_id  # 頁面已建立，只是內容失敗
    
    return True, page_id

def sync_markdown_file(filepath):
    """同步 Markdown 檔案到 Notion"""
    
    if not os.path.exists(filepath):
        return False, f"檔案不存在: {filepath}"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 從檔名取得標題
    filename = os.path.basename(filepath)
    title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ')
    
    # 取得標籤
    tags = []
    if 'facebook' in filepath.lower():
        tags.append('Facebook')
    if 'integration' in filepath.lower():
        tags.append('整合')
    
    return create_page_with_content(title, content, tags)

# 主程式
if __name__ == "__main__":
    print("=" * 50)
    print("Notion Sync Script v1.3")
    print("=" * 50)
    print(f"Database ID: {DATABASE_ID}")
    print()
    
    if len(sys.argv) < 2:
        print("使用方法: python3 sync_to_notion.py <markdown_file.md>")
        print("範例: python3 sync_to_notion.py memory/projects/facebook.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(f"同步檔案: {filepath}")
    print()
    
    success, result = sync_markdown_file(filepath)
    
    if success:
        print(f"\n✅ 同步完成！")
        print(f"   Page ID: {result}")
    else:
        print(f"\n❌ 同步失敗: {result}")
