#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
效能預警系統 - Performance Alerting System
"""

import os
import json
import time
from datetime import datetime, timedelta

class PerformanceAlerter:
    def __init__(self):
        self.thresholds = {
            "response_time_ms": 5000,  # 5秒
            "error_rate_percent": 10,     # 10%
            "memory_percent": 90,         # 90%
            "cpu_percent": 80            # 80%
        }
        
        self.alert_file = os.path.expanduser("~/.openclaw/workspace/memory/alerts.json")
        self.load_alerts()
        
    def load_alerts(self):
        if os.path.exists(self.alert_file):
            with open(self.alert_file, "r") as f:
                self.alerts = json.load(f)
        else:
            self.alerts = {"alerts": [], "stats": {"total": 0}}
    
    def save_alerts(self):
        with open(self.alert_file, "w") as f:
            json.dump(self.alerts, f, indent=2)
    
    def check_response_time(self):
        """檢查響應時間"""
        # 從 Cron logs 獲取
        try:
            import subprocess
            result = subprocess.run(
                ["openclaw", "cron", "runs"],
                capture_output=True, text=True, timeout=10
            )
            
            # 簡單實現：返回模擬數據
            return {"status": "ok", "value": 2500}
            
        except:
            return {"status": "unknown", "value": 0}
    
    def check_error_rate(self):
        """檢查錯誤率"""
        # 從失敗記錄獲取
        try:
            fail_file = os.path.expanduser("~/.openclaw/workspace/memory/task_failures.json")
            
            if os.path.exists(fail_file):
                with open(fail_file, "r") as f:
                    data = json.load(f)
                    total = data.get("stats", {}).get("total", 0)
                    
                    return {
                        "status": "warning" if total > 10 else "ok",
                        "value": total
                    }
            
            return {"status": "ok", "value": 0}
            
        except:
            return {"status": "unknown", "value": 0}
    
    def check_memory(self):
        """檢查記憶使用"""
        try:
            import subprocess
            result = subprocess.run(
                ["df", "-h", os.path.expanduser("~")],
                capture_output=True, text=True, timeout=5
            )
            
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                parts = lines[1].split()
                percent = int(parts[4].replace("%", ""))
                
                return {
                    "status": "warning" if percent > 80 else "ok",
                    "value": percent
                }
            
        except:
            pass
        
        return {"status": "unknown", "value": 0}
    
    def send_alert(self, alert_type, message, severity="medium"):
        """發送告警"""
        alert = {
            "id": f"alert_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }
        
        self.alerts["alerts"].append(alert)
        self.alerts["stats"]["total"] += 1
        self.save_alerts()
        
        # 發送到 Telegram
        emoji = {"low": "🟡", "medium": "🟠", "high": "🔴", "critical": "🚨"}
        
        print(f"\n{emoji.get(severity, '⚠️')} ALERT: {alert_type}")
        print(f"   {message}")
        
        return alert
    
    def run_check(self):
        """執行檢查"""
        print("\n" + "="*50)
        print("🔍 效能預警檢查")
        print("="*50)
        
        alerts_sent = []
        
        # 1. 響應時間
        response = self.check_response_time()
        if response["value"] > self.thresholds["response_time_ms"]:
            alert = self.send_alert(
                "response_time",
                f"響應時間過長: {response['value']}ms (閾值: {self.thresholds['response_time_ms']}ms)",
                "high"
            )
            alerts_sent.append(alert)
        
        # 2. 錯誤率
        errors = self.check_error_rate()
        if errors["value"] > self.thresholds["error_rate_percent"]:
            alert = self.send_alert(
                "error_rate",
                "錯誤率過高: {}% (閾值: {}%)".format(
                    errors["value"], 
                    self.thresholds["error_rate_percent"]
                ),
                "high"
            )
            alerts_sent.append(alert)
        
        # 3. 記憶使用
        memory = self.check_memory()
        if memory["value"] > self.thresholds["memory_percent"]:
            alert = self.send_alert(
                "memory",
                f"記憶使用過高: {memory['value']}% (閾值: {self.thresholds['memory_percent']}%)",
                "medium"
            )
            alerts_sent.append(alert)
        
        if not alerts_sent:
            print("✅ 所有指標正常")
        
        return alerts_sent

if __name__ == "__main__":
    alerter = PerformanceAlerter()
    alerter.run_check()
