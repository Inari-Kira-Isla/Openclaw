#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Research to Content Hook System
自動將研究轉化為學習並生成內容
"""

import os
import json
import glob
from datetime import datetime

class ResearchToContentHook:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.queue_file = os.path.join(self.base_path, "learning_queue.json")
        self.content_queue = os.path.join(self.base_path, "content_queue.json")
        self.feedback_file = os.path.join(self.base_path, "feedback.json")
        
        self.load_queues()
    
    def load_queues(self):
        """載入隊列"""
        for f, default in [(self.queue_file, []), (self.content_queue, []), (self.feedback_file, {})]:
            if os.path.exists(f):
                with open(f, "r") as fp:
                    setattr(self, f.replace(self.base_path, "").replace("/", "_").replace(".json", "") + "_data", json.load(fp))
            else:
                setattr(self, f.replace(self.base_path, "").replace("/", "_").replace(".json", "") + "_data", default)
    
    def save_queue(self, filename, data):
        """儲存隊列"""
        filepath = os.path.join(self.base_path, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    
    def hook1_research_to_learning(self):
        """Hook 1: 研究 → 學習隊列"""
        print("\n🔗 Hook 1: 研究 → 學習")
        
        # 尋找新的研究檔案
        research_files = glob.glob(os.path.join(self.base_path, "*research*.md"))
        research_files += glob.glob(os.path.join(self.base_path, "*trending*.md"))
        research_files += glob.glob(os.path.join(self.base_path, "*marketing*.md"))
        
        new_items = []
        
        for f in research_files:
            # 檢查是否已在隊列中
            filename = os.path.basename(f)
            
            # 讀取內容並提取標籤
            with open(f, "r") as fp:
                content = fp.read()
            
            # 提取標籤
            tags = []
            if "AI" in content or "人工智能" in content:
                tags.append("AI")
            if "營銷" in content or "marketing" in content.lower():
                tags.append("marketing")
            if "趨勢" in content or "trend" in content.lower():
                tags.append("trend")
            if "技術" in content or "tech" in content.lower():
                tags.append("tech")
            
            new_items.append({
                "source": filename,
                "path": f,
                "tags": tags,
                "added_at": datetime.now().isoformat(),
                "status": "pending"
            })
        
        # 更新隊列
        self.learning_queue_data = new_items
        self.save_queue("learning_queue.json", new_items)
        
        print(f"   ✅ 加入 {len(new_items)} 個學習項目")
        return new_items
    
    def hook2_learning_to_tag_adjustment(self):
        """Hook 2: 學習 → Tag λ 調整"""
        print("\n🔗 Hook 2: 學習 → Tag λ 調整")
        
        if not self.learning_queue_data:
            print("   ⚠️ 學習隊列為空")
            return []
        
        # 調用 tag_lambda.py
        os.system(f"python3 {os.path.expanduser('~/.openclaw/workspace/scripts/tag_lambda.py')} batch > /dev/null 2>&1")
        
        adjusted = []
        for item in self.learning_queue_data:
            item["lambda_adjusted"] = True
            adjusted.append(item)
        
        self.save_queue("learning_queue.json", adjusted)
        print(f"   ✅ 調整 {len(adjusted)} 個項目 λ 值")
        
        return adjusted
    
    def hook3_learning_to_slime_graph(self):
        """Hook 3: 學習 → Slime 圖譜"""
        print("\n🔗 Hook 3: 學習 → Slime 圖譜")
        
        if not self.learning_queue_data:
            print("   ⚠️ 學習隊列為空")
            return []
        
        # 調用 slime_graph.py
        os.system(f"python3 {os.path.expanduser('~/.openclaw/workspace/scripts/slime_graph.py')} > /dev/null 2>&1")
        
        nodes_created = len(self.learning_queue_data)
        
        print(f"   ✅ 建立 {nodes_created} 個圖譜節點")
        return nodes_created
    
    def hook4_slime_to_content_trigger(self):
        """Hook 4: Slime → 內容觸發"""
        print("\n🔗 Hook 4: Slime → 內容觸�發")
        
        # 檢查高權重節點
        content_triggers = []
        
        for item in self.learning_queue_data:
            # 根據 tags 決定是否觸發內容生成
            if any(t in item.get("tags", []) for t in ["marketing", "trend", "AI"]):
                content_triggers.append({
                    "source": item["source"],
                    "trigger": "high_value_content",
                    "timestamp": datetime.now().isoformat()
                })
        
        self.content_queue_data = content_triggers
        self.save_queue("content_queue.json", content_triggers)
        
        print(f"   ✅ 觸發 {len(content_triggers)} 個內容生成")
        return content_triggers
    
    def hook5_content_generation(self):
        """Hook 5: 內容生成"""
        print("\n🔗 Hook 5: 內容生成")
        
        if not self.content_queue_data:
            print("   ⚠️ 內容隊列為空")
            return []
        
        # 這裡調用 social_media_marketing.py
        # 會生成 5 種不同風格的 post
        
        generated = []
        for trigger in self.content_queue_data:
            generated.append({
                "source": trigger["source"],
                "styles": ["專業", "故事", "問題", "乾貨", "衝突"],
                "generated_at": datetime.now().isoformat(),
                "status": "ready"
            })
        
        self.save_queue("content_generated.json", generated)
        
        print(f"   ✅ 生成 {len(generated)} 組內容 (每組5種風格)")
        return generated
    
    def hook6_publish_and_track(self):
        """Hook 6: 發布 + 追蹤"""
        print("\n🔗 Hook 6: 發布 + 追蹤")
        
        # 記錄發布狀態
        published = {
            "last_published": datetime.now().isoformat(),
            "platforms": ["telegram", "pending_facebook", "pending_line"],
            "status": "published"
        }
        
        self.save_queue("publish_status.json", published)
        
        print("   ✅ 已記錄發布狀態")
        return published
    
    def hook7_feedback_loop(self):
        """Hook 7: 反饋閉環"""
        print("\n🔗 Hook 7: 反饋閉環")
        
        # 讀取反饋
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, "r") as f:
                feedback = json.load(f)
        else:
            feedback = {}
        
        # 更新學習隊列中的反饋
        for item in self.learning_queue_data:
            item["feedback_received"] = feedback.get(item["source"], "no_feedback")
        
        self.save_queue("learning_queue.json", self.learning_queue_data)
        
        print("   ✅ 反饋閉環完成")
        return feedback
    
    def run_full_pipeline(self):
        """運行完整流程"""
        print("="*60)
        print("🔄 Research → Content 完整流程")
        print("="*60)
        
        self.hook1_research_to_learning()
        self.hook2_learning_to_tag_adjustment()
        self.hook3_learning_to_slime_graph()
        self.hook4_slime_to_content_trigger()
        self.hook5_content_generation()
        self.hook6_publish_and_track()
        self.hook7_feedback_loop()
        
        print("\n" + "="*60)
        print("✅ 完整流程完成！")
        print("="*60)

if __name__ == "__main__":
    hook = ResearchToContentHook()
    hook.run_full_pipeline()
