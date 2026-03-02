#!/usr/bin/env python3
"""
Agent 輪替系統 - Agent Rotation System
根據任務類型和 Agent 忙碌程度自動分配
"""

import os
import json
import subprocess
from datetime import datetime

# Agent 定義
AGENTS = {
    "kira": {
        "name": "Kira",
        "role": "協調者",
        "skills": ["coordination", "decision", "planning"],
        "agents": ["main", "knowledge-agent"]
    },
    "cynthia": {
        "name": "Cynthia", 
        "role": "知識庫",
        "skills": ["knowledge", "search", "faq"],
        "agents": ["memory-agent", "qa-agent"]
    },
    "slime": {
        "name": "史萊姆",
        "role": "學習優化",
        "skills": ["learning", "optimization", "prompt"],
        "agents": ["self-evolve-agent", "prompt-refiner"]
    },
    "team": {
        "name": "Team",
        "role": "執行者",
        "skills": ["execution", "task", "scheduling"],
        "agents": ["task-agent", "scheduler"]
    },
    "evolution": {
        "name": "Evolution",
        "role": "質疑者",
        "skills": ["analysis", "questioning", "performance"],
        "agents": ["analytics-agent", "performance-agent"]
    }
}

# 任務分類關鍵詞
TASK_KEYWORDS = {
    "coordination": ["協調", "計劃", "安排", "決定", "coordination"],
    "knowledge": ["知識", "查詢", "搜索", "資料", "knowledge"],
    "learning": ["學習", "優化", "改進", "提升", "learning"],
    "execution": ["執行", "任務", "操作", "完成", "execution"],
    "analysis": ["分析", "質疑", "檢討", "評估", "analysis"],
    "code": ["代碼", "程式", "開發", "code"],
    "creative": ["創作", "設計", "內容", "creative"]
}

class AgentRotationSystem:
    def __init__(self):
        self.queue_file = os.path.expanduser("~/.openclaw/workspace/memory/agent_queue.json")
        self.load_queue()
        
    def load_queue(self):
        """載入任務隊列"""
        if os.path.exists(self.queue_file):
            with open(self.queue_file, "r") as f:
                self.queue = json.load(f)
        else:
            self.queue = {"pending": [], "running": [], "completed": []}
    
    def save_queue(self):
        """保存任務隊列"""
        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        with open(self.queue_file, "w") as f:
            json.dump(self.queue, f, indent=2)
    
    def classify_task(self, task):
        """分類任務"""
        task_lower = task.lower()
        
        for category, keywords in TASK_KEYWORDS.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return category
        
        return "coordination"  # 預設
        
    def match_agent(self, category):
        """匹配最適合的 Agent"""
        # 根據 category 選擇對應的 bot
        mapping = {
            "coordination": "kira",
            "knowledge": "cynthia", 
            "learning": "slime",
            "execution": "team",
            "analysis": "evolution",
            "code": "slime",  # 代碼也給史萊姆優化
            "creative": "kira"  # 創意給 Kira 協調
        }
        
        return mapping.get(category, "kira")
    
    def enqueue_task(self, task, priority="normal"):
        """加入任務隊列"""
        category = self.classify_task(task)
        bot = self.match_agent(category)
        
        task_obj = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "task": task,
            "category": category,
            "assigned_bot": bot,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        # 按優先級排序
        priority_order = {"high": 0, "normal": 1, "low": 2}
        self.queue["pending"].append(task_obj)
        self.queue["pending"].sort(key=lambda x: priority_order.get(x["priority"], 1))
        
        self.save_queue()
        
        return task_obj
    
    def execute_task(self, task_obj):
        """執行任務"""
        bot = task_obj["assigned_bot"]
        
        # 實際執行 - 這裡調用對應的 Agent
        print(f"▶️ 執行任務: {task_obj['task']}")
        print(f"   分配給: {AGENTS[bot]['name']}")
        
        # 更新狀態
        task_obj["status"] = "running"
        task_obj["started_at"] = datetime.now().isoformat()
        
        # 這裡可以調用具體的 Agent
        # 例如使用 sessions_spawn 或其他方式
        
        return True
    
    def process_queue(self):
        """處理隊列"""
        results = []
        
        while self.queue["pending"]:
            task_obj = self.queue["pending"].pop(0)
            
            try:
                self.execute_task(task_obj)
                task_obj["status"] = "completed"
                task_obj["completed_at"] = datetime.now().isoformat()
            except Exception as e:
                task_obj["status"] = "failed"
                task_obj["error"] = str(e)
            
            self.queue["completed"].append(task_obj)
            results.append(task_obj)
            
            # 保持隊列不超過 100 個
            if len(self.queue["completed"]) > 100:
                self.queue["completed"] = self.queue["completed"][-100:]
        
        self.save_queue()
        return results
    
    def get_status(self):
        """獲取狀態"""
        return {
            "pending": len(self.queue["pending"]),
            "running": len(self.queue["running"]),
            "completed_today": len([c for c in self.queue["completed"] 
                if c.get("completed_at", "").startswith(datetime.now().strftime("%Y-%m-%d"))])
        }
    
    def get_best_agent(self, task):
        """獲取最適合的 Agent（單次任務）"""
        category = self.classify_task(task)
        bot_name = self.match_agent(category)
        
        return {
            "bot": bot_name,
            "name": AGENTS[bot_name]["name"],
            "role": AGENTS[bot_name]["role"],
            "category": category,
            "available_agents": AGENTS[bot_name]["agents"]
        }

# CLI
if __name__ == "__main__":
    import sys
    
    ars = AgentRotationSystem()
    
    if len(sys.argv) < 2:
        print("🤖 Agent Rotation System")
        print("用法:")
        print("  python agent_router.py add <任務>")
        print("  python agent_router.py process")
        print("  python agent_router.py status")
        print("  python agent_router.py match <任務>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        result = ars.enqueue_task(task)
        print(f"✅ 任務已加入隊列: {result['assigned_bot']} - {task}")
    
    elif cmd == "process":
        results = ars.process_queue()
        print(f"✅ 處理了 {len(results)} 個任務")
    
    elif cmd == "status":
        status = ars.get_status()
        print(f"📊 隊列狀態:")
        print(f"  等待中: {status['pending']}")
        print(f"  執行中: {status['running']}")
        print(f"  今日完成: {status['completed_today']}")
    
    elif cmd == "match" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        result = ars.get_best_agent(task)
        print(f"🎯 最佳匹配:")
        print(f"  Bot: {result['name']}")
        print(f"  角色: {result['role']}")
        print(f"  類別: {result['category']}")
        print(f"  可用 Agents: {', '.join(result['available_agents'])}")
