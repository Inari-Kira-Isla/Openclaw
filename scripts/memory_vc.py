#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記憶版本控制 - Memory Version Control
使用 Git 管理記憶版本
"""

import os
import subprocess
import shutil
from datetime import datetime

class MemoryVersionControl:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.git_dir = os.path.join(self.base_path, ".git")
        self.log_file = os.path.join(self.base_path, "version_log.json")
    
    def init_repo(self):
        """初始化 Git 倉庫"""
        if os.path.exists(self.git_dir):
            print("✅ Git 倉庫已存在")
            return True
        
        try:
            # 初始化 Git
            subprocess.run(["git", "init"], cwd=self.base_path, capture_output=True)
            
            # 配置 Git
            subprocess.run(["git", "config", "user.email", "kira@openclaw.ai"], cwd=self.base_path, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Kira"], cwd=self.base_path, capture_output=True)
            
            # 建立 .gitignore
            gitignore = """
# 忽略系統和臨時文件
*.log
*.jsonl
*.tmp
.DS_Store
.AppleDouble
.LSOverride
vectors/
archives/
"""
            with open(os.path.join(self.base_path, ".gitignore"), "w") as f:
                f.write(gitignore)
            
            # 首次提交
            subprocess.run(["git", "add", "."], cwd=self.base_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit - Memory system"], cwd=self.base_path, capture_output=True)
            
            print("✅ Git 倉庫初始化完成")
            return True
        
        except Exception as e:
            print(f"❌ 初始化失敗: {e}")
            return False
    
    def commit(self, message=None):
        """提交更改"""
        if not os.path.exists(self.git_dir):
            print("❌ Git 倉庫未初始化")
            return False
        
        if not message:
            message = f"Auto-commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            subprocess.run(["git", "add", "-A"], cwd=self.base_path, capture_output=True)
            result = subprocess.run(["git", "commit", "-m", message], cwd=self.base_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 提交成功: {message}")
                return True
            else:
                if "nothing to commit" in result.stderr:
                    print("ℹ️ 沒有需要提交的更改")
                else:
                    print(f"⚠️ 提交訊息: {result.stderr}")
                return False
        
        except Exception as e:
            print(f"❌ 提交失敗: {e}")
            return False
    
    def log(self, limit=10):
        """查看提交歷史"""
        if not os.path.exists(self.git_dir):
            print("❌ Git 倉庫未初始化")
            return []
        
        try:
            result = subprocess.run(
                ["git", "log", f"--max-count={limit}", "--oneline"],
                cwd=self.base_path, capture_output=True, text=True
            )
            
            commits = result.stdout.strip().split("\n")
            
            print(f"\n📜 最近 {len(commits)} 次提交:")
            for c in commits:
                if c:
                    print(f"   {c}")
            
            return commits
        
        except Exception as e:
            print(f"❌ 獲取歷史失敗: {e}")
            return []
    
    def diff(self, commit1=None, commit2=None):
        """查看差異"""
        if not os.path.exists(self.git_dir):
            return []
        
        try:
            if commit1 and commit2:
                result = subprocess.run(
                    ["git", "diff", commit1, commit2],
                    cwd=self.base_path, capture_output=True, text=True
                )
            elif commit1:
                result = subprocess.run(
                    ["git", "show", commit1],
                    cwd=self.base_path, capture_output=True, text=True
                )
            else:
                result = subprocess.run(
                    ["git", "diff", "--stat"],
                    cwd=self.base_path, capture_output=True, text=True
                )
            
            return result.stdout
        
        except Exception as e:
            return f"Error: {e}"
    
    def restore(self, commit, file_path=None):
        """還原到指定版本"""
        if not os.path.exists(self.git_dir):
            print("❌ Git 倉庫未初始化")
            return False
        
        try:
            if file_path:
                subprocess.run(
                    ["git", "checkout", commit, "--", file_path],
                    cwd=self.base_path, capture_output=True
                )
                print(f"✅ 已還原: {file_path}")
            else:
                subprocess.run(
                    ["git", "checkout", commit, "--", "."],
                    cwd=self.base_path, capture_output=True
                )
                print(f"✅ 已還原到: {commit}")
            
            return True
        
        except Exception as e:
            print(f"❌ 還原失敗: {e}")
            return False
    
    def branch(self, action="list"):
        """分支管理"""
        if not os.path.exists(self.git_dir):
            return []
        
        try:
            if action == "list":
                result = subprocess.run(
                    ["git", "branch", "-a"],
                    cwd=self.base_path, capture_output=True, text=True
                )
                return result.stdout.strip().split("\n")
            
            elif action == "current":
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.base_path, capture_output=True, text=True
                )
                return result.stdout.strip()
        
        except Exception as e:
            return []

if __name__ == "__main__":
    import sys
    
    vc = MemoryVersionControl()
    
    if len(sys.argv) < 2:
        print("記憶版本控制")
        print("用法:")
        print("  python memory_vc.py init          # 初始化")
        print("  python memory_vc.py commit       # 提交")
        print("  python memory_vc.py log          # 查看歷史")
        print("  python memory_vc.py diff         # 查看差異")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        vc.init_repo()
    
    elif cmd == "commit":
        msg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        vc.commit(msg)
    
    elif cmd == "log":
        vc.log()
    
    elif cmd == "diff":
        print(vc.diff())
    
    elif cmd == "branch":
        print("分支:", vc.branch("current"))
        print("所有分支:", vc.branch("list"))
