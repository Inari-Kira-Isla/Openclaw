#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rhizome Executor 系統 - Root Execution System
根據知識圖譜自動觸發行動
"""

import os
import json
import subprocess
from datetime import datetime

class RhizomeExecutor:
    def __init__(self):
        self.execution_file = os.path.expanduser("~/.openclaw/workspace/memory/rhizome_executions.json")
        self.load_executions()
        
        # 動作模板
        self.action_templates = {
            "send_email": {
                "description": "發送郵件",
                "template": "自動生成郵件: {subject}"
            },
            "update_crm": {
                "description": "更新 CRM",
                "template": "更新客戶狀態: {customer}"
            },
            "generate_quote": {
                "description": "生成報價單",
                "template": "生成報價: {product}"
            },
            "notify_slack": {
                "description": "發送 Slack 通知",
                "template": "通知: {message}"
            },
            "create_reminder": {
                "description": "建立提醒",
                "template": "提醒: {task}"
            }
        }
    
    def load_executions(self):
        if os.path.exists(self.execution_file):
            with open(self.execution_file, "r") as f:
                self.executions = json.load(f)
        else:
            self.executions = {"records": [], "stats": {"total": 0, "success": 0, "failed": 0}}
    
    def save_executions(self):
        with open(self.execution_file, "w") as f:
            json.dump(self.executions, f, indent=2)
    
    def evaluate_trigger(self, node):
        """評估是否觸發動作"""
        # 高權重節點觸發
        if node.get("weight", 0) > 0.7:
            return True
        
        # 風險節點立即觸發
        if node.get("category") == "warning":
            return True
        
        # 商業機會觸發
        if node.get("category") == "opportunity":
            return True
        
        return False
    
    def determine_action(self, node):
        """決定動作類型"""
        category = node.get("category", "unknown")
        
        action_map = {
            "price": "generate_quote",
            "warning": "notify_slack",
            "opportunity": "create_reminder",
            "tech": "update_crm",
            "knowledge": "send_email"
        }
        
        return action_map.get(category, "notify_slack")
    
    def execute_action(self, action_type, params):
        """執行動作"""
        template = self.action_templates.get(action_type, {})
        
        execution = {
            "id": f"exec_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "action_type": action_type,
            "description": template.get("description", "未知動作"),
            "params": params,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        # 模擬執行
        try:
            # 實際實現可以調用對應的 API
            execution["status"] = "success"
            self.executions["stats"]["success"] += 1
            print(f"✅ 執行成功: {action_type}")
            
        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)
            self.executions["stats"]["failed"] += 1
            print(f"❌ 執行失敗: {e}")
        
        self.executions["records"].append(execution)
        self.executions["stats"]["total"] += 1
        self.save_executions()
        
        return execution
    
    def process_node(self, node):
        """處理單個節點"""
        if not self.evaluate_trigger(node):
            return None
        
        action_type = self.determine_action(node)
        
        params = {
            "node_id": node.get("id"),
            "node_label": node.get("label"),
            "category": node.get("category"),
            "weight": node.get("weight")
        }
        
        return self.execute_action(action_type, params)
    
    def process_graph(self, nodes):
        """處理整個知識圖譜"""
        print(f"\n🔄 處理 {len(nodes)} 個節點...")
        
        triggered = 0
        for node in nodes:
            result = self.process_node(node)
            if result:
                triggered += 1
        
        return triggered
    
    def get_pending_actions(self):
        """獲取待執行動作"""
        return [e for e in self.executions["records"] if e["status"] == "pending"]
    
    def get_stats(self):
        """獲取統計"""
        return self.executions["stats"]

if __name__ == "__main__":
    executor = RhizomeExecutor()
    
    # 測試節點
    test_nodes = [
        {"id": "1", "label": "海膽價格下跌", "category": "price", "weight": 0.9},
        {"id": "2", "label": "新投資機會", "category": "opportunity", "weight": 0.85},
        {"id": "3", "label": "技術更新", "category": "tech", "weight": 0.5},
    ]
    
    print("📊 Rhizome Executor 系統")
    print(f"處理的節點數: {executor.process_graph(test_nodes)}")
    print(f"統計: {executor.get_stats()}")
