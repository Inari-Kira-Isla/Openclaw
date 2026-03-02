#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
優化研究鉤子系統 - Optimized Research Hooks Runner
合併執行減少負擔
"""

import os
import sys
import json
from datetime import datetime

class OptimizedResearchRunner:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.results_file = os.path.join(self.base_path, "research_results.json")
        self.lock_file = os.path.join(self.base_path, ".research_hook.lock")
        
        # 合併的任務組
        self.task_groups = {
            "morning": {
                "time": "08:00",
                "tasks": ["market_research", "meeting_check", "daily_summary"]
            },
            "midday": {
                "time": "12:00", 
                "tasks": ["health_check", "system_status"]
            },
            "evening": {
                "time": "20:00",
                "tasks": ["finance_report", "token_analysis", "daily_review"]
            },
            "weekly": {
                "time": "monday_09:00",
                "tasks": ["japan_seafood", "weekly_summary", "trend_analysis"]
            }
        }
    
    def is_locked(self):
        """檢查鎖"""
        if os.path.exists(self.lock_file):
            # 檢查是否過期 (5分鐘)
            mtime = os.path.getmtime(self.lock_file)
            if datetime.now().timestamp() - mtime < 300:
                return True
            else:
                os.remove(self.lock_file)
        return False
    
    def acquire_lock(self):
        """獲取鎖"""
        with open(self.lock_file, "w") as f:
            f.write(str(datetime.now().timestamp()))
    
    def release_lock(self):
        """釋放鎖"""
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)
    
    def run_task(self, task_name):
        """執行單個任務"""
        print(f"\n📌 執行: {task_name}")
        
        try:
            if task_name == "market_research":
                # 市場研究
                os.system("python3 ~/.openclaw/workspace/scripts/hourly_trending.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            elif task_name == "meeting_check":
                # 會議檢查
                os.system("python3 ~/.openclaw/workspace/scripts/meeting_agent.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            elif task_name == "daily_summary":
                # 每日總結
                return {"task": task_name, "status": "skipped", "time": datetime.now().isoformat()}
            
            elif task_name == "health_check":
                # 健康檢查
                os.system("python3 ~/.openclaw/workspace/scripts/performance_alert.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            elif task_name == "system_status":
                # 系統狀態
                os.system("python3 ~/.openclaw/workspace/scripts/monitoring_dashboard.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            elif task_name == "finance_report":
                # 財務報告
                os.system("python3 ~/.openclaw/workspace/scripts/finance_agent.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            elif task_name == "token_analysis":
                # Token 分析
                os.system("python3 ~/.openclaw/workspace/scripts/token_analyzer.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            elif task_name == "daily_review":
                # 每日回顧
                return {"task": task_name, "status": "skipped", "time": datetime.now().isoformat()}
            
            elif task_name == "japan_seafood":
                # 日本水產
                return {"task": task_name, "status": "skipped", "time": datetime.now().isoformat()}
            
            elif task_name == "weekly_summary":
                # 每週總結
                return {"task": task_name, "status": "skipped", "time": datetime.now().isoformat()}
            
            elif task_name == "trend_analysis":
                # 趨勢分析
                os.system("python3 ~/.openclaw/workspace/scripts/memory_clustering.py > /dev/null 2>&1")
                return {"task": task_name, "status": "success", "time": datetime.now().isoformat()}
            
            else:
                return {"task": task_name, "status": "unknown", "time": datetime.now().isoformat()}
        
        except Exception as e:
            return {"task": task_name, "status": "error", "error": str(e), "time": datetime.now().isoformat()}
    
    def run_group(self, group_name):
        """執行任務組"""
        group = self.task_groups[group_name]
        results = []
        
        print(f"\n{'='*60}")
        print(f"🔗 執行任務組: {group_name}")
        print(f"⏰ 時間: {group['time']}")
        print(f"{'='*60}")
        
        for task in group["tasks"]:
            result = self.run_task(task)
            results.append(result)
        
        return results
    
    def run_all_optimized(self):
        """執行所有優化任務"""
        if self.is_locked():
            print("⚠️ 已有任務運行中，跳過")
            return []
        
        self.acquire_lock()
        
        try:
            # 根據時間執行對應任務組
            now = datetime.now()
            hour = now.hour
            
            results = []
            
            # 早上 (8點)
            if hour == 8:
                results.extend(self.run_group("morning"))
            
            # 中午 (12點)
            elif hour == 12:
                results.extend(self.run_group("midday"))
            
            # 晚上 (20點)
            elif hour == 20:
                results.extend(self.run_group("evening"))
            
            # 週一早上9點
            elif now.weekday() == 0 and hour == 9:
                results.extend(self.run_group("weekly"))
            
            # 總結
            success = len([r for r in results if r["status"] == "success"])
            skipped = len([r for r in results if r["status"] == "skipped"])
            
            print(f"\n{'='*60}")
            print(f"✅ 完成!")
            print(f"   成功: {success}")
            print(f"   跳過: {skipped}")
            print(f"{'='*60}")
            
            return results
        
        finally:
            self.release_lock()
    
    def get_status(self):
        """獲取狀態"""
        return {
            "groups": len(self.task_groups),
            "tasks": sum(len(g["tasks"]) for g in self.task_groups.values()),
            "locked": self.is_locked()
        }

if __name__ == "__main__":
    runner = OptimizedResearchRunner()
    
    if len(sys.argv) > 1:
        # 執行特定任務組
        group = sys.argv[1]
        if group in runner.task_groups:
            runner.run_group(group)
        else:
            print(f"未知任務組: {group}")
    else:
        # 執行所有優化任務
        runner.run_all_optimized()
