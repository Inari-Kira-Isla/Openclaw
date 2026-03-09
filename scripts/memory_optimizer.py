#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記憶體優化系統 - Memory Optimization System
"""

import os
import subprocess
from datetime import datetime

class MemoryOptimizer:
    def __init__(self):
        self.log_file = os.path.expanduser("~/.openclaw/logs/memory_optimization.log")
        
    def check_memory(self):
        """檢查記憶使用"""
        result = subprocess.run(
            ["vm_stat"],
            capture_output=True, text=True
        )
        
        lines = result.stdout.strip().split("\n")
        stats = {}
        
        for line in lines:
            if "Pages free:" in line:
                stats["free"] = int(line.split(":")[1].strip().rstrip("."))
            elif "Pages active:" in line:
                stats["active"] = int(line.split(":")[1].strip().rstrip("."))
            elif "Pages wired:" in line:
                stats["wired"] = int(line.split(":")[1].strip().rstrip("."))
        
        # Convert to MB (page size = 4KB)
        total = (stats.get("free", 0) + stats.get("active", 0) + stats.get("wired", 0)) * 4 / 1024
        
        return {
            "free_mb": round(stats.get("free", 0) * 4 / 1024, 2),
            "active_mb": round(stats.get("active", 0) * 4 / 1024, 2),
            "wired_mb": round(stats.get("wired", 0) * 4 / 1024, 2),
            "total_mb": round(total, 2)
        }
    
    def clean_browser_cache(self):
        """清理瀏覽器緩存"""
        print("🧹 清理瀏覽器緩存...")
        
        cache_path = os.path.expanduser("~/.openclaw/browser/openclaw/user-data")
        
        if os.path.exists(cache_path):
            # 只清理部分緩存，不刪除登入數據
            subprocess.run(["rm", "-rf", f"{cache_path}/Cache"], capture_output=True)
            subprocess.run(["rm", "-rf", f"{cache_path}/Code Cache"], capture_output=True)
            
            return True
        
        return False
    
    def clean_logs(self):
        """清理日誌"""
        print("📄 清理舊日誌...")
        
        log_path = os.path.expanduser("~/.openclaw/logs")
        count = 0
        
        if os.path.exists(log_path):
            for f in os.listdir(log_path):
                if f.endswith(".log") and os.path.getsize(os.path.join(log_path, f)) > 10 * 1024 * 1024:  # > 10MB
                    os.remove(os.path.join(log_path, f))
                    count += 1
        
        return count
    
    def clean_models_cache(self):
        """清理模型緩存"""
        print("🤖 清理模型緩存...")
        
        # 檢查是否有其他模型
        models_path = os.path.expanduser("~/.openclaw/models")
        
        if os.path.exists(models_path):
            files = [f for f in os.listdir(models_path) if f.endswith(".gguf")]
            return len(files)
        
        return 0
    
    def run_optimization(self):
        """執行優化"""
        print("\n" + "="*50)
        print("🧠 記憶體優化系統")
        print("="*50)
        
        # 優化前
        before = self.check_memory()
        print(f"\n優化前:")
        print(f"  Free: {before['free_mb']} MB")
        print(f"  Active: {before['active_mb']} MB")
        print(f"  Wired: {before['wired_mb']} MB")
        
        # 執行優化
        results = {}
        results["browser_cache"] = self.clean_browser_cache()
        results["logs"] = self.clean_logs()
        results["models"] = self.clean_models_cache()
        
        # 優化後
        after = self.check_memory()
        print(f"\n優化後:")
        print(f"  Free: {after['free_mb']} MB")
        
        freed = after['free_mb'] - before['free_mb']
        print(f"\n✅ 釋放: {round(freed, 2)} MB")
        
        return {
            "before": before,
            "after": after,
            "freed_mb": round(freed, 2),
            "actions": results
        }

if __name__ == "__main__":
    optimizer = MemoryOptimizer()
    optimizer.run_optimization()
