#!/usr/bin/env python3
"""
[DEPRECATED 2026-03-04] 已被 SQLite 本地方案取代，不再使用 Notion API。
Notion 向量資料庫檢查腳本
檢查 Notion AI Agent 系統架構學習筆記 資料庫狀態
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
import requests
import json

NOTION_KEY = os.environ.get("NOTION_API_KEY", "")
DB_ID = "30aa1238f49d817c8163dd76d1309240"

print("========================================")
print("  Notion 向量資料庫檢查")
print("========================================")

# 查詢資料庫
headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

r = requests.post(f"https://api.notion.com/v1/databases/{DB_ID}/query", 
                  headers=headers, json={"page_size": 100}, timeout=10)

if r.status_code != 200:
    print(f"❌ API 錯誤: {r.status_code}")
    exit(1)

d = r.json()
results = d.get('results', [])

total = len(results)
pending = 0
vectorized = 0
pending_titles = []

for item in results:
    props = item.get('properties', {})
    if not props:
        continue
    
    # 取得標題
    title = "No title"
    title_obj = props.get('標題', {})
    if title_obj:
        title_list = title_obj.get('title', [])
        if title_list:
            title = title_list[0].get('text', {}).get('content', 'No title')
    
    # 取得狀態
    status = ""
    status_obj = props.get('向量狀態', {})
    if status_obj and isinstance(status_obj, dict):
        select = status_obj.get('select')
        if select and isinstance(select, dict):
            status = select.get('name', '')
    
    if status == '待處理':
        pending += 1
        pending_titles.append(title)
    elif '已向量化' in status:
        vectorized += 1

print()
print("📊 統計:")
print(f"   總筆記數: {total}")
print(f"   已向量化: {vectorized}")
print(f"   待處理: {pending}")

if total > 0:
    percent = int(vectorized * 100 / total)
    print(f"   進度: {percent}%")

print()
if pending == 0:
    print("✅ 所有筆記已完成向量處理！")
else:
    print(f"⚠️ 還有 {pending} 筆記待處理")
    print()
    print("待處理筆記:")
    for t in pending_titles[:10]:
        print(f"   - {t}")
    if len(pending_titles) > 10:
        print(f"   ... 還有 {len(pending_titles) - 10} 個")

print()
print("========================================")
