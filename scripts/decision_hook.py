#!/usr/bin/env python3
"""
Decision Hook System
==================
自動觸發的決策優化鉤子

Usage:
    python3 decision_hook.py install    # 安鉤子
   裝 python3 decision_hook.py trigger   # 觸發測試
    python3 decision_hook.py watch     # 監聽模式
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List

# ============================================================================
#  鉤子配置
# ============================================================================

HOOK_CONFIG = {
    "triggers": [
        {
            "name": "auto_decide",
            "pattern": ["下一步", "接下來", "要做什麼", "what's next"],
            "action": "trigger_auto_decide",
            "priority": 10
        },
        {
            "name": "low_confidence",
            "condition": "confidence < 0.5",
            "action": "trigger_claude",
            "priority": 20
        },
        {
            "name": "high_confidence",
            "condition": "confidence >= 0.8",
            "action": "trigger_autonomous",
            "priority": 15
        },
        {
            "name": "decision_complete",
            "pattern": ["完成", "結束", "done"],
            "action": "trigger_optimize",
            "priority": 5
        },
        {
            "name": "uncertain",
            "pattern": ["不確定", "不知道", "建議", "幫我決定"],
            "action": "trigger_claude",
            "priority": 25
        }
    ],
    "actions": {
        "trigger_auto_decide": {
            "type": "decision",
            "script": "~/.openclaw/workspace/scripts/auto_decide.py"
        },
        "trigger_claude": {
            "type": "spawn",
            "model": "claude",
            "prompt": "請幫我決定下一步行動..."
        },
        "trigger_autonomous": {
            "type": "execute",
            "script": "~/.openclaw/workspace/scripts/auto_decide.py"
        },
        "trigger_optimize": {
            "type": "learn",
            "script": "~/.openclaw/workspace/scripts/decision_tracker.py"
        }
    }
}

# ============================================================================
#  鉤子觸發器
# ============================================================================

class DecisionHook:
    """決策鉤子"""
    
    def __init__(self):
        self.hooks = HOOK_CONFIG
        self.history = []
        
    def check_trigger(self, message: str) -> List[Dict]:
        """檢查觸發條件"""
        triggered = []
        
        for trigger in self.hooks["triggers"]:
            # 模式匹配
            if "pattern" in trigger:
                for pattern in trigger["pattern"]:
                    if pattern in message.lower():
                        triggered.append(trigger)
                        break
            
            # 條件判斷（這裡可以擴展更多條件）
            if "condition" in trigger:
                # 暫時跳過，需要外部傳入變量
                pass
        
        # 按優先級排序
        triggered.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return triggered
    
    def execute_action(self, action_name: str, context: Dict = None) -> Dict:
        """執行鉤子動作"""
        if action_name not in self.hooks["actions"]:
            return {"error": f"Unknown action: {action_name}"}
        
        action = self.hooks["actions"][action_name]
        
        if action["type"] == "decision":
            # 執行自動決策
            return self._execute_decision(action, context)
        elif action["type"] == "spawn":
            # 調用 Claude
            return self._execute_spawn(action, context)
        elif action["type"] == "execute":
            # 執行腳本
            return self._execute_script(action, context)
        elif action["type"] == "learn":
            # 學習優化
            return self._execute_learn(action, context)
        
        return {"error": "Unknown action type"}
    
    def _execute_decision(self, action: Dict, context: Dict) -> Dict:
        """執行自動決策"""
        script = Path(action["script"]).expanduser()
        
        if not script.exists():
            return {"error": f"Script not found: {script}"}
        
        # 執行腳本
        import subprocess
        result = subprocess.run(
            ["python3", str(script), "--context", context.get("message", "")],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "action": "auto_decide",
            "result": result.stdout.strip(),
            "success": result.returncode == 0
        }
    
    def _execute_spawn(self, action: Dict, context: Dict) -> Dict:
        """執行 Claude 調用"""
        # 這裡可以調用 sessions_spawn
        return {
            "action": "claude_spawn",
            "model": action.get("model", "claude"),
            "prompt": action.get("prompt", ""),
            "note": "需要通過 OpenClaw sessions_spawn 執行"
        }
    
    def _execute_script(self, action: Dict, context: Dict) -> Dict:
        """執行腳本"""
        script = Path(action["script"]).expanduser()
        
        import subprocess
        result = subprocess.run(
            ["python3", str(script)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "action": "script_execute",
            "result": result.stdout.strip(),
            "success": result.returncode == 0
        }
    
    def _execute_learn(self, action: Dict, context: Dict) -> Dict:
        """執行學習優化"""
        script = Path(action["script"]).expanduser()
        
        import subprocess
        result = subprocess.run(
            ["python3", str(script), "optimize"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "action": "learn_optimize",
            "result": result.stdout.strip(),
            "success": result.returncode == 0
        }
    
    def process(self, message: str, context: Dict = None) -> Dict:
        """處理消息，觸發相應鉤子"""
        if context is None:
            context = {}
        
        context["message"] = message
        context["timestamp"] = datetime.now().isoformat()
        
        # 檢查觸發
        triggered = self.check_trigger(message)
        
        if not triggered:
            return {
                "triggered": False,
                "message": "No hooks triggered"
            }
        
        results = []
        for trigger in triggered:
            # 記錄
            self.history.append({
                "trigger": trigger["name"],
                "message": message,
                "timestamp": context["timestamp"]
            })
            
            # 執行動作
            result = self.execute_action(trigger["action"], context)
            results.append({
                "trigger": trigger["name"],
                "action": trigger["action"],
                "result": result
            })
        
        return {
            "triggered": True,
            "hooks": triggered,
            "results": results
        }

# ============================================================================
#  命令
# ============================================================================

def cmd_install():
    """安裝鉤子"""
    print("📦 安裝決策鉤子...")
    
    # 創建鉤子配置
    hook_dir = Path.home() / ".openclaw" / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = hook_dir / "decision.json"
    with open(config_file, "w") as f:
        json.dump(HOOK_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 鉤子配置已安裝: {config_file}")
    print(f"\n📋 鉤子列表:")
    for trigger in HOOK_CONFIG["triggers"]:
        print(f"   • {trigger['name']}: {trigger.get('pattern', trigger.get('condition', ''))}")

def cmd_trigger(message: str = "下一步要做什麼"):
    """觸發測試"""
    print(f"🧪 測試觸發: {message}")
    print("=" * 40)
    
    hook = DecisionHook()
    result = hook.process(message)
    
    print(f"\n結果:")
    print(f"   觸發: {'是' if result['triggered'] else '否'}")
    
    if result["triggered"]:
        print(f"   鉤子數: {len(result['hooks'])}")
        for r in result["results"]:
            print(f"\n   📌 {r['trigger']}:")
            if r["result"].get("result"):
                print(f"      {r['result']['result'][:200]}")
            else:
                print(f"      {r['result']}")

def cmd_watch():
    """監聽模式"""
    print("👀 監聽模式 (Ctrl+C 退出)")
    print("=" * 40)
    
    hook = DecisionHook()
    
    while True:
        try:
            message = input("\n> ").strip()
            if not message:
                continue
            
            result = hook.process(message)
            
            if result["triggered"]:
                print(f"\n✅ 觸發 {len(result['hooks'])} 個鉤子:")
                for r in result["results"]:
                    print(f"   • {r['trigger']}")
            
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("\n👋 監聽結束")

# ============================================================================
#  主入口
# ============================================================================

def main():
    if len(sys.argv) < 2:
        # 默認觸發測試
        cmd_trigger()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "install":
        cmd_install()
    elif cmd == "trigger":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "下一步要做什麼"
        cmd_trigger(message)
    elif cmd == "watch":
        cmd_watch()
    else:
        print(f"未知命令: {cmd}")
        print("可用: install, trigger, watch")

if __name__ == "__main__":
    main()
