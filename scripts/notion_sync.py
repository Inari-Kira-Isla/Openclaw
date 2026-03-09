#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEPRECATED 2026-03-04] 已被 SQLite 本地方案取代，不再使用 Notion API。
Notion 自動同步系統 - Notion Auto Sync System
"""

import os

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
import json
import requests
from datetime import datetime

class NotionSync:
    def __init__(self):
        self.key = os.environ.get("NOTION_API_KEY", "")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        self.databases = {
            "success": "315a1238-f49d-8149-b67d-f138cc7c7f7c",
            "error": "315a1238-f49d-81ef-be80-c632e0b5e493",
            "learning": "30aa1238-f49d-817c-8163-dd76d1309240",
            "daily": "30aa1238-f49d-8136-a813-fb759eb30e47",
            "members": "302a1238-f49d-80cc-ba55-f83d5704bdb8"
        }
        
        self.local_path = os.path.expanduser("~/.openclaw/workspace/memory/notion_sync/")
        os.makedirs(self.local_path, exist_ok=True)
    
    def query_database(self, db_id):
        """查詢資料庫"""
        url = f"{self.base_url}/databases/{db_id}/query"
        
        response = requests.post(url, headers=self.headers, json={})
        
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"   ❌ Error: {response.status_code}")
            return []
    
    def get_page_content(self, page_id):
        """獲取頁面內容"""
        url = f"{self.base_url}/blocks/{page_id}/children"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    
    def extract_text(self, block):
        """提取文本"""
        if "paragraph" in block:
            texts = block["paragraph"].get("rich_text", [])
            return "".join([t.get("plain_text", "") for t in texts])
        return ""
    
    def sync_database(self, db_name, db_id):
        """同步資料庫"""
        print(f"\n🔄 同步: {db_name}")
        
        # 查詢所有頁面
        pages = self.query_database(db_id)
        
        print(f"   找到 {len(pages)} 個頁面")
        
        items = []
        
        for page in pages:
            page_id = page.get("id")
            props = page.get("properties", {})
            
            # 提取標題
            title = "Untitled"
            for key, val in props.items():
                if val.get("type") == "title":
                    title_arr = val.get("title", [])
                    title = "".join([t.get("plain_text", "") for t in title_arr]) if title_arr else "Untitled"
            
            # 提取其他欄位
            item = {
                "id": page_id,
                "title": title,
                "created_time": page.get("created_time"),
                "last_edited_time": page.get("last_edited_time")
            }
            
            # 添加其他欄位
            for key, val in props.items():
                try:
                    if val.get("type") == "rich_text":
                        item[key] = "".join([t.get("plain_text", "") for t in val.get("rich_text", [])])
                    elif val.get("type") == "number":
                        item[key] = val.get("number")
                    elif val.get("type") == "select":
                        select_val = val.get("select")
                        item[key] = select_val.get("name") if select_val else None
                    elif val.get("type") == "checkbox":
                        item[key] = val.get("checkbox")
                    elif val.get("type") == "date":
                        date_val = val.get("date")
                        item[key] = date_val.get("start") if date_val else None
                except:
                    pass
            
            items.append(item)
        
        # 保存到本地
        output_file = os.path.join(self.local_path, f"{db_name}.json")
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ 已保存: {output_file}")
        
        return items
    
    def sync_all(self):
        """同步所有資料庫"""
        print("\n" + "="*50)
        print("🔄 Notion 自動同步系統")
        print("="*50)
        
        results = {}
        
        for name, db_id in self.databases.items():
            items = self.sync_database(name, db_id)
            results[name] = len(items)
        
        # 生成摘要
        print("\n" + "="*50)
        print("📊 同步完成!")
        print("="*50)
        
        for name, count in results.items():
            print(f"   {name}: {count} 個項目")
        
        return results
    
    def get_updates(self, db_name, db_id):
        """獲取更新"""
        items = self.sync_database(db_name, db_id)
        
        # 找出今天更新的
        today = datetime.now().strftime("%Y-%m-%d")
        
        updates = [i for i in items if today in i.get("last_edited_time", "")]
        
        return updates

if __name__ == "__main__":
    sync = NotionSync()
    sync.sync_all()
