#!/usr/bin/env python3
"""
Notion Sync Script - AI Agent 系統架構學習筆記
"""

import os
import json
import requests
from datetime import datetime

# 配置
NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238-f49d-817c-8163-dd76d1309240"
NOTION_VERSION = "2022-06-28"

def get_headers():
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

def create_note(data):
    """創建 Notion 筆記"""
    url = "https://api.notion.com/v1/pages"
    
    properties = {
        "標題": {"title": [{"text": {"content": data.get("title", "")}}]},
        "標籤": {"multi_select": [{"name": tag} for tag in data.get("tags", [])]},
        "來源": {"rich_text": [{"text": {"content": data.get("source", "")}}]},
        "重點": {"rich_text": [{"text": {"content": data.get("highlight", "")}}]},
        "應用": {"rich_text": [{"text": {"content": data.get("application", "")}}]},
        "日期": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
    }
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    
    response = requests.post(url, headers=get_headers(), json=payload)
    return response.status_code == 200

# Test
test_data = {
    "title": "OpenClaw 系統架構筆記",
    "tags": ["Agent", "架構"],
    "source": "OpenClaw 官方文檔",
    "highlight": "OpenClaw 是一個 AI Agent 運行框架",
    "application": "可用於建構自己的 AI Agent 系統"
}

if create_note(test_data):
    print("✅ 測試筆記創建成功！")
else:
    print("❌ 測試失敗")
