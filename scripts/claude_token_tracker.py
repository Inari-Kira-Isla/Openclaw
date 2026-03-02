#!/usr/bin/env python3
"""
Claude Token Tracker
====================
追蹤 Claude CLI 的 token 使用量

Usage:
    python claude_token_tracker.py "你的任務"
    
Output:
    - 即時顯示 token 使用量
    - 記錄到 ~/.claude_token_history.json
    - 每日/每週統計
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

HISTORY_FILE = Path.home() / ".claude_token_history.json"

# ============================================================================
#  Token 計算 (基於字符估算)
# ============================================================================

def estimate_tokens(text: str) -> int:
    """估算 token 數量 (約 4 字元 = 1 token)"""
    if not text:
        return 0
    return len(text) // 4

def calculate_cost(input_tokens: int, output_tokens: int, model: str = "claude-sonnet-4-20250514") -> Dict:
    """計算成本 (USD)"""
    # Claude Sonnet 定價
    pricing = {
        "claude-sonnet-4-20250514": {
            "input": 0.000003,   # $3/million
            "output": 0.000015   # $15/million
        },
        "claude-opus-4-5-20250514": {
            "input": 0.000015,   # $15/million
            "output": 0.000075   # $75/million
        },
        "claude-3-5-sonnet": {
            "input": 0.000003,
            "output": 0.000015
        }
    }
    
    p = pricing.get(model, pricing["claude-sonnet-4-20250514"])
    cost = (input_tokens * p["input"]) + (output_tokens * p["output"])
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost_usd": round(cost, 6)
    }

# ============================================================================
#  歷史記錄
# ============================================================================

def load_history() -> List[Dict]:
    """載入歷史記錄"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []

def save_history(history: List[Dict]):
    """保存歷史記錄"""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def add_record(task: str, result: str, duration: float):
    """新增記錄"""
    input_tokens = estimate_tokens(task)
    output_tokens = estimate_tokens(result)
    
    record = {
        "timestamp": datetime.now().isoformat(),
        "task": task[:100],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "duration_seconds": round(duration, 2),
        "cost": calculate_cost(input_tokens, output_tokens)
    }
    
    history = load_history()
    history.append(record)
    save_history(history)
    
    return record

# ============================================================================
#  統計分析
# ============================================================================

def get_stats(days: int = 7) -> Dict:
    """取得統計"""
    history = load_history()
    
    # 過濾最近 N 天
    cutoff = datetime.now() - timedelta(days=days)
    recent = [
        r for r in history 
        if datetime.fromisoformat(r["timestamp"]) > cutoff
    ]
    
    if not recent:
        return {"days": days, "total_tasks": 0, "total_tokens": 0, "total_cost": 0}
    
    total_tokens = sum(r["total_tokens"] for r in recent)
    total_cost = sum(r["cost"]["cost_usd"] for r in recent)
    
    return {
        "days": days,
        "total_tasks": len(recent),
        "total_tokens": total_tokens,
        "total_cost_usd": round(total_cost, 4),
        "avg_tokens_per_task": total_tokens // len(recent),
        "avg_duration_seconds": sum(r["duration_seconds"] for r in recent) / len(recent)
    }

def print_stats(days: int = 7):
    """顯示統計"""
    stats = get_stats(days)
    
    print(f"\n📊 Claude Token 統計 (過去 {stats['days']} 天)")
    print("=" * 40)
    print(f"   任務數:     {stats['total_tasks']}")
    print(f"   Token總量:  {stats['total_tokens']:,}")
    print(f"   總成本:     ${stats['total_cost_usd']:.4f}")
    print(f"   平均/任務:  {stats['avg_tokens_per_task']:,} tokens")
    print(f"   平均耗時:   {stats['avg_duration_seconds']:.1f}s")

# ============================================================================
#  執行追蹤
# ============================================================================

def run_with_tracking(task: str, workdir: str = None) -> Dict:
    """執行 Claude CLI 並追蹤"""
    print(f"\n🎯 任務: {task[:50]}...")
    
    # 創建臨時目錄
    if not workdir:
        workdir = subprocess.run(
            ["mktemp", "-d"], capture_output=True, text=True
        ).stdout.strip()
        subprocess.run(["git", "init"], cwd=workdir, capture_output=True)
    
    start_time = time.time()
    
    # 執行 Claude
    cmd = ["claude", "-p", task]
    result = subprocess.run(
        cmd,
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    duration = time.time() - start_time
    
    # 記錄
    record = add_record(task, result.stdout, duration)
    
    # 顯示結果
    cost = record["cost"]
    print(f"\n✅ 完成 ({duration:.1f}s)")
    print(f"   📥 Input:  {cost['input_tokens']:,} tokens")
    print(f"   📤 Output: {cost['output_tokens']:,} tokens")
    print(f"   💰 Cost:   ${cost['cost_usd']:.4f}")
    
    return record

# ============================================================================
#  主流程
# ============================================================================

def main():
    if len(sys.argv) < 2:
        # 顯示統計
        print_stats(7)
        print("\n使用方法:")
        print("  python claude_token_tracker.py \"你的任務\"")
        print("  python claude_token_tracker.py --stats 30")
        return
    
    if sys.argv[1] == "--stats":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print_stats(days)
        return
    
    task = " ".join(sys.argv[1:])
    run_with_tracking(task)

if __name__ == "__main__":
    main()
