#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory 向量化系統 - Memory Vectorization System
自動將所有記憶檔案向量化
"""

import os
import json
import glob
import subprocess
from datetime import datetime

class MemoryVectorizer:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.vectors_path = os.path.expanduser("~/.openclaw/workspace/memory/vectors/")
        self.vector_db_path = os.path.expanduser("~/.openclaw/vectors/vec.db")
        self.ollama_model = "nomic-embed-text"
        
        os.makedirs(self.vectors_path, exist_ok=True)
    
    def get_embedding(self, text):
        """獲取向量"""
        import requests
        
        try:
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": self.ollama_model, "prompt": text[:500]},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("embedding", [])
            else:
                print(f"   ❌ API Error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            return None
    
    def vectorize_file(self, file_path):
        """向量化單個檔案"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 獲取向量
            embedding = self.get_embedding(content[:2000])  # Limit text length
            
            if embedding:
                return {
                    "file": os.path.basename(file_path),
                    "path": file_path,
                    "embedding": embedding,
                    "size": len(content),
                    "vectorized_at": datetime.now().isoformat()
                }
        
        except Exception as e:
            print(f"   ❌ Error vectorizing {file_path}: {e}")
        
        return None
    
    def vectorize_all(self):
        """向量化所有記憶"""
        print("\n🔄 開始向量化記憶...")
        
        # 獲取所有 md 檔案
        md_files = glob.glob(os.path.join(self.base_path, "*.md"))
        
        # 排除系統檔案
        exclude = ["memory_index.json", "memory_clusters.json", "training_log.json"]
        md_files = [f for f in md_files if os.path.basename(f) not in exclude]
        
        print(f"   找到 {len(md_files)} 個記憶檔案")
        
        vectors = []
        success = 0
        failed = 0
        
        for i, f in enumerate(md_files):
            print(f"   [{i+1}/{len(md_files)}] 向量化: {os.path.basename(f)}")
            
            result = self.vectorize_file(f)
            
            if result:
                vectors.append(result)
                success += 1
            else:
                failed += 1
        
        # 保存向量
        vector_file = os.path.join(self.vectors_path, "all_memories_vectors.json")
        
        with open(vector_file, "w") as f:
            json.dump(vectors, f, indent=2)
        
        print(f"\n✅ 向量化完成!")
        print(f"   成功: {success}")
        print(f"   失敗: {failed}")
        print(f"   總向量: {len(vectors)}")
        print(f"   保存至: {vector_file}")
        
        return vectors
    
    def search(self, query, top_k=5):
        """語義搜尋"""
        print(f"\n🔍 搜尋: {query}")
        
        # 獲取查詢向量
        query_embedding = self.get_embedding(query)
        
        if not query_embedding:
            print("   ❌ 無法獲取查詢向量")
            return []
        
        # 載入向量數據
        vector_file = os.path.join(self.vectors_path, "all_memories_vectors.json")
        
        if not os.path.exists(vector_file):
            print("   ❌ 未找到向量數據，請先向量化")
            return []
        
        with open(vector_file, "r") as f:
            vectors = json.load(f)
        
        # 計算相似度
        results = []
        
        for item in vectors:
            emb = item.get("embedding", [])
            
            if emb and query_embedding:
                # 簡單 cosine similarity
                dot = sum(a * b for a, b in zip(query_embedding, emb))
                norm1 = sum(a * a for a in query_embedding) ** 0.5
                norm2 = sum(a * a for a in emb) ** 0.5
                
                if norm1 > 0 and norm2 > 0:
                    similarity = dot / (norm1 * norm2)
                    results.append({
                        "file": item["file"],
                        "similarity": similarity,
                        "path": item["path"]
                    })
        
        # 排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 輸出結果
        print(f"\n📊 搜尋結果 (Top {top_k}):")
        
        for i, r in enumerate(results[:top_k]):
            print(f"   {i+1}. {r['file']} (相似度: {r['similarity']:.3f})")
        
        return results[:top_k]
    
    def update_vectors(self):
        """增量更新向量"""
        print("\n🔄 增量更新向量...")
        
        # 獲取現有向量
        vector_file = os.path.join(self.vectors_path, "all_memories_vectors.json")
        
        if os.path.exists(vector_file):
            with open(vector_file, "r") as f:
                existing = json.load(f)
            
            existing_files = {v["file"] for v in existing}
        else:
            existing = []
            existing_files = set()
        
        # 獲取所有 md 檔案
        md_files = glob.glob(os.path.join(self.base_path, "*.md"))
        
        new_files = [f for f in md_files if os.path.basename(f) not in existing_files]
        
        print(f"   新檔案: {len(new_files)}")
        
        # 向量化新檔案
        new_vectors = []
        
        for f in new_files:
            result = self.vectorize_file(f)
            if result:
                new_vectors.append(result)
        
        # 合併
        all_vectors = existing + new_vectors
        
        # 保存
        with open(vector_file, "w") as f:
            json.dump(all_vectors, f, indent=2)
        
        print(f"   ✅ 更新完成! 總向量: {len(all_vectors)}")
        
        return all_vectors

if __name__ == "__main__":
    import sys
    
    vectorizer = MemoryVectorizer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "search":
            query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "海膽 價格"
            vectorizer.search(query)
        
        elif sys.argv[1] == "update":
            vectorizer.update_vectors()
        
        else:
            print("用法:")
            print("  python memory_vectorizer.py       # 向量化所有")
            print("  python memory_vectorizer.py search <query>  # 搜尋")
            print("  python memory_vectorizer.py update # 增量更新")
    else:
        vectorizer.vectorize_all()
