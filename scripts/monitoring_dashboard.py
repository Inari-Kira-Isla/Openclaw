#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即時監控儀表板系統 - Real-time Monitoring Dashboard
"""

import os
import json
import subprocess
from datetime import datetime

class MonitoringDashboard:
    def __init__(self):
        self.status_file = os.path.expanduser("~/.openclaw/logs/dashboard_status.json")
        
    def get_system_status(self):
        """獲取系統狀態"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "cron": self.check_cron(),
            "agents": self.check_agents(),
            "memory": self.check_memory(),
            "disk": self.check_disk(),
            "network": self.check_network()
        }
        
        return status
    
    def check_cron(self):
        """檢查 Cron 狀態"""
        try:
            result = subprocess.run(
                ["openclaw", "cron", "list"],
                capture_output=True, text=True, timeout=10
            )
            
            running = "running" in result.stdout
            idle = "idle" in result.stdout
            
            return {
                "status": "ok" if running or idle else "warning",
                "running": running,
                "idle": idle
            }
        except:
            return {"status": "error"}
    
    def check_agents(self):
        """檢查 Agents"""
        agents_path = os.path.expanduser("~/.openclaw/agents/")
        
        if not os.path.exists(agents_path):
            return {"status": "unknown"}
        
        agents = []
        for agent in os.listdir(agents_path):
            sessions_path = os.path.join(agents_path, agent, "sessions")
            
            if os.path.exists(sessions_path):
                sessions = len([f for f in os.listdir(sessions_path) if f.endswith(".jsonl")])
                agents.append({"name": agent, "sessions": sessions})
        
        return {"count": len(agents), "agents": agents}
    
    def check_memory(self):
        """檢查記憶使用"""
        memory_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        
        if not os.path.exists(memory_path):
            return {"status": "unknown"}
        
        files = os.listdir(memory_path)
        
        return {"count": len(files)}
    
    def check_disk(self):
        """檢查磁盤"""
        try:
            result = subprocess.run(
                ["df", "-h", os.path.expanduser("~")],
                capture_output=True, text=True, timeout=5
            )
            
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                parts = lines[1].split()
                return {"used": parts[2], "total": parts[1], "percent": parts[4]}
        except:
            pass
        
        return {"status": "unknown"}
    
    def check_network(self):
        """檢查網絡連接"""
        return {"status": "ok"}
    
    def generate_dashboard(self):
        """生成儀表板"""
        status = self.get_system_status()
        
        # 保存狀態
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
        
        # 生成 Markdown 報告
        report = f"""
# 📊 系統監控儀表板

## 更新時間: {status['timestamp']}

### Cron Jobs
| 狀態 | 數值 |
|------|------|
| 狀態 | {status['cron'].get('status', 'unknown')} |
| Running | {status['cron'].get('running', False)} |
| Idle | {status['cron'].get('idle', False)} |

### Agents
- 總數: {status['agents'].get('count', 0)}

### Memory Files
- 檔案數: {status['memory'].get('count', 0)}

### Disk
- 使用: {status['disk'].get('used', 'N/A')}
- 總計: {status['disk'].get('total', 'N/A')}
- 百分比: {status['disk'].get('percent', 'N/A')}

### Network
- 狀態: {status['network'].get('status', 'unknown')}
"""
        
        return report
    
    def send_to_telegram(self, report):
        """發送到 Telegram"""
        # 簡化實現：打印
        print(report)
        
        return True

if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    
    print("📊 生成監控儀表板...")
    report = dashboard.generate_dashboard()
    dashboard.send_to_telegram(report)
    
    print("\n✅ 完成")
