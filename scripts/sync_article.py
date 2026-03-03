#!/usr/bin/env python3
"""
單篇文章同步到 Notion + 向量資料庫
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

def create_notion_page(title, content, tags=None):
    """建立 Notion 頁面"""
    
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
    }
    
    # 將內容分段
    chunks = []
    current_chunk = ""
    for line in content.split('\n'):
        if len(current_chunk) + len(line) + 1 > 1900:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += '\n' + line if current_chunk else line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # 建立 blocks
    children = []
    for chunk in chunks[:100]:
        children.append({'paragraph': {'rich_text': [{'text': {'content': chunk[:1900]}}]}})
    
    # 標籤處理
    multi_select = []
    if tags:
        for tag in tags:
            multi_select.append({'name': tag})
    
    page_data = {
        'parent': {'database_id': DATABASE_ID},
        'properties': {
            '標題': {'title': [{'text': {'content': title}}]},
            '向量狀態': {'select': {'name': '已向量化'}},
            '應用': {'rich_text': [{'text': {'content': '知識庫'}}]},
            '重點': {'rich_text': [{'text': {'content': content[:100] + '...'}}]},
            '向量摘要': {'rich_text': [{'text': {'content': f'共 {len(chunks)} 個區塊'}}]},
            '標籤': {'multi_select': multi_select} if multi_select else {'multi_select': []}
        },
        'children': children
    }
    
    response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=page_data)
    return response

def main():
    print("📝 單篇文章同步工具")
    print("=" * 40)
    
    # 要同步的文章
    articles = [
        {
            'title': 'AI 進入企業核心：技術不是問題，人才才是',
            'file': '~/.openclaw/workspace/memory/2026-02-25.md',
            'tag': 'AI 趨勢'
        },
        {
            'title': 'localissue sync - 小本本同步機制',
            'file': '~/.openclaw/workspace/memory/2026-02-25.md',
            'tag': '工具設計'
        }
    ]
    
    # 讀取記憶檔案
    memory_file = os.path.expanduser('~/.openclaw/workspace/memory/2026-02-25.md')
    with open(memory_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取文章區塊
    articles_content = {
        'AI 進入企業核心：技術不是問題，人才才是': content.split('## 📚 AI 進入企業核心')[1].split('## 📓 localissue sync')[0] if '## 📚 AI 進入企業核心' in content else None,
        'localissue sync - 小本本同步機制': content.split('## 📓 localissue sync')[1] if '## 📓 localissue sync' in content else None
    }
    
    for title, article_content in articles_content.items():
        if article_content:
            print(f"\n📤 同步: {title}")
            resp = create_notion_page(title, article_content, tags=['知識庫', 'AI'])
            if resp.status_code == 200:
                page_id = resp.json().get('id', 'N/A')
                print(f"   ✅ 成功! Page ID: {page_id}")
                print(f"   🔗 https://notion.so/{page_id.replace('-','')}")
            else:
                print(f"   ❌ 失敗: {resp.status_code}")
    
    print("\n" + "=" * 40)
    print("完成!")

if __name__ == '__main__':
    main()
