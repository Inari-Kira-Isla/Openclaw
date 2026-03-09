#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究分析鉤子系統 - Research Analysis Hooks
自動觸發各種研究和分析
"""

import os
import json
from datetime import datetime

class ResearchHooks:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.hooks_file = os.path.join(self.base_path, "research_hooks.json")
        self.load_hooks()
    
    def load_hooks(self):
        if os.path.exists(self.hooks_file):
            with open(self.hooks_file, "r") as f:
                self.hooks = json.load(f)
        else:
            self.hooks = {
                "hooks": [],
                "last_run": {}
            }
    
    def save_hooks(self):
        with open(self.hooks_file, "w") as f:
            json.dump(self.hooks, f, indent=2)
    
    def add_hook(self, name, trigger_type, action, schedule=None, conditions=None):
        """添加鉤子"""
        hook = {
            "id": f"hook_{len(self.hooks['hooks']) + 1}",
            "name": name,
            "trigger_type": trigger_type,  # schedule, event, manual
            "action": action,
            "schedule": schedule,
            "conditions": conditions or {},
            "enabled": True,
            "created_at": datetime.now().isoformat(),
            "last_run": None
        }
        
        self.hooks["hooks"].append(hook)
        self.save_hooks()
        
        return hook
    
    def run_hook(self, hook_id):
        """運行鉤子"""
        for hook in self.hooks["hooks"]:
            if hook["id"] == hook_id and hook["enabled"]:
                action = hook["action"]
                
                result = {
                    "hook_id": hook_id,
                    "name": hook["name"],
                    "action": action,
                    "executed_at": datetime.now().isoformat(),
                    "status": "success"
                }
                
                # 記錄執行
                hook["last_run"] = datetime.now().isoformat()
                self.hooks["last_run"][hook_id] = result
                self.save_hooks()
                
                return result
        
        return None
    
    def list_hooks(self):
        """列出所有鉤子"""
        return self.hooks["hooks"]
    
    def enable_hook(self, hook_id, enabled=True):
        """啟用/停用鉤子"""
        for hook in self.hooks["hooks"]:
            if hook["id"] == hook_id:
                hook["enabled"] = enabled
                self.save_hooks()
                return True
        return False

def setup_default_hooks():
    """設置默認鉤子"""
    hooks = ResearchHooks()
    
    # 1. 模型升級分析鉤子
    hooks.add_hook(
        name="Model Upgrade Analysis",
        trigger_type="schedule",
        action="run_model_upgrade_analysis",
        schedule="0 10 * * *",  # 每日10點
        conditions={"enabled": True}
    )
    
    # 2. 日本水產分析鉤子
    hooks.add_hook(
        name="Japan Seafood Analysis",
        trigger_type="schedule",
        action="run_japan_seafood_analysis",
        schedule="0 9 * * 1",  # 每周一9點
        conditions={"enabled": True}
    )
    
    # 3. Token 使用量鉤子
    hooks.add_hook(
        name="Token Usage Alert",
        trigger_type="schedule",
        action="check_token_usage",
        schedule="0 */2 * * *",  # 每2小時
        conditions={"budget_threshold": 80}  # 80% 預算
    )
    
    # 4. 市場研究鉤子
    hooks.add_hook(
        name="Market Research",
        trigger_type="schedule",
        action="run_market_research",
        schedule="0 8 * * *",  # 每日8點
        conditions={"categories": ["seafood", "ai", "trading"]}
    )
    
    # 5. 財務報告鉤子
    hooks.add_hook(
        name="Finance Report",
        trigger_type="schedule",
        action="run_finance_report",
        schedule="0 20 * * *",  # 每日8點
        conditions={"enabled": True}
    )
    
    # 6. 會議檢查鉤子
    hooks.add_hook(
        name="Meeting Reminder",
        trigger_type="schedule",
        action="check_meetings",
        schedule="0 8 * * *",  # 每日8點
        conditions={"remind_hours": 24}
    )
    
    # 7. 價格預警鉤子
    hooks.add_hook(
        name="Price Alert",
        trigger_type="event",
        action="check_price_alerts",
        schedule=None,
        conditions={"threshold_percent": 10}
    )
    
    # 8. 系統健康檢查鉤子
    hooks.add_hook(
        name="System Health",
        trigger_type="schedule",
        action="run_health_check",
        schedule="0 12 * * *",  # 每日12點
        conditions={"enabled": True}
    )
    
    return hooks.list_hooks()

if __name__ == "__main__":
    # 設置默認鉤子
    hooks = setup_default_hooks()
    
    print("\n" + "="*60)
    print("🔗 研究分析鉤子系統")
    print("="*60)
    
    print(f"\n✅ 已建立 {len(hooks)} 個鉤子:\n")
    
    for h in hooks:
        emoji = "✅" if h["enabled"] else "❌"
        print(f"   {emoji} {h['name']}")
        print(f"      類型: {h['trigger_type']}")
        print(f"      排程: {h['schedule'] or '手動觸發'}")
        print()
