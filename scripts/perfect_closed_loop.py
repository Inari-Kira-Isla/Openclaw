#!/usr/bin/env python3
"""
Perfect Closed-Loop System
==========================
OpenClaw 編排層：前期整理 → Claude CLI 執行 → 閉環回報

Usage:
    python perfect_closed_loop.py "研究最新 AI Agents 趨勢"
"""

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from enum import Enum
from typing import Optional

# ============================================================================
#  Phase 1: OpenClaw 前期準備
# ============================================================================

class TaskType(Enum):
    """任務類型分類"""
    SIMPLE_QUERY = "simple"      # 簡單查詢，OpenClaw 直接處理
    COMPLEX_ANALYSIS = "complex" # 複雜分析，需要 Claude 推理
    TECHNICAL_IMPLEMENT = "tech" # 技術實現，需要代碼生成
    DECISION_NEEDED = "decision" # 需要人類/Claude 決策

def analyze_task(task: str) -> TaskType:
    """分析任務類型"""
    task_lower = task.lower()
    
    # 複雜任務關鍵詞
    complex_keywords = ["研究", "分析", "比較", "評估", "趨勢", "策略"]
    tech_keywords = ["開發", "重構", "修復", "優化", "建立", "實現", "代碼"]
    decision_keywords = ["應該", "選哪個", "推薦", "建議"]
    
    if any(k in task_lower for k in decision_keywords):
        return TaskType.DECISION_NEEDED
    elif any(k in task_lower for k in tech_keywords):
        return TaskType.TECHNICAL_IMPLEMENT
    elif any(k in task_lower for k in complex_keywords):
        return TaskType.COMPLEX_ANALYSIS
    else:
        return TaskType.SIMPLE_QUERY

def gather_context(task: str) -> dict:
    """蒐集相關上下文"""
    print(f"\n📋 Phase 1: 前期準備 - 蒐集上下文")
    print(f"   任務: {task}")
    
    context = {
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "memory_results": [],
        "web_results": []
    }
    
    # 這裡調用 OpenClaw 的 memory_search
    # 實際實現需要通過 OpenClaw API
    print(f"   🔍 搜尋 Memory...")
    print(f"   🌐 搜尋 Web...")
    
    return context

def build_prompt(task: str, context: dict) -> str:
    """Prompt 工廠：組裝上下文"""
    print(f"\n🏭 Phase 1.5: 組裝 Prompt")
    
    prompt = f"""## 任務
{task}

## 上下文
{json.dumps(context.get('memory_results', []), indent=2, ensure_ascii=False)}

## 輸出要求
- 結構化回覆
- 重點摘要
- 可執行的建議（如果適用）
"""
    return prompt

# ============================================================================
#  Phase 2: Claude CLI 執行
# ============================================================================

def execute_with_claude(prompt: str, workdir: str = None) -> dict:
    """通過 Claude CLI 執行任務"""
    print(f"\n⚡ Phase 2: Claude CLI 執行")
    
    # 創建臨時目錄
    if not workdir:
        workdir = tempfile.mkdtemp()
        subprocess.run(["git", "init"], cwd=workdir, capture_output=True)
    
    print(f"   📁 工作目錄: {workdir}")
    print(f"   🤖 調用 Claude Max...")
    
    # 調用 Claude CLI
    cmd = ["claude", "-p", prompt]
    result = subprocess.run(
        cmd,
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr,
        "workdir": workdir
    }

# ============================================================================
#  Phase 3: 閉環回報
# ============================================================================

class LoopStatus(Enum):
    """閉環狀態"""
    COMPLETE = "complete"
    NEEDS_RETRY = "retry"
    NEEDS_HUMAN_DECISION = "human_decision"

def close_loop(task: str, result: dict, context: dict) -> LoopStatus:
    """閉環處理"""
    print(f"\n🔄 Phase 3: 閉環處理")
    
    if result["success"]:
        print(f"   ✅ 任務完成")
        print(f"   📝 結果: {result['output'][:200]}...")
        
        # 記錄到 Memory
        record_to_memory(task, result, context)
        
        # Telegram 回報（實際需要調用 OpenClaw message API）
        notify_telegram(task, result)
        
        return LoopStatus.COMPLETE
    else:
        print(f"   ❌ 任務失敗: {result.get('error', 'Unknown')}")
        return LoopStatus.NEEDS_RETRY

def record_to_memory(task: str, result: dict, context: dict):
    """記錄到記憶系統"""
    print(f"   💾 記錄到 Memory...")
    # 實際實現需要通過 OpenClaw memory API
    
    entry = f"""# 任務記錄 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 任務
{task}

## 結果
{result.get('output', '')[:500]}

## 狀態
{"✅ 完成" if result['success'] else "❌ 失敗"}
"""
    print(f"   📄 Memory Entry:\n{entry}")

def notify_telegram(task: str, result: dict):
    """Telegram 通知"""
    print(f"   📱 Telegram 通知...")
    # 實際實現需要調用 OpenClaw message API
    message = f"""✅ 任務完成

📋 任務: {task}
📝 結果: {result.get('output', '')[:300]}...
"""
    print(f"   📨 訊息: {message}")

# ============================================================================
#  主流程
# ============================================================================

def run_closed_loop(task: str) -> dict:
    """執行完整閉環流程"""
    
    print("=" * 60)
    print("🎯 Perfect Closed-Loop System")
    print("=" * 60)
    
    # Phase 1: 前期準備
    task_type = analyze_task(task)
    print(f"\n📊 任務類型: {task_type.value}")
    
    if task_type == TaskType.SIMPLE_QUERY:
        print(f"   → OpenClaw 直接處理")
        return {"type": "simple", "task": task}
    
    context = gather_context(task)
    prompt = build_prompt(task, context)
    
    # Phase 2: Claude CLI 執行
    result = execute_with_claude(prompt)
    
    # Phase 3: 閉環
    status = close_loop(task, result, context)
    
    return {
        "type": task_type.value,
        "status": status.value,
        "result": result
    }

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "測試任務"
    run_closed_loop(task)
