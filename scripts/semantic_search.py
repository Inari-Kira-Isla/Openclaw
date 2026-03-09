#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
語義搜尋系統 - Semantic Search System
基於向量的語義搜尋
"""

import os
import json
import requests

class SemanticSearch:
    def __init__(self):
        self.vector_file = os.path.expanduser("~/.openclaw/workspace/memory/vectors/all_memories_vectors.json")
        self.ollama_url = "http://localhost:11434/api/embeddings"
        self.model = "nomic-embed-text"
        
        self.load_vectors()
    
    def load_vectors(self):
        if os.path.exists(self.vector_file):
            with open(self.vector_file, "r") as f:
                self.vectors = json.load(f)
            print(f"Loaded {len(self.vectors)} vectors")
        else:
            self.vectors = []
            print("No vectors found")
    
    def get_embedding(self, text):
        response = requests.post(
            self.ollama_url,
            json={"model": self.model, "prompt": text[:500]},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get("embedding", [])
        return None
    
    def cosine_similarity(self, a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a > 0 and norm_b > 0:
            return dot / (norm_a * norm_b)
        return 0
    
    def search(self, query, top_k=5):
        print(f"\n🔍 Semantic Search: {query}")
        
        # Get query embedding
        query_emb = self.get_embedding(query)
        
        if not query_emb:
            print("   ❌ Failed to get query embedding")
            return []
        
        # Calculate similarities
        results = []
        
        for item in self.vectors:
            emb = item.get("embedding", [])
            
            if emb:
                similarity = self.cosine_similarity(query_emb, emb)
                results.append({
                    "file": item.get("file", "unknown"),
                    "similarity": similarity
                })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Output
        print(f"\n📊 Top {top_k} Results:")
        
        for i, r in enumerate(results[:top_k]):
            print(f"   {i+1}. {r['file']} ({r['similarity']:.3f})")
        
        return results[:top_k]

if __name__ == "__main__":
    import sys
    
    searcher = SemanticSearch()
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        searcher.search(query)
    else:
        # Default test queries
        print("Testing semantic search...")
        searcher.search("海膽 價格")
        searcher.search("AI agent 系統")
        searcher.search("營銷 策略")
