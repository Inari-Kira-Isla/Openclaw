#!/usr/bin/env python3
"""同步知識庫文檔到 Notion"""

import requests
import os

NOTION_API_KEY = "***REMOVED***"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
NOTION_VERSION = "2022-06-28"

def sync_knowledge_file(file_path, title):
    """同步單個知識文件到 Notion"""
    
    if not os.path.exists(file_path):
        print(f"❌ 找不到檔案: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into chunks
    chunks = []
    current_chunk = ''
    for line in content.split('\n'):
        if len(current_chunk) + len(line) + 1 > 1900:
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
    
    children = []
    for chunk in chunks[:100]:
        children.append({'paragraph': {'rich_text': [{'text': {'content': chunk[:1900]}}]}})
    
    page_data = {
        'parent': {'database_id': DATABASE_ID},
        'properties': {
            '標題': {'title': [{'text': {'content': title}}]},
            '向量狀態': {'select': {'name': '已向量化'}},
            '應用': {'rich_text': [{'text': {'content': 'OpenClaw 系統'}}]},
            '重點': {'rich_text': [{'text': {'content': f'同步 {len(chunks)} 個區塊'}}]},
            '向量摘要': {'rich_text': [{'text': {'content': '知識庫文件'}}]}}
        },
        'children': children
    }
    
    response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=page_data)
    
    if response.status_code == 200:
        print(f'✅ {title} 同步成功!')
        return True
    else:
        print(f'❌ {title} 同步失敗: {response.text[:200]}')
        return False

if __name__ == '__main__':
    # 同步 AI 趨勢報告
    sync_knowledge_file(
        os.path.expanduser('~/.openclaw/workspace/knowledge/AI_趨勢報告_2026-02-25.md'),
        'AI 趨勢報告 - 2026年2月25日'
    )
