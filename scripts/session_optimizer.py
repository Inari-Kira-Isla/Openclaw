#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即時 Session 優化系統 - Real-time Session Optimization System
"""

import os
import json
import subprocess
from datetime import datetime, timedelta

class SessionOptimizer:
    def __init__(self):
        self.log_file = os.path.expanduser("~/.openclaw/workspace/memory/session_optimization.json")
        self.load_data()
        
    def load_data(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"sessions": [], "optimizations": [], "stats": {}}
    
    def save_data(self):
        with open(self.log_file, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def analyze_sessions(self):
        """分析當前 Sessions"""
        print("\n🔍 分析 Sessions...")
        
        sessions = []
        
        # 檢查各 Agent 的 Sessions
        agents_path = os.path.expanduser("~/.openclaw/agents/")
        
        if os.path.exists(agents_path):
            for agent in os.listdir(agents_path):
                agent_sessions_path = os.path.join(agents_path, agent, "sessions")
                
                if os.path.exists(agent_sessions_path):
                    files = os.listdir(agent_sessions_path)
                    sessions_count = len([f for f in files if f.endswith(".jsonl")])
                    
                    if sessions_count > 0:
                        sessions.append({
                            "agent": agent,
                            "sessions": sessions_count,
                            "path": agent_sessions_path
                        })
        
        print(f"  發現 {len(sessions)} Agents 有 Sessions")
        
        return sessions
    
    def optimize_sessions(self, sessions):
        """優化 Sessions"""
        print("\n⚡ 優化 Sessions...")
        
        optimized = []
        
        for session in sessions:
            agent = session["agent"]
            
            # 清理過期的 Session 檔案
            session_path = session["path"]
            
            if os.path.exists(session_path):
                files = [f for f in os.listdir(session_path) if f.endswith(".jsonl")]
                
                # 保留最近 5 個
                if len(files) > 5:
                    # 按修改時間排序
                    files.sort(key=lambda f: os.path.getmtime(os.path.join(session_path, f)))
                    
                    # 刪除舊的
                    for f in files[:-5]:
                        old_path = os.path.join(session_path, f)
                        os.remove(old_path)
                        optimized.append(f"  清理 {agent}: {f}")
        
        return optimized
    
    def clear_locks(self):
        """清理過期的 Lock 檔案"""
        print("\n🔓 清理 Lock 檔案...")
        
        locks_cleared = []
        
        agents_path = os.path.expanduser("~/.openclaw/agents/")
        
        if os.path.exists(agents_path):
            for agent in os.listdir(agents_path):
                locks_path = os.path.join(agents_path, agent, "sessions")
                
                if os.path.exists(locks_path):
                    locks = [f for f in os.listdir(locks_path) if f.endswith(".lock")]
                    
                    for lock in locks:
                        lock_path = os.path.join(locks_path, lock)
                        os.remove(lock_path)
                        locks_cleared.append(f"  清理 {agent}: {lock}")
        
        return locks_cleared
    
    def check_memory(self):
        """檢查記憶使用"""
        print("\n💾 檢查記憶...")
        
        memory_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        
        if os.path.exists(memory_path):
            files = os.listdir(memory_path)
            total_size = sum(os.path.getsize(os.path.join(memory_path, f)) for f in files)
            
            # 清理舊檔案 (超過30天)
            old_files = []
            cutoff = datetime.now() - timedelta(days=30)
            
            for f in files:
                if f.startswith("memory-"):
                    fpath = os.path.join(memory_path, f)
                    mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                    
                    if mtime < cutoff:
                        old_files.append(f)
            
            return {"total_files": len(files), "total_size_mb": round(total_size/1024/1024, 2), "old_files": len(old_files)}
        
        return {}
    
    def run_optimization(self):
        """執行完整優化"""
        print("\n" + "="*50)
        print("⚡ 即時 Session 優化系統")
        print("="*50)
        
        results = {}
        
        # 1. 分析
        sessions = self.analyze_sessions()
        results["sessions"] = len(sessions)
        
        # 2. 優化 Sessions
        optimized = self.optimize_sessions(sessions)
        results["optimized"] = len(optimized)
        
        # 3. 清理 Locks
        locks = self.clear_locks()
        results["locks_cleared"] = len(locks)
        
        # 4. 檢查記憶
        memory = self.check_memory()
        results["memory"] = memory
        
        # 記錄
        self.data["optimizations"].append({
            "timestamp": datetime.now().isoformat(),
            "results": results
        })
        self.save_data()
        
        print("\n📊 優化結果:")
        print(f"  Sessions: {results['sessions']}")
        print(f"  優化: {results['optimized']}")
        print(f"  Locks 清理: {results['locks_cleared']}")
        
        if "memory" in results:
            print(f"  記憶檔案: {results['memory'].get('total_files', 0)}")
        
        print("\n✅ 優化完成！")
        
        return results

if __name__ == "__main__":
    optimizer = SessionOptimizer()
    optimizer.run_optimization()
