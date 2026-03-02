#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記憶主題聚類 - Memory Topic Clustering
自動建立跨記憶關聯
"""

import os
import json
import glob
from collections import defaultdict
from datetime import datetime

class MemoryClustering:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.cluster_file = os.path.join(self.base_path, "memory_clusters.json")
        self.load_clusters()
    
    def load_clusters(self):
        if os.path.exists(self.cluster_file):
            with open(self.cluster_file, "r") as f:
                self.clusters = json.load(f)
        else:
            self.clusters = {"clusters": [], "last_updated": None}
    
    def save_clusters(self):
        self.clusters["last_updated"] = datetime.now().isoformat()
        with open(self.cluster_file, "w") as f:
            json.dump(self.clusters, f, indent=2)
    
    def extract_keywords(self, content):
        """提取關鍵詞"""
        keywords = []
        
        # 預定義關鍵詞組
        keyword_groups = {
            "海膽": ["海膽", "海產", "龍蝦", "蟹"],
            "AI系統": ["AI", "人工智慧", "agent", "openclaw"],
            "營銷": ["營銷", "marketing", "推廣", "社群"],
            "學習": ["學習", "training", "education"],
            "自動化": ["自動化", "automation", "workflow"],
            "商務": ["商務", "business", "BNI", "客戶"]
        }
        
        content_lower = content.lower()
        
        for group, words in keyword_groups.items():
            if any(w in content_lower for w in words):
                keywords.append(group)
        
        return keywords
    
    def build_clusters(self):
        """建立聚類"""
        print("🔗 建立記憶主題聚類...")
        
        # 讀取所有記憶
        memories = {}
        
        for f in glob.glob(os.path.join(self.base_path, "*.md")):
            name = os.path.basename(f)
            
            if name in [".gitignore", "memory_clusters.json", "memory_index.json"]:
                continue
            
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                keywords = self.extract_keywords(content)
                
                memories[name] = {
                    "keywords": keywords,
                    "path": f,
                    "size": os.path.getsize(f)
                }
            
            except:
                continue
        
        # 建立聚類
        keyword_to_memories = defaultdict(list)
        
        for mem, data in memories.items():
            for kw in data["keywords"]:
                keyword_to_memories[kw].append(mem)
        
        # 轉換為聚類列表
        clusters = []
        
        for keyword, mems in keyword_to_memories.items():
            if len(mems) > 1:  # 只包含多於1個記憶的聚類
                clusters.append({
                    "topic": keyword,
                    "memories": mems,
                    "count": len(mems)
                })
        
        # 按數量排序
        clusters.sort(key=lambda x: x["count"], reverse=True)
        
        self.clusters["clusters"] = clusters
        self.save_clusters()
        
        print(f"   ✅ 建立 {len(clusters)} 個主題聚類")
        
        # 顯示
        for c in clusters[:5]:
            print(f"   📌 {c['topic']}: {c['count']} 個記憶")
        
        return clusters
    
    def find_related(self, memory_name):
        """查找相關記憶"""
        if not self.clusters["clusters"]:
            self.build_clusters()
        
        # 找到所屬聚類
        for cluster in self.clusters["clusters"]:
            if memory_name in cluster["memories"]:
                related = [m for m in cluster["memories"] if m != memory_name]
                return {
                    "memory": memory_name,
                    "topic": cluster["topic"],
                    "related": related
                }
        
        return None

if __name__ == "__main__":
    clustering = MemoryClustering()
    clustering.build_clusters()
    
    # 測試
    print("\n🔍 測試關聯查找:")
    test_memories = ["lobster-system.md", "marketing.md", "agent-learning-2026-02-24.md"]
    
    for mem in test_memories:
        result = clustering.find_related(mem)
        if result:
            print(f"\n   {mem}:")
            print(f"   主題: {result['topic']}")
            print(f"   相關: {result['related'][:3]}")
