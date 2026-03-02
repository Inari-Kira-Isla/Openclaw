#!/usr/bin/env python3
"""
智能每日 Notion 同步腳本 - 只同步當日新增內容
"""

import requests
import os
from datetime import datetime

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
NOTION_VERSION = "2022-06-28"

def get_existing_titles():
    """取得資料庫中已有的標題"""
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
    }
    
    existing = set()
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
            
        resp = requests.post(
            f'https://api.notion.com/v1/databases/{DATABASE_ID}/query',
            headers=headers,
            json=payload
        )
        
        if resp.status_code != 200:
            print(f"⚠️ 無法取得現有頁面: {resp.status_code}")
            return set()
        
        data = resp.json()
        for page in data.get('results', []):
            title = page.get('properties', {}).get('標題', {}).get('title', [])
            if title:
                existing.add(title[0]['text']['content'])
        
        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')
    
    return existing

def read_memory_file():
    """讀取今日記憶檔案"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_path = os.path.expanduser(f"~/.openclaw/workspace/memory/{today}.md")
    
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def extract_new_articles(content):
    """提取當日新增的文章區塊"""
    if not content:
        return []
    
    articles = []
    
    # 定義文章標題模式
    article_markers = [
        "## 📚 AI 進入企業核心",
        "## 📓 localissue sync",
        "## 📊 分析學習"
    ]
    
    for marker in article_markers:
        if marker in content:
            # 找到標題位置
            idx = content.find(marker)
            # 找下一個 ## 標題
            next_idx = content.find("\n## ", idx + len(marker))
            if next_idx == -1:
                article = content[idx:]
            else:
                article = content[idx:next_idx]
            
            title = marker.replace("## ", "").replace("📚 ", "").replace("📓 ", "").replace("📊 ", "")
            articles.append((title, article.strip()))
    
    return articles

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
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"🧠 智能同步 - {today}")
    print("=" * 40)
    
    # 取得現有標題
    print("📋 檢查現有頁面...")
    existing = get_existing_titles()
    print(f"   現有 {len(existing)} 個頁面")
    
    # 讀取記憶
    content = read_memory_file()
    if not content:
        print("❌ 找不到記憶檔案")
        return
    
    # 提取文章
    articles = extract_new_articles(content)
    print(f"   發現 {len(articles)} 篇文章")
    
    # 只同步不存在的
    synced = 0
    for title, article in articles:
        if title in existing:
            print(f"   ⏭️  跳過: {title[:30]}... (已存在)")
        else:
            print(f"   📤 新增: {title[:30]}...")
            resp = create_notion_page(title, article, tags=['知識庫'])
            if resp.status_code == 200:
                page_id = resp.json().get('id', 'N/A')
                print(f"       ✅ https://notion.so/{page_id.replace('-','')}")
                synced += 1
            else:
                print(f"       ❌ 失敗: {resp.status_code}")
    
    print("=" * 40)
    if synced > 0:
        print(f"✅ 完成! 新增 {synced} 篇文章")
    else:
        print("✅ 沒有新內容需要同步")

if __name__ == '__main__':
    main()
