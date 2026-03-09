#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任務失敗記錄系統 - Task Failure Recording System
自動記錄失敗任務並觸發處理
"""

import os
import json
from datetime import datetime

class TaskFailureRecorder:
    def __init__(self):
        self.failure_file = os.path.expanduser("~/.openclaw/workspace/memory/task_failures.json")
        self.load_failures()
        
    def load_failures(self):
        if os.path.exists(self.failure_file):
            with open(self.failure_file, "r") as f:
                self.failures = json.load(f)
        else:
            self.failures = {"records": [], "stats": {"total": 0, "by_type": {}}}
    
    def save_failures(self):
        with open(self.failure_file, "w") as f:
            json.dump(self.failures, f, indent=2)
    
    def record_failure(self, task_name, error_type, error_message, context=None, severity="medium"):
        """記錄失敗任務"""
        record = {
            "id": f"fail_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "task_name": task_name,
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",  # pending, analyzing, resolved
            "retry_count": 0
        }
        
        self.failures["records"].append(record)
        self.failures["stats"]["total"] += 1
        
        # 統計
        if error_type not in self.failures["stats"]["by_type"]:
            self.failures["stats"]["by_type"][error_type] = 0
        self.failures["stats"]["by_type"][error_type] += 1
        
        self.save_failures()
        
        # 如果是高嚴重性，觸發告警
        if severity == "high":
            self.trigger_alert(record)
        
        return record
    
    def trigger_alert(self, record):
        """觸發告警"""
        print(f"⚠️ HIGH PRIORITY FAILURE: {record['task_name']}")
        print(f"   Error: {record['error_message']}")
        
        # 這裡可以觸發各種告警
    
    def get_pending_failures(self):
        """獲取待處理失敗"""
        return [f for f in self.failures["records"] if f["status"] == "pending"]
    
    def resolve_failure(self, failure_id, solution):
        """標記為已解決"""
        for f in self.failures["records"]:
            if f["id"] == failure_id:
                f["status"] = "resolved"
                f["solution"] = solution
                f["resolved_at"] = datetime.now().isoformat()
        
        self.save_failures()
    
    def get_stats(self):
        """獲取統計"""
        return self.failures["stats"]
    
    def analyze_patterns(self):
        """分析失敗模式"""
        patterns = {}
        
        for f in self.failures["records"]:
            error_type = f["error_type"]
            if error_type not in patterns:
                patterns[error_type] = 0
            patterns[error_type] += 1
        
        # 排序
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_patterns

# CLI
if __name__ == "__main__":
    import sys
    
    recorder = TaskFailureRecorder()
    
    if len(sys.argv) < 2:
        print("任務失敗記錄系統")
        print("用法:")
        print("  python task_failure.py record <任務名> <錯誤類型> <錯誤訊息>")
        print("  python task_failure.py list")
        print("  python task_failure.py stats")
        print("  python task_failure.py patterns")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "record" and len(sys.argv) >= 5:
        task_name = sys.argv[2]
        error_type = sys.argv[3]
        error_message = sys.argv[4]
        severity = sys.argv[5] if len(sys.argv) > 5 else "medium"
        
        recorder.record_failure(task_name, error_type, error_message, severity=severity)
        print(f"✅ 失敗記錄完成: {task_name}")
    
    elif cmd == "list":
        pending = recorder.get_pending_failures()
        print(f"📋 待處理失敗 ({len(pending)}):")
        for f in pending:
            print(f"  • {f['task_name']} - {f['error_type']} [{f['severity']}]")
    
    elif cmd == "stats":
        stats = recorder.get_stats()
        print(f"📊 失敗統計:")
        print(f"  總數: {stats['total']}")
        for t, c in stats['by_type'].items():
            print(f"  {t}: {c}")
    
    elif cmd == "patterns":
        patterns = recorder.analyze_patterns()
        print(f"🔍 失敗模式:")
        for p, c in patterns[:5]:
            print(f"  {p}: {c}次")
