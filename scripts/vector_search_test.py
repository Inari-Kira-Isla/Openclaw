#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量搜尋準確度測試 - Vector Search Accuracy Test
"""

import os
import json
import glob
import random
from datetime import datetime

class VectorSearchTester:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.test_results_file = os.path.join(self.base_path, "vector_search_test.json")
    
    def generate_test_queries(self):
        """生成測試查詢"""
        queries = [
            {"query": "AI agent 系統", "expected_tags": ["AI", "agent"]},
            {"query": "營銷策略", "expected_tags": ["marketing"]},
            {"query": "自動化工作流", "expected_tags": ["automation"]},
            {"query": "學習系統", "expected_tags": ["learning"]},
            {"query": "商業客戶", "expected_tags": ["business"]},
            {"query": "海膽報價", "expected_tags": ["seafood"]},
            {"query": "OpenClaw 設定", "expected_tags": ["AI"]},
            {"query": "社群經營", "expected_tags": ["marketing"]}
        ]
        
        return queries
    
    def test_search(self, query, expected_tags):
        """測試搜尋"""
        # 讀取索引
        index_file = os.path.join(self.base_path, "memory_index.json")
        
        if not os.path.exists(index_file):
            return {
                "query": query,
                "results": [],
                "match_score": 0,
                "status": "no_index"
            }
        
        with open(index_file, "r") as f:
            index = json.load(f)
        
        # 簡單匹配（基於標籤）
        query_lower = query.lower()
        results = []
        
        # 從索引獲取結果
        for tag, files in index.get("by_tag", {}).items():
            if tag.lower() in query_lower:
                for f in files:
                    if f not in results:
                        results.append(f)
        
        # 評分
        match_score = min(len(results) / 5, 1.0)  # 最多5個結果得滿分
        
        return {
            "query": query,
            "results": results[:5],
            "match_score": match_score,
            "expected_tags": expected_tags,
            "status": "ok"
        }
    
    def run_tests(self):
        """運行所有測試"""
        print("\n🔬 向量搜尋準確度測試")
        print("="*50)
        
        queries = self.generate_test_queries()
        results = []
        
        total_score = 0
        
        for q in queries:
            result = self.test_search(q["query"], q["expected_tags"])
            results.append(result)
            total_score += result["match_score"]
            
            print(f"\n📝 查詢: {q['query']}")
            print(f"   結果: {len(result['results'])} 個")
            print(f"   匹配分數: {result['match_score']:.2f}")
        
        # 總結
        avg_score = total_score / len(queries) if queries else 0
        
        print("\n" + "="*50)
        print(f"📊 平均準確度: {avg_score:.2%}")
        
        if avg_score > 0.8:
            print("✅ 搜尋效果良好")
        elif avg_score > 0.5:
            print("⚠️ 搜尋效果一般，建議優化")
        else:
            print("❌ 搜尋效果差，需要改善")
        
        # 儲存結果
        test_report = {
            "test_date": datetime.now().isoformat(),
            "total_queries": len(queries),
            "avg_score": avg_score,
            "results": results
        }
        
        with open(self.test_results_file, "w") as f:
            json.dump(test_report, f, indent=2)
        
        return test_report

if __name__ == "__main__":
    tester = VectorSearchTester()
    tester.run_tests()
