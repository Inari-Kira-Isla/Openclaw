#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記憶索引系統 - Memory Indexing System
自動為記憶建立標籤分類
"""

import os
import json
import glob
from datetime import datetime
from collections import defaultdict

class MemoryIndexer:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.index_file = os.path.join(self.base_path, "memory_index.json")
        self.load_index()
    
    def load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                self.index = json.load(f)
        else:
            self.index = {
                "by_tag": {},
                "by_date": {},
                "by_category": {},
                "last_updated": None
            }
    
    def save_index(self):
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, "w") as f:
            json.dump(self.index, f, indent=2)
    
    def extract_tags(self, content):
        """從內容提取標籤"""
        tags = []
        
        # 預設標籤映射
        tag_patterns = {
            "AI": ["ai", "人工智慧", "機器學習", "ml"],
            "marketing": ["marketing", "營銷", "推廣", "社群"],
            "automation": ["automation", "自動化", "workflow"],
            "openclaw": ["openclaw", "agent", "system"],
            "learning": ["learning", "學習", "training"],
            "business": ["business", "商業", "bni", "客戶"],
            "code": ["code", "代碼", "python", "script"],
            "knowledge": ["知識", "概念", "theory"]
        }
        
        content_lower = content.lower()
        
        for tag, patterns in tag_patterns.items():
            if any(p in content_lower for p in patterns):
                tags.append(tag)
        
        return tags
    
    def extract_category(self, filename):
        """從檔案名稱提取類別"""
        name = filename.lower()
        
        if "learning" in name or "study" in name:
            return "learning"
        elif "marketing" in name or "research" in name:
            return "marketing"
        elif "agent" in name or "evolution" in name:
            return "agent"
        elif "notion" in name or "sync" in name:
            return "notion"
        elif "trend" in name or "hourly" in name:
            return "trends"
        elif "daily" in name:
            return "daily"
        elif "system" in name or "architecture" in name:
            return "system"
        else:
            return "other"
    
    def build_index(self):
        """建立索引"""
        print("🔍 建立記憶索引...")
        
        # 重置索引
        self.index = {
            "by_tag": defaultdict(list),
            "by_date": defaultdict(list),
            "by_category": defaultdict(list),
            "last_updated": None
        }
        
        # 掃描所有 md 檔案
        md_files = glob.glob(os.path.join(self.base_path, "*.md"))
        
        for f in md_files:
            filename = os.path.basename(f)
            
            # 跳過系統檔案
            if filename in ["INDEX.md", "memory_index.json"]:
                continue
            
            # 讀取內容
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    content = fp.read()
            except:
                continue
            
            # 提取元數據
            tags = self.extract_tags(content)
            category = self.extract_category(filename)
            
            # 提取日期
            date = None
            if "2026-" in filename:
                date = filename[:10]  # YYYY-MM-DD
            
            # 建立索引
            entry = {
                "file": filename,
                "path": f,
                "category": category,
                "tags": tags,
                "date": date,
                "size": os.path.getsize(f)
            }
            
            # 按類別索引
            self.index["by_category"][category].append(filename)
            
            # 按標籤索引
            for tag in tags:
                self.index["by_tag"][tag].append(filename)
            
            # 按日期索引
            if date:
                self.index["by_date"][date].append(filename)
        
        self.save_index()
        
        # 輸出統計
        print(f"   📊 索引統計:")
        print(f"      總檔案: {len(md_files)}")
        print(f"      類別: {len(self.index['by_category'])}")
        print(f"      標籤: {len(self.index['by_tag'])}")
        print(f"      日期: {len(self.index['by_date'])}")
        
        return self.index
    
    def search(self, query):
        """搜尋"""
        results = []
        
        query_lower = query.lower()
        
        # 搜尋標籤
        if query_lower in self.index["by_tag"]:
            results.extend(self.index["by_tag"][query_lower])
        
        # 搜尋類別
        if query_lower in self.index["by_category"]:
            results.extend(self.index["by_category"][query_lower])
        
        # 去重
        results = list(set(results))
        
        return results
    
    def get_stats(self):
        """獲取統計"""
        return {
            "total_files": sum(len(v) for v in self.index["by_category"].values()),
            "categories": dict(self.index["by_category"]),
            "tags": list(self.index["by_tag"].keys()),
            "date_range": {
                "start": min(self.index["by_date"].keys()) if self.index["by_date"] else None,
                "end": max(self.index["by_date"].keys()) if self.index["by_date"] else None
            }
        }

if __name__ == "__main__":
    indexer = MemoryIndexer()
    indexer.build_index()
    
    # 測試搜尋
    print("\n🔍 測試搜尋:")
    for q in ["AI", "marketing", "agent"]:
        results = indexer.search(q)
        print(f"   {q}: {len(results)} 個檔案")
