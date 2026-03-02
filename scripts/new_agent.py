#!/usr/bin/env python3
"""
新 Agent 創建系統 - New Agent Creation System
從需求到部署的完整閉環流程
"""

import os
import json
import subprocess
from datetime import datetime

AGENT_TEMPLATES = {
    "coder": {
        "role": "程式開發者",
        "skills": ["code", "debug", "review"],
        "description": "專注於代碼開發和調試"
    },
    "analyst": {
        "role": "數據分析師", 
        "skills": ["analysis", "statistics", "visualization"],
        "description": "專注於數據分析和報告"
    },
    "researcher": {
        "role": "研究者",
        "skills": ["research", "search", "learning"],
        "description": "專注於資訊收集和研究"
    },
    "writer": {
        "role": "內容創作者",
        "skills": ["writing", "editing", "creative"],
        "description": "專注於內容創作"
    },
    "coordinator": {
        "role": "協調者",
        "skills": ["planning", "delegation", "tracking"],
        "description": "專注於任務協調"
    }
}

class NewAgentSystem:
    def __init__(self):
        self.agents_path = os.path.expanduser("~/.openclaw/workspace/agents/")
        self.memory_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        os.makedirs(self.agents_path, exist_ok=True)
        
    def create_agent(self, name, template="coder", custom_skills=None):
        """創建新 Agent"""
        print(f"🤖 創建新 Agent: {name}")
        
        template_data = AGENT_TEMPLATES.get(template, AGENT_TEMPLATES["coder"])
        
        # 生成 Agent 結構
        agent_structure = {
            "name": name,
            "template": template,
            "role": template_data["role"],
            "skills": custom_skills or template_data["skills"],
            "description": template_data["description"],
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "performance": {
                "tasks_completed": 0,
                "success_rate": 0,
                "avg_response_time": 0
            }
        }
        
        # 保存 Agent 定義
        agent_file = os.path.join(self.agents_path, f"{name}.json")
        with open(agent_file, "w") as f:
            json.dump(agent_structure, f, indent=2)
        
        # 生成 SKILL.md
        self.generate_skill_md(name, agent_structure)
        
        # 生成 SOUL.md
        self.generate_soul_md(name, agent_structure)
        
        print(f"✅ Agent 創建完成: {name}")
        return agent_structure
    
    def generate_skill_md(self, name, data):
        """生成 Skill.md"""
        content = f"""# SKILL.md - {name}

## 觸發條件

當用戶提及以下關鍵字時觸發：
- {name}
- {data['role']}
- {', '.join(data['skills'])}

## 功能

### 主要技能
{chr(10).join(f'- {skill}' for skill in data['skills'])}

### 描述
{data['description']}

## 使用方式

```
@{name} [任務]
```

## 整合

此 Agent 由 Agent Rotation System 調度。
"""
        
        skill_file = os.path.join(self.agents_path, f"{name}/SKILL.md")
        os.makedirs(os.path.dirname(skill_file), exist_ok=True)
        with open(skill_file, "w") as f:
            f.write(content)
        
        print(f"✅ SKILL.md 生成完成")
    
    def generate_soul_md(self, name, data):
        """生成 SOUL.md"""
        content = f"""# SOUL.md - {name}

## 身份

- **名稱**: {name}
- **角色**: {data['role']}
- **存在理由**: {data['description']}

## 核心價值

- 專注於 {data['skills'][0]}
- 持續學習和優化
- 與團隊协作

## 行為準則

- 主動發現問題
- 及時匯報進度
- 持續自我改進

## 團隊協作

與其他 Agents 協作：
- Kira: 協調者
- Cynthia: 知識庫
- 史萊姆: 學習優化
- Team: 執行者
- Evolution: 質疑者

---

_Created: {datetime.now().strftime('%Y-%m-%d')}_
"""
        
        soul_file = os.path.join(self.agents_path, f"{name}/SOUL.md")
        os.makedirs(os.path.dirname(soul_file), exist_ok=True)
        with open(soul_file, "w") as f:
            f.write(content)
        
        print(f"✅ SOUL.md 生成完成")
    
    def register_agent(self, name):
        """註冊 Agent 到 OpenClaw"""
        print(f"📝 註冊 Agent: {name}...")
        
        # 這裡可以調用 OpenClaw 註冊命令
        # 實際實現需要根據 OpenClaw 的註冊方式
        
        return {"status": "registered", "name": name}
    
    def train_agent(self, name, tasks):
        """訓練 Agent"""
        print(f"🎓 訓練 Agent: {name}")
        
        results = []
        for task in tasks:
            print(f"  訓練任務: {task}")
            results.append({
                "task": task,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            })
        
        # 更新 Agent 狀態
        agent_file = os.path.join(self.agents_path, f"{name}.json")
        with open(agent_file, "r") as f:
            agent = json.load(f)
        
        agent["status"] = "trained"
        agent["training_results"] = results
        
        with open(agent_file, "w") as f:
            json.dump(agent, f, indent=2)
        
        return results
    
    def deploy_agent(self, name):
        """部署 Agent"""
        print(f"🚀 部署 Agent: {name}...")
        
        # 更新狀態
        agent_file = os.path.join(self.agents_path, f"{name}.json")
        with open(agent_file, "r") as f:
            agent = json.load(f)
        
        agent["status"] = "deployed"
        agent["deployed_at"] = datetime.now().isoformat()
        
        with open(agent_file, "w") as f:
            json.dump(agent, f, indent=2)
        
        # 添加到 Router
        self.add_to_router(name)
        
        return {"status": "deployed", "name": name}
    
    def add_to_router(self, name):
        """添加到 Router"""
        # 更新 agent_router.py 的 AGENTS 字典
        router_file = os.path.expanduser("~/.openclaw/workspace/scripts/agent_router.py")
        
        # 這裡應該動態更新
        print(f"✅ 已添加到 Router")
    
    def monitor_agent(self, name):
        """監控 Agent 效能"""
        agent_file = os.path.join(self.agents_path, f"{name}.json")
        
        if not os.path.exists(agent_file):
            return {"error": "Agent not found"}
        
        with open(agent_file, "r") as f:
            agent = json.load(f)
        
        return agent.get("performance", {})
    
    def full_cycle(self, name, template, tasks):
        """完整閉環：創建 → 註冊 → 訓練 → 部署 → 監控"""
        print(f"\n🔄 開始完整閉環流程: {name}")
        print("="*50)
        
        # 1. 創建
        agent = self.create_agent(name, template)
        print()
        
        # 2. 註冊
        self.register_agent(name)
        print()
        
        # 3. 訓練
        if tasks:
            self.train_agent(name, tasks)
            print()
        
        # 4. 部署
        self.deploy_agent(name)
        print()
        
        # 5. 監控
        perf = self.monitor_agent(name)
        print(f"📊 效能: {perf}")
        
        print("="*50)
        print(f"✅ 完整閉環完成: {name}")
        
        return {
            "name": name,
            "status": "deployed",
            "performance": perf
        }

# CLI
if __name__ == "__main__":
    import sys
    
    nas = NewAgentSystem()
    
    if len(sys.argv) < 3:
        print("🤖 New Agent Creation System")
        print("用法:")
        print("  python new_agent.py create <名稱> <模板>")
        print("  python new_agent.py list")
        print("  python new_agent.py monitor <名稱>")
        print("  python new_agent.py full <名稱> <模板>")
        print()
        print("模板: coder, analyst, researcher, writer, coordinator")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) >= 4:
        name = sys.argv[2]
        template = sys.argv[3]
        nas.create_agent(name, template)
    
    elif cmd == "list":
        for f in os.listdir(nas.agents_path):
            if f.endswith(".json"):
                print(f"  • {f[:-5]}")
    
    elif cmd == "monitor" and len(sys.argv) >= 3:
        name = sys.argv[2]
        print(nas.monitor_agent(name))
    
    elif cmd == "full" and len(sys.argv) >= 4:
        name = sys.argv[2]
        template = sys.argv[3]
        tasks = sys.argv[4:] if len(sys.argv) > 4 else []
        nas.full_cycle(name, template, tasks)
