#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slime 知識圖譜系統 - Slime Knowledge Graph System
"""

import os
import json
import random
from datetime import datetime
from collections import defaultdict

class SlimeKnowledgeGraph:
    def __init__(self):
        self.graph_file = os.path.expanduser("~/.openclaw/workspace/memory/slime_graph.json")
        self.load_graph()
    
    def load_graph(self):
        if os.path.exists(self.graph_file):
            with open(self.graph_file, "r", encoding="utf-8") as f:
                self.graph = json.load(f)
        else:
            self.graph = {
                "nodes": [],
                "edges": [],
                "clusters": []
            }
    
    def save_graph(self):
        with open(self.graph_file, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, ensure_ascii=False, indent=2)
    
    def add_node(self, label, category, weight=0.5, metadata=None):
        """添加節點"""
        node = {
            "id": f"node_{len(self.graph['nodes'])}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "label": label,
            "category": category,
            "weight": weight,
            "metadata": metadata or {},
            "connections": 0,
            "created_at": datetime.now().isoformat()
        }
        
        # 根據 category 設定顏色
        colors = {
            "price": "#FF6B6B",      # 紅色 - 價格/商業
            "tech": "#4ECDC4",       # 青色 - 技術
            "knowledge": "#95E1D3",   # 綠色 - 知識
            "warning": "#F38181",     # 紅色閃爍 - 風險
            "opportunity": "#FCE38A"  # 黃色 - 機會
        }
        
        node["color"] = colors.get(category, "#AAAAAA")
        
        self.graph["nodes"].append(node)
        
        return node
    
    def add_edge(self, source_id, target_id, relationship="linked"):
        """添加邊（連接）"""
        edge = {
            "source": source_id,
            "target": target_id,
            "relationship": relationship,
            "strength": random.uniform(0.3, 1.0),
            "created_at": datetime.now().isoformat()
        }
        
        # 更新節點連接數
        for node in self.graph["nodes"]:
            if node["id"] == source_id:
                node["connections"] = node.get("connections", 0) + 1
            if node["id"] == target_id:
                node["connections"] = node.get("connections", 0) + 1
        
        self.graph["edges"].append(edge)
        
        return edge
    
    def detect_patterns(self):
        """偵測模式"""
        patterns = []
        
        # 1. 發現高權重節點（商業機會）
        high_weight = [n for n in self.graph["nodes"] if n.get("weight", 0) > 0.7]
        if high_weight:
            patterns.append({
                "type": "opportunity",
                "message": f"發現 {len(high_weight)} 個高權重節點（商業機會）",
                "nodes": [n["label"] for n in high_weight[:5]]
            })
        
        # 2. 發現孤立節點（知識盲區）
        isolated = [n for n in self.graph["nodes"] if n.get("connections", 0) == 0]
        if isolated:
            patterns.append({
                "type": "blind_spot",
                "message": f"發現 {len(isolated)} 個孤立節點（知識盲區）",
                "nodes": [n["label"] for n in isolated[:5]]
            })
        
        # 3. 發現高連接節點（關鍵樞紐）
        hub = sorted(self.graph["nodes"], key=lambda x: x.get("connections", 0), reverse=True)[:3]
        if hub and hub[0].get("connections", 0) > 3:
            patterns.append({
                "type": "hub",
                "message": f"發現關鍵樞紐節點: {hub[0]['label']}",
                "nodes": [n["label"] for n in hub]
            })
        
        return patterns
    
    def generate_visualization(self):
        """生成視覺化數據"""
        # 根據權重設定節點大小
        nodes = []
        for node in self.graph["nodes"]:
            size = 20 + (node.get("weight", 0.5) * 40)
            
            # 風險節點閃爍
            if node.get("category") == "warning":
                size = 60
                node["pulsing"] = True
            
            nodes.append({
                "id": node["id"],
                "label": node["label"],
                "size": size,
                "color": node.get("color", "#AAAAAA"),
                "x": random.randint(100, 800),
                "y": random.randint(100, 600),
                "pulsing": node.get("pulsing", False)
            })
        
        edges = []
        for edge in self.graph["edges"]:
            edges.append({
                "source": edge["source"],
                "target": edge["target"],
                "strength": edge.get("strength", 0.5)
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "patterns": self.detect_patterns()
        }
    
    def add_from_content(self, content, tags):
        """從內容添加節點"""
        # 根據 tags 設定 category
        category_map = {
            "價格": "price",
            "技術": "tech",
            "知識": "knowledge",
            "風險": "warning",
            "機會": "opportunity"
        }
        
        category = "knowledge"
        for tag in tags:
            if tag in category_map:
                category = category_map[tag]
                break
        
        # 根據標籤設定權重
        weight = 0.5
        if any(t in tags for t in ["價格", "行情", "投資"]):
            weight = 0.9
        elif any(t in tags for t in ["原理", "理論"]):
            weight = 0.2
        
        node = self.add_node(
            label=content[:30],
            category=category,
            weight=weight,
            metadata={"tags": tags}
        )
        
        return node
    
    def get_stats(self):
        """獲取統計"""
        return {
            "total_nodes": len(self.graph["nodes"]),
            "total_edges": len(self.graph["edges"]),
            "categories": list(set(n.get("category", "unknown") for n in self.graph["nodes"])),
            "avg_connections": sum(n.get("connections", 0) for n in self.graph["nodes"]) / max(len(self.graph["nodes"]), 1)
        }

if __name__ == "__main__":
    import sys
    
    slime = SlimeKnowledgeGraph()
    
    # 添加一些測試節點
    slime.add_node("海膽報價", "price", 0.9)
    slime.add_node("AI技術", "tech", 0.7)
    slime.add_node("投資風險", "warning", 0.8)
    slime.add_node("新商機", "opportunity", 0.85)
    
    # 測試
    print("📊 Slime 知識圖譜系統")
    print(json.dumps(slime.get_stats(), indent=2))
    print("\n🔍 偵測模式:")
    print(json.dumps(slime.detect_patterns(), indent=2, ensure_ascii=False))
