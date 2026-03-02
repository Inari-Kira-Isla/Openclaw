#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記憶自動歸檔系統 - Memory Auto-Archive System
30日前記憶自動壓縮
"""

import os
import json
import shutil
import tarfile
import glob
from datetime import datetime, timedelta

class MemoryArchiver:
    def __init__(self, days=30):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.archive_dir = os.path.join(self.base_path, "archives/")
        self.days = days
        
        os.makedirs(self.archive_dir, exist_ok=True)
    
    def get_old_files(self):
        """獲取需要歸檔的檔案"""
        cutoff = datetime.now() - timedelta(days=self.days)
        old_files = []
        
        for f in glob.glob(os.path.join(self.base_path, "*.md")):
            # 跳過系統檔案
            if os.path.basename(f) in ["INDEX.md", "memory_index.json"]:
                continue
            
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            
            if mtime < cutoff:
                old_files.append({
                    "path": f,
                    "name": os.path.basename(f),
                    "mtime": mtime.isoformat(),
                    "size": os.path.getsize(f)
                })
        
        return old_files
    
    def archive_files(self, files):
        """歸檔檔案"""
        if not files:
            print("✅ 沒有需要歸檔的檔案")
            return []
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"archive_{timestamp}"
        archive_path = os.path.join(self.archive_dir, archive_name)
        
        os.makedirs(archive_path, exist_ok=True)
        
        archived = []
        
        for f in files:
            src = f["path"]
            dst = os.path.join(archive_path, f["name"])
            
            shutil.copy2(src, dst)
            archived.append(f["name"])
            
            # 刪除原檔案
            os.remove(src)
        
        # 壓縮
        tar_path = os.path.join(self.archive_dir, f"{archive_name}.tar.gz")
        
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(archive_path, arcname=archive_name)
        
        # 清理目錄
        shutil.rmtree(archive_path)
        
        # 記錄元數據
        metadata = {
            "archive_date": timestamp,
            "files": archived,
            "count": len(archived),
            "size": os.path.getsize(tar_path)
        }
        
        metadata_file = os.path.join(self.archive_dir, f"{archive_name}_meta.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   ✅ 歸檔 {len(archived)} 個檔案")
        
        return archived
    
    def list_archives(self):
        """列出所有歸檔"""
        archives = []
        
        for f in os.listdir(self.archive_dir):
            if f.endswith("_meta.json"):
                meta_path = os.path.join(self.archive_dir, f)
                with open(meta_path, "r") as fp:
                    meta = json.load(fp)
                    archives.append(meta)
        
        return sorted(archives, key=lambda x: x["archive_date"], reverse=True)
    
    def restore_archive(self, archive_name):
        """還原歸檔"""
        tar_path = os.path.join(self.archive_dir, f"{archive_name}.tar.gz")
        
        if not os.path.exists(tar_path):
            print(f"❌ 歸檔不存在: {archive_name}")
            return []
        
        # 解壓到臨時目錄
        temp_dir = os.path.join(self.archive_dir, "temp_restore")
        
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(temp_dir)
        
        # 還原檔案
        restored = []
        
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                src = os.path.join(root, f)
                dst = os.path.join(self.base_path, f)
                
                shutil.copy2(src, dst)
                restored.append(f)
        
        # 清理
        shutil.rmtree(temp_dir)
        
        print(f"   ✅ 還原 {len(restored)} 個檔案")
        
        return restored
    
    def run(self):
        """執行歸檔"""
        print(f"\n🗄️ 記憶自動歸檔系統 (>{self.days}天)")
        print("="*50)
        
        old_files = self.get_old_files()
        
        print(f"   找到 {len(old_files)} 個舊檔案")
        
        if old_files:
            self.archive_files(old_files)
        
        # 顯示統計
        archives = self.list_archives()
        print(f"\n   總歸檔次數: {len(archives)}")
        
        return old_files

if __name__ == "__main__":
    import sys
    
    archiver = MemoryArchiver(days=30)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            archives = archiver.list_archives()
            print("📦 歸檔列表:")
            for a in archives:
                print(f"   - {a['archive_date']}: {a['count']} 個檔案")
        
        elif sys.argv[1] == "restore" and len(sys.argv) > 2:
            archiver.restore_archive(sys.argv[2])
        
        else:
            archiver.run()
    else:
        archiver.run()
