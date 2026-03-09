#!/usr/bin/env python3
"""
Session & Data Cleanup Script
定期清理過期的 sessions、cron logs、臨時文件
"""

import os
import glob
import time
from datetime import datetime, timedelta

# 配置
MAX_CRON_LOGS = 20  # 保留最近20個 cron log
MAX_BACKUPS = 7     # 保留最近7個備份
MAX_MEMORY_DAYS = 30 # 記憶保留30天

def cleanup_cron_logs():
    """清理過期 cron logs"""
    log_dir = os.path.expanduser("~/.openclaw/cron/runs/")
    if not os.path.exists(log_dir):
        return 0
    
    logs = sorted(glob.glob(os.path.join(log_dir, "*.jsonl")), key=os.path.getmtime, reverse=True)
    removed = 0
    
    for log in logs[MAX_CRON_LOGS:]:
        os.remove(log)
        removed += 1
    
    print(f"🗑️ Cron logs: 清理了 {removed} 個")
    return removed

def cleanup_backups():
    """清理過期備份"""
    backup_dir = os.path.expanduser("~/.openclaw/backups/")
    if not os.path.exists(backup_dir):
        return 0
    
    backups = sorted(glob.glob(os.path.join(backup_dir, "backup-*")), key=os.path.getmtime, reverse=True)
    removed = 0
    
    for backup in backups[MAX_BACKUPS:]:
        os.system(f"rm -rf {backup}")
        removed += 1
    
    print(f"📦 Backups: 清理了 {removed} 個")
    return removed

def cleanup_memory():
    """清理過期記憶"""
    memory_dir = os.path.expanduser("~/.openclaw/workspace/memory/")
    if not os.path.exists(memory_dir):
        return 0
    
    cutoff = time.time() - (MAX_MEMORY_DAYS * 24 * 60 * 60)
    removed = 0
    
    for f in os.listdir(memory_dir):
        if f.startswith("memory-") or f.endswith(".tmp"):
            path = os.path.join(memory_dir, f)
            if os.path.getmtime(path) < cutoff:
                os.remove(path)
                removed += 1
    
    print(f"🧠 Memory: 清理了 {removed} 個")
    return removed

def cleanup_temp():
    """清理臨時文件"""
    temp_patterns = [
        "~/.openclaw/*.tmp",
        "~/.openclaw/logs/*.err",
        "~/.openclaw/logs/*.old"
    ]
    
    total = 0
    for pattern in temp_patterns:
        expanded = os.path.expanduser(pattern)
        files = glob.glob(expanded)
        for f in files:
            try:
                os.remove(f)
                total += 1
            except:
                pass
    
    print(f"📄 Temp files: 清理了 {total} 個")
    return total

def get_status():
    """獲取系統狀態"""
    print("\n📊 系統狀態:")
    
    # Cron logs
    log_dir = os.path.expanduser("~/.openclaw/cron/runs/")
    cron_count = len(glob.glob(os.path.join(log_dir, "*.jsonl"))) if os.path.exists(log_dir) else 0
    print(f"  Cron logs: {cron_count}")
    
    # Backups
    backup_dir = os.path.expanduser("~/.openclaw/backups/")
    backup_count = len(glob.glob(os.path.join(backup_dir, "backup-*"))) if os.path.exists(backup_dir) else 0
    print(f"  Backups: {backup_count}")
    
    # Memory files
    memory_dir = os.path.expanduser("~/.openclaw/workspace/memory/")
    memory_count = len([f for f in os.listdir(memory_dir) if f.endswith(".md")]) if os.path.exists(memory_dir) else 0
    print(f"  Memory files: {memory_count}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        get_status()
    else:
        print("🔧 開始清理系統...")
        total = 0
        total += cleanup_cron_logs()
        total += cleanup_backups()
        total += cleanup_memory()
        total += cleanup_temp()
        
        print(f"\n✅ 清理完成: 共 {total} 個項目")
        get_status()
