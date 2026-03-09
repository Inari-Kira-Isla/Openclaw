#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
備份還原系統 - Backup & Restore System
"""

import os
import json
import shutil
import subprocess
from datetime import datetime
import tarfile
import gzip

class BackupRestore:
    def __init__(self):
        self.backup_dir = os.path.expanduser("~/.openclaw/backups/")
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.config = {
            "critical_files": [
                "workspace/TOOLS.md",
                "workspace/AGENTS.md", 
                "workspace/SOUL.md",
                "workspace/MEMORY.md",
                "workspace/enterprise-neural-system.md"
            ],
            "config_files": [
                "openclaw.json",
                "config/api-keys.yaml"
            ]
        }
    
    def create_backup(self, backup_type="full"):
        """創建備份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{backup_type}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        base = os.path.expanduser("~/.openclaw/")
        
        # 備份關鍵檔案
        backed_up = []
        
        if backup_type in ["full", "critical"]:
            for f in self.config["critical_files"]:
                src = os.path.join(base, f)
                if os.path.exists(src):
                    dst = os.path.join(backup_path, f)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    backed_up.append(f)
        
        if backup_type in ["full", "config"]:
            for f in self.config["config_files"]:
                src = os.path.join(base, f)
                if os.path.exists(src):
                    dst = os.path.join(backup_path, f)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    backed_up.append(f)
        
        # 創建壓縮包
        tar_path = os.path.join(self.backup_dir, f"{backup_name}.tar.gz")
        
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(backup_path, arcname=os.path.basename(backup_path))
        
        # 清理臨時目錄
        shutil.rmtree(backup_path)
        
        # 記錄元數據
        metadata = {
            "backup_type": backup_type,
            "timestamp": timestamp,
            "files": backed_up,
            "size": os.path.getsize(tar_path)
        }
        
        metadata_file = os.path.join(self.backup_dir, f"{backup_name}_meta.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # 清理舊備份（保留最近7個）
        self.clean_old_backups(7)
        
        print(f"✅ 備份完成: {backup_name}.tar.gz")
        
        return metadata
    
    def clean_old_backups(self, keep=7):
        """清理舊備份"""
        backups = sorted(
            [f for f in os.listdir(self.backup_dir) if f.startswith("backup_") and f.endswith(".tar.gz")],
            reverse=True
        )
        
        for old in backups[keep:]:
            os.remove(os.path.join(self.backup_dir, old))
            meta = old.replace(".tar.gz", "_meta.json")
            meta_path = os.path.join(self.backup_dir, meta)
            if os.path.exists(meta_path):
                os.remove(meta_path)
            print(f"🗑️ 清理舊備份: {old}")
    
    def restore_backup(self, backup_name):
        """還原備份"""
        backup_path = os.path.join(self.backup_dir, f"{backup_name}.tar.gz")
        
        if not os.path.exists(backup_path):
            print(f"❌ 備份不存在: {backup_name}")
            return False
        
        # 解壓
        temp_dir = os.path.join(self.backup_dir, "temp_restore")
        
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(temp_dir)
        
        # 還原檔案
        base = os.path.expanduser("~/.openclaw/")
        
        restored = []
        
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                src = os.path.join(root, f)
                rel_path = os.path.relpath(src, temp_dir)
                dst = os.path.join(base, rel_path)
                
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                restored.append(rel_path)
        
        # 清理
        shutil.rmtree(temp_dir)
        
        print(f"✅ 還原完成: {len(restored)} 個檔案")
        
        return restored
    
    def list_backups(self):
        """列出所有備份"""
        backups = []
        
        for f in os.listdir(self.backup_dir):
            if f.startswith("backup_") and f.endswith("_meta.json"):
                meta_path = os.path.join(self.backup_dir, f)
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    backups.append(meta)
        
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)

if __name__ == "__main__":
    import sys
    
    br = BackupRestore()
    
    if len(sys.argv) < 2:
        print("備份還原系統")
        print("用法:")
        print("  python backup_restore.py backup [full|critical|config]")
        print("  python backup_restore.py restore <backup_name>")
        print("  python backup_restore.py list")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "backup":
        btype = sys.argv[2] if len(sys.argv) > 2 else "full"
        br.create_backup(btype)
    
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("請指定備份名稱")
        else:
            br.restore_backup(sys.argv[2])
    
    elif cmd == "list":
        backups = br.list_backups()
        print(f"📦 可用備份 ({len(backups)}):")
        for b in backups:
            print(f"  - {b['timestamp']} ({b['backup_type']})")
