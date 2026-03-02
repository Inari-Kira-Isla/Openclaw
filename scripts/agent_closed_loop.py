#!/usr/bin/env python3
"""
新 Agent 閉環系統 - New Agent Closed Loop System
整合創建、訓練、部署、監控於一體
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# 添加項目路徑
sys.path.insert(0, '/Users/ki/.openclaw/workspace/scripts')

from new_agent import NewAgentSystem
from agent_router import AgentRotationSystem
from feedback import FeedbackSystem

class AgentClosedLoopSystem:
    def __init__(self):
        self.agent_system = NewAgentSystem()
        self.router = AgentRotationSystem()
        self.feedback = FeedbackSystem()
        self.log_path = os.path.expanduser("~/.openclaw/workspace/memory/agent_closed_loop.jsonl")
        
    def log(self, stage, message):
        """記錄日誌"""
        entry = {
            "stage": stage,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        print(f"[{stage}] {message}")
    
    def detect_need(self):
        """1. 偵測需求"""
        self.log("detect", "偵測新 Agent 需求...")
        
        # 從反饋系統獲取需求
        pending_feedback = self.feedback.get_pending_feedback("suggestion")
        
        needs = []
        for fb in pending_feedback:
            if "new agent" in fb.get("content", "").lower():
                needs.append(fb)
        
        self.log("detect", f"發現 {len(needs)} 個需求")
        return needs
    
    def design(self, need):
        """2. 設計 Agent"""
        self.log("design", "設計新 Agent...")
        
        # 根據需求設計
        name = f"agent_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        template = "coder"  # 預設
        
        self.log("design", f"設計完成: {name} ({template})")
        return {"name": name, "template": template}
    
    def create(self, design):
        """3. 創建 Agent"""
        self.log("create", f"創建 Agent: {design['name']}...")
        
        agent = self.agent_system.create_agent(
            design["name"], 
            design["template"]
        )
        
        self.log("create", "創建完成")
        return agent
    
    def register(self, agent):
        """4. 註冊 Agent"""
        self.log("register", f"註冊 Agent: {agent['name']}...")
        
        result = self.agent_system.register_agent(agent["name"])
        
        self.log("register", "註冊完成")
        return result
    
    def train(self, agent):
        """5. 訓練 Agent"""
        self.log("train", f"訓練 Agent: {agent['name']}...")
        
        # 簡單訓練任務
        tasks = [
            "基礎任務測試",
            "團隊協作測試",
            "效能優化"
        ]
        
        results = self.agent_system.train_agent(agent["name"], tasks)
        
        self.log("train", f"訓練完成 ({len(results)} 任務)")
        return results
    
    def deploy(self, agent):
        """6. 部署 Agent"""
        self.log("deploy", f"部署 Agent: {agent['name']}...")
        
        result = self.agent_system.deploy_agent(agent["name"])
        
        self.log("deploy", "部署完成")
        
        # 添加到 Router
        self.router.enqueue_task(f"新 Agent {agent['name']} 已部署")
        
        return result
    
    def monitor(self, agent):
        """7. 監控效能"""
        self.log("monitor", f"監控 Agent: {agent['name']}...")
        
        perf = self.agent_system.monitor_agent(agent["name"])
        
        self.log("monitor", f"效能: {perf}")
        
        return perf
    
    def collect_feedback(self, agent, perf):
        """8. 收集反饋"""
        self.log("feedback", f"收集反饋: {agent['name']}...")
        
        # 根據效能收集反饋
        if perf.get("success_rate", 0) < 0.8:
            self.feedback.collect(
                "optimization",
                f"Agent {agent['name']} 效能不佳",
                f"成功率: {perf.get('success_rate', 0)}",
                source="closed_loop",
                priority="high"
            )
        
        self.log("feedback", "反饋收集完成")
    
    def full_cycle(self):
        """執行完整閉環"""
        self.log("START", "=== 新 Agent 閉環系統啟動 ===")
        
        # 1. 偵測需求
        needs = self.detect_need()
        
        if not needs:
            self.log("SKIP", "無新需求，跳過")
            return {"status": "skipped", "reason": "no_need"}
        
        for need in needs:
            self.log("PROCESS", f"處理需求: {need.get('title')}")
            
            # 2-8. 完整流程
            design = self.design(need)
            agent = self.create(design)
            self.register(agent)
            self.train(agent)
            self.deploy(agent)
            perf = self.monitor(agent)
            self.collect_feedback(agent, perf)
        
        self.log("END", "=== 閉環系統完成 ===")
        
        return {"status": "completed", "agents_processed": len(needs)}

# CLI
if __name__ == "__main__":
    acl = AgentClosedLoopSystem()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "run":
            acl.full_cycle()
        elif sys.argv[1] == "detect":
            needs = acl.detect_need()
            print(f"發現 {len(needs)} 個需求")
    else:
        print("🤖 New Agent Closed Loop System")
        print("用法:")
        print("  python agent_closed_loop.py run")
        print("  python agent_closed_loop.py detect")
