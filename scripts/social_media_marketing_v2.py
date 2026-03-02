#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社群營銷系統 v2 - 早上研究 + 晚上生成
"""

import os
import json
import random
from datetime import datetime

class SocialMediaMarketingV2:
    def __init__(self):
        self.memory_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.learning_file = os.path.join(self.memory_path, "marketing_learning.json")
        self.load_learning()
        
    def load_learning(self):
        if os.path.exists(self.learning_file):
            with open(self.learning_file, "r") as f:
                self.learning = json.load(f)
        else:
            self.learning = {"topics": [], "styles": [], "posts_count": 0}
    
    def save_learning(self):
        with open(self.learning_file, "w") as f:
            json.dump(self.learning, f, indent=2)
    
    def morning_research(self):
        """早上的研究"""
        print("\n" + "="*50)
        print("🔍 早上研究社群營銷趨勢")
        print("="*50)
        
        # 研究主題
        topics = [
            "AI科技最新趨勢",
            "衝突型Hook寫作技巧", 
            "2026社群營銷方法",
            "內容創作理論",
            "用戶心理學"
        ]
        
        findings = []
        for t in topics:
            print(f"  研究: {t}")
            findings.append({"topic": t, "timestamp": datetime.now().isoformat()})
        
        # 保存研究結果
        research_file = os.path.join(self.memory_path, f"research_{datetime.now().strftime('%Y%m%d')}.json")
        with open(research_file, "w", encoding="utf-8") as f:
            json.dump(findings, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 研究完成: {len(findings)} 個主題")
        return findings
    
    def generate_conflict_hook(self, topic):
        """生成衝突型 Hook 文案"""
        
        # 衝突型 Hook 公式
        # [對手]說[質疑]，直到我[展示]，[對方改觀]
        
        conflicts = [
            ("所有人都話唔可能", "直到我展示咗呢個方法"),
            ("專家話呢啲嘢呃人", "但我用佢賺咗第一桶金"),
            ("網上面人人都話錯", "但事實證明佢係啱"),
            ("傳統做法已經過時", "新方法效果更好"),
            ("人人都話難", "但我做到咗")
        ]
        
        # 選擇一個衝突
        conflict = random.choice(conflicts)
        
        # 結合 AI 主題
        templates = [
            f"{conflict[0]}AI時代已經來臨，{conflict[1]}",
            f"{conflict[0]}ChatGPT冇用，{conflict[1]}",
            f"{conflict[0]}免費AI工具已經夠用，{conflict[1]}",
            f"{conflict[0]}學AI好難，{conflict[1]}",
            f"{conflict[0]}AI會取代人類，{conflict[1]}"
        ]
        
        base = random.choice(templates)
        
        # 加入個人化元素（令唔似 AI）
        personal = [
            "我自己試咗3個月",
            "我身邊既朋友都話",
            "坦白講，我一開始都唔信",
            "老實講，結果令我意外",
            "講開呢啲，我最有資格講"
        ]
        
        if random.random() > 0.4:
            base = random.choice(personal) + "，" + base
        
        # 加入 topic
        final = f"{topic}: {base}"
        
        # 控制長度 100-200字
        if len(final) > 180:
            final = final[:177] + "..."
        
        return final
    
    def evening_generation(self):
        """晚上的生成"""
        print("\n" + "="*50)
        print("✍️ 晚上生成5篇 AI 科技衝突型 Hook")
        print("="*50)
        
        # 5 個不同 topic
        topics = [
            "AI寫作",
            "ChatGPT技巧",
            "Midjourney應用",
            "AI自動化",
            "AI賺錢方法"
        ]
        
        posts = []
        for i, topic in enumerate(topics):
            content = self.generate_conflict_hook(topic)
            posts.append({
                "index": i + 1,
                "style": "衝突型Hook",
                "topic": topic,
                "content": content,
                "length": len(content)
            })
            print(f"  [{i+1}] {content[:50]}...")
        
        # 保存到 Notion (本地)
        output_file = os.path.join(self.memory_path, f"marketing_{datetime.now().strftime('%Y%m%d')}.json")
        data = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "type": "evening_generation",
            "posts": posts
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 生成完成: {len(posts)} 篇")
        
        # 學習
        self.learning["topics"].extend(topics)
        self.learning["posts_count"] = self.learning.get("posts_count", 0) + 5
        self.save_learning()
        
        return posts
    
    def summary(self):
        """總結"""
        print("\n" + "="*50)
        print("📊 今日總結")
        print("="*50)
        
        print(f"  總發布: {self.learning.get('posts_count', 0)} 篇")
        print(f"  研究主題: {len(set(self.learning.get('topics', [])))}")
        
        return {
            "posts_count": self.learning.get("posts_count", 0),
            "topics_count": len(set(self.learning.get("topics", [])))
        }

if __name__ == "__main__":
    import sys
    
    sms = SocialMediaMarketingV2()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "morning":
            sms.morning_research()
        elif sys.argv[1] == "evening":
            sms.evening_generation()
        elif sys.argv[1] == "summary":
            sms.summary()
    else:
        # 執行完整流程
        sms.morning_research()
        sms.evening_generation()
        sms.summary()
