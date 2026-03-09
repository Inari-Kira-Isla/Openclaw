#!/usr/bin/env python3
"""
每小時熱門話題研究腳本
使用 You.com + Serper API 搜索熱門話題
"""

import os
import json
import requests
from datetime import datetime

# API Keys
YOU_API_KEY = "***REMOVED***"
SERPER_API_KEY = "***REMOVED***"

def search_youtube_trending():
    """搜索 YouTube 熱門"""
    topics = []
    try:
        r = requests.post(
            "https://google.serper.dev/videos",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": "trending 2026", "num": 5},
            timeout=15
        )
        if r.status_code == 200:
            for item in r.json().get("videos", [])[:3]:
                topics.append({
                    "source": "YouTube",
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "category": "影片"
                })
    except Exception as e:
        print(f"YouTube search error: {e}")
    return topics

def search_general():
    """搜索一般熱門話題"""
    topics = []
    queries = [
        ("AI trends 2026", "AI"),
        ("technology news 2026", "科技"),
        ("finance investing", "金融"),
        ("mathematics discoveries", "數學"),
        ("philosophy discussions", "哲學")
    ]
    
    for query, category in queries:
        try:
            # Try Serper first
            r = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                json={"q": query, "num": 3},
                timeout=15
            )
            if r.status_code == 200:
                for item in r.json().get("organic", [])[:2]:
                    topics.append({
                        "source": "Google",
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "category": category,
                        "query": query
                    })
                continue
        except:
            pass
        
        # Fallback to You.com
        try:
            r = requests.get(
                "https://api.you.com/search",
                params={"query": query, "apikey": YOU_API_KEY, "num": 3},
                timeout=15
            )
            if r.status_code == 200:
                for item in r.json().get("results", [])[:2]:
                    topics.append({
                        "source": "You.com",
                        "title": item.get("title", ""),
                        "link": item.get("url", ""),
                        "category": category,
                        "query": query
                    })
        except Exception as e:
            print(f"You.com error for {query}: {e}")
    
    return topics

def record_to_memory(topics):
    memory_path = os.path.expanduser("~/.openclaw/workspace/memory/hourly-trending.md")
    
    content = f"""# 每小時熱門話題 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    for t in topics:
        content += f"""### {t['category']} [{t['source']}]
- {t['title']}
- {t['link']}

"""
    
    with open(memory_path, "a", encoding="utf-8") as f:
        f.write(content)
    
    return len(topics)

if __name__ == "__main__":
    print(f"🔍 搜索熱門話題... {datetime.now()}")
    
    # YouTube
    yt_topics = search_youtube_trending()
    
    # General
    gen_topics = search_general()
    
    topics = yt_topics + gen_topics
    count = record_to_memory(topics)
    
    print(f"✅ 記錄了 {count} 個話題")
    for t in topics[:5]:
        print(f"  [{t['category']}] {t['title'][:50]}")
