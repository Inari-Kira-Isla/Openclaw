#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
優先向量化系統 - Priority Vectorization
根據優先級向量化記憶檔案
"""

import os
import json
import glob
import requests
from datetime import datetime

class PriorityVectorizer:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.output_file = os.path.join(self.base_path, "vectors/all_memories_vectors.json")
        self.model = "nomic-embed-text"
        
        # 優先級定義
        self.priority_patterns = [
            # 🔴 高優先級 (research, trends, analysis)
            {"pattern": ["research", "trend", "analysis", "report", "市場"], "priority": 3},
            # 🟡 中優先級 (daily, learning, agent)
            {"pattern": ["daily", "learning", "agent", "session", "筆記"], "priority": 2},
            # 🟢 低優先級 (config, setup, system)
            {"pattern": ["config", "setup", "system", "index"], "priority": 1}
        ]
    
    def get_priority(self, filename):
        """獲取檔案優先級"""
        name_lower = filename.lower()
        
        for pp in self.priority_patterns:
            for p in pp["pattern"]:
                if p in name_lower:
                    return pp["priority"]
        
        return 2  # 預設中等
    
    def get_files_by_priority(self):
        """根據優先級排序檔案"""
        # 獲取所有 md 檔案
        files = glob.glob(os.path.join(self.base_path, "*.md"))
        
        # 排除系統檔案
        exclude = ["memory_index.json", "memory_clusters.json", "training_log.json", "vectors.json"]
        files = [f for f in files if os.path.basename(f) not in exclude]
        
        # 添加優先級
        file_priority = []
        for f in files:
            priority = self.get_priority(os.path.basename(f))
            file_priority.append({
                "path": f,
                "name": os.path.basename(f),
                "priority": priority
            })
        
        # 按優先級排序 (高優先級在前)
        file_priority.sort(key=lambda x: x["priority"], reverse=True)
        
        return file_priority
    
    def vectorize_file(self, filepath):
        """向量化單個檔案"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()[:1000]  # 限制長度
            
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": self.model, "prompt": content},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "file": os.path.basename(filepath),
                    "embedding": data.get("embedding", []),
                    "priority": self.get_priority(os.path.basename(filepath)),
                    "vectorized_at": datetime.now().isoformat()
                }
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        return None
    
    def run_priority_vectorization(self, limit=None):
        """運行優先向量化"""
        files = self.get_files_by_priority()
        
        if limit:
            files = files[:limit]
        
        print("\n" + "="*60)
        print("🔄 優先向量化系統")
        print("="*60)
        
        print(f"\n📊 檔案優先級:")
        priority_counts = {3: 0, 2: 0, 1: 0}
        for f in files:
            priority_counts[f["priority"]] += 1
        
        print(f"   🔴 高優先級: {priority_counts[3]} 個")
        print(f"   🟡 中優先級: {priority_counts[2]} 個")
        print(f"   🟢 低優先級: {priority_counts[1]} 個")
        
        print(f"\n🚀 開始向量化 (共 {len(files)} 個)...")
        
        vectors = []
        success = 0
        failed = 0
        
        for i, f in enumerate(files):
            emoji = "🔴" if f["priority"] == 3 else "🟡" if f["priority"] == 2 else "🟢"
            print(f"   [{i+1}/{len(files)}] {emoji} {f['name']}")
            
            result = self.vectorize_file(f["path"])
            
            if result:
                vectors.append(result)
                success += 1
            else:
                failed += 1
        
        # 保存結果
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, "w") as f:
            json.dump(vectors, f)
        
        print(f"\n✅ 向量化完成!")
        print(f"   成功: {success}")
        print(f"   失敗: {failed}")
        print(f"   總向量: {len(vectors)}")
        print(f"   保存至: {self.output_file}")
        
        return vectors

if __name__ == "__main__":
    vectorizer = PriorityVectorizer()
    
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    vectorizer.run_priority_vectorization(limit)
