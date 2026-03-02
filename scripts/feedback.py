#!/usr/bin/env python3
"""
反饋系統 - Feedback System
與鈎子結合的自動反饋收集與處理
"""

import os
import json
from datetime import datetime
from enum import Enum

class FeedbackType(Enum):
    PERFORMANCE = "performance"      # 效能反饋
    ERROR = "error"                  # 錯誤反饋
    SUGGESTION = "suggestion"      # 建議反饋
    LEARNING = "learning"           # 學習反饋
    OPTIMIZATION = "optimization"  # 優化反饋

class FeedbackPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class FeedbackSystem:
    def __init__(self):
        self.memory_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.feedback_file = os.path.join(self.memory_path, "feedback.jsonl")
        
    def collect(self, feedback_type, title, content, source="system", priority="medium", tags=None):
        """收集反饋"""
        record = {
            "type": "feedback",
            "feedback_type": feedback_type,
            "title": title,
            "content": content,
            "source": source,
            "priority": priority,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
            "status": "pending"  # pending, reviewed, implemented
        }
        
        # 保存
        os.makedirs(self.memory_path, exist_ok=True)
        with open(self.feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        print(f"✅ Feedback collected: {feedback_type} - {title}")
        
        # 如果是高優先級，立即觸發處理
        if priority in ["high", "critical"]:
            self.trigger_immediate_action(record)
        
        return record
    
    def trigger_immediate_action(self, feedback):
        """觸發即時行動"""
        print(f"⚠️ High priority feedback - triggering action: {feedback['title']}")
        
        # 可以觸發各種鈎子
        actions = {
            "performance": self.trigger_performance_check,
            "error": self.trigger_error_handler,
            "suggestion": self.trigger_review,
            "optimization": self.trigger_optimization
        }
        
        action = actions.get(feedback["feedback_type"])
        if action:
            action(feedback)
    
    def trigger_performance_check(self, feedback):
        """觸發效能檢查"""
        os.system("openclaw cron run agent-performance 2>/dev/null &")
    
    def trigger_error_handler(self, feedback):
        """觸發錯誤處理"""
        print("🔧 Triggering error handler...")
    
    def trigger_review(self, feedback):
        """觸發審查"""
        print("📋 Triggering review...")
    
    def trigger_optimization(self, feedback):
        """觸發優化"""
        print("⚡ Triggering optimization...")
    
    def get_pending_feedback(self, feedback_type=None):
        """獲取待處理反饋"""
        if not os.path.exists(self.feedback_file):
            return []
        
        results = []
        with open(self.feedback_file, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                if record.get("status") == "pending":
                    if feedback_type is None or record.get("feedback_type") == feedback_type:
                        results.append(record)
        return results
    
    def mark_reviewed(self, feedback_id):
        """標記為已審查"""
        self.update_status(feedback_id, "reviewed")
    
    def mark_implemented(self, feedback_id):
        """標記為已實施"""
        self.update_status(feedback_id, "implemented")
    
    def update_status(self, feedback_id, status):
        """更新狀態"""
        # 讀取所有記錄
        records = []
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                for line in f:
                    records.append(json.loads(line))
        
        # 更新狀態
        for record in records:
            if record.get("title") == feedback_id:
                record["status"] = status
        
        # 寫回
        with open(self.feedback_file, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

# CLI
if __name__ == "__main__":
    import sys
    
    fs = FeedbackSystem()
    
    if len(sys.argv) < 3:
        print("Feedback System CLI")
        print("用法:")
        print("  python feedback.py collect <類型> <標題> <內容>")
        print("  python feedback.py list")
        print("  類型: performance, error, suggestion, learning, optimization")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "collect" and len(sys.argv) >= 5:
        feedback_type = sys.argv[2]
        title = sys.argv[3]
        content = sys.argv[4]
        fs.collect(feedback_type, title, content)
    
    elif cmd == "list":
        pending = fs.get_pending_feedback()
        print(f"📋 Pending Feedback ({len(pending)}):")
        for p in pending:
            print(f"  [{p['feedback_type']}] {p['title']} - {p['status']}")
