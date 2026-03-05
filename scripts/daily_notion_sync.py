#!/usr/bin/env python3
"""
[DEPRECATED 2026-03-04] 已被 SQLite 本地方案取代，不再使用 Notion API。
每日 Notion 同步腳本 - 完整記憶同步
"""

import requests
import os

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
from datetime import datetime

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
NOTION_VERSION = "2022-06-28"

def read_memory_file():
    """讀取今日記憶檔案"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_path = os.path.expanduser(f"~/.openclaw/workspace/memory/{today}.md")
    
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def create_notion_page(title, content):
    """建立 Notion 頁面"""
    
    # 將內容分段（Notion 每個 block 有長度限制）
    chunks = []
    current_chunk = ""
    for line in content.split('\n'):
        if len(current_chunk) + len(line) + 1 > 1900:  # Notion block limit
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += '\n' + line
            else:
                current_chunk = line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
    }
    
    # 建立第一個 block（標題）
    children = []
    for i, chunk in enumerate(chunks[:100]):  # Notion 限制 100 個 children
        children.append({'paragraph': {'rich_text': [{'text': {'content': chunk[:1900]}}]}})
    
    page_data = {
        'parent': {'database_id': DATABASE_ID},
        'properties': {
            '標題': {'title': [{'text': {'content': title}}]},
            '向量狀態': {'select': {'name': '已向量化'}},
            '應用': {'rich_text': [{'text': {'content': 'OpenClaw 系統'}}]},
            '重點': {'rich_text': [{'text': {'content': f'同步 {len(chunks)} 個區塊'}}]},
            '向量摘要': {'rich_text': [{'text': {'content': '完整記憶同步'}}]}
        },
        'children': children
    }
    
    response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=page_data)
    
    return response

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📓 同步 {today} 記憶到 Notion...")
    
    content = read_memory_file()
    if not content:
        print(f"❌ 找不到記憶檔案")
        return False
    
    # 取前 100 行作為標題參考
    preview = '\n'.join(content.split('\n')[:5])
    print(f"📝 內容預覽:\n{preview}")
    
    response = create_notion_page(f"記憶同步 - {today}", content)
    
    if response.status_code == 200:
        page_id = response.json().get("id", "N/A")
        print('✅ 同步成功!')
        print(f'   Page ID: {page_id}')
        print(f'   URL: https://notion.so/{page_id.replace("-", "")}')
        return True
    else:
        print(f'❌ 同步失敗: {response.status_code}')
        print(f'   {response.text[:300]}')
        return False

if __name__ == '__main__':
    main()
