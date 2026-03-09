#!/usr/bin/env python3
"""
Auto-Decide System
==================
自動決定下一步行動

Usage:
    python3 auto_decide.py                    # 互動模式
    python3 auto_decide.py --context "網站"    # 指定上下文
    python3 auto_decide.py --auto              # 全自動模式
"""

import json
import os
import random
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
#  決策規則
# ============================================================================

DECISION_RULES = {
    # 網站相關
    "網站": ["預覽網站", "部署上線", "增加內容", "測試功能"],
    "網站完成": ["預覽", "部署", "生成統計"],
    
    # 內容相關
    "內容": ["生成更多", "發布到網站", "分享到社群"],
    "生成完成": ["查看結果", "生成下一個", "發布"],
    
    # 開發相關
    "代碼": ["測試", "提交", "審查", "部署"],
    "功能完成": ["測試", "文檔", "下一個功能"],
    
    # 學習相關
    "學習": ["繼續", "複習", "實踐", "分享"],
    
    # 一般
    "完成": ["下一步", "統計", "匯報"],
}

# ============================================================================
#  評估邏輯
# ============================================================================

def assess_context(context: str = None) -> Dict:
    """評估當前上下文"""
    if not context:
        # 嘗試從環境讀取
        context = os.environ.get("AEO_CONTEXT", "")
    
    return {
        "context": context,
        "timestamp": datetime.now().isoformat(),
        "detected_keywords": detect_keywords(context)
    }

def detect_keywords(text: str) -> List[str]:
    """檢測關鍵詞"""
    keywords = []
    for keyword in DECISION_RULES.keys():
        if keyword in text:
            keywords.append(keyword)
    return keywords

def find_options(context: str) -> List[str]:
    """找到可能的選項"""
    keywords = detect_keywords(context)
    
    options = []
    for keyword in keywords:
        if keyword in DECISION_RULES:
            options.extend(DECISION_RULES[keyword])
    
    # 去重
    options = list(set(options))
    
    # 如果沒有匹配，返回默認選項
    if not options:
        options = ["生成內容", "查看統計", "預覽網站", "下一步"]
    
    return options

# ============================================================================
#  簡單決策
# ============================================================================

def make_simple_decision(context: str) -> Dict:
    """簡單決策 - 基於規則"""
    options = find_options(context)
    
    # 根據關鍵詞權重排序
    weights = {}
    for opt in options:
        weights[opt] = 0
        for kw in detect_keywords(context):
            if kw in opt or opt in kw:
                weights[opt] += 1
    
    # 選擇最高權重
    if weights:
        decision = max(weights, key=weights.get)
    else:
        decision = random.choice(options)
    
    return {
        "type": "simple",
        "decision": decision,
        "options": options,
        "reason": "基於規則匹配"
    }

# ============================================================================
#  複雜決策 - 調用 Claude
# ============================================================================

def make_complex_decision(context: str) -> Dict:
    """複雜決策 - 需要 Claude"""
    options = find_options(context)
    
    prompt = f"""## 上下文
{context}

## 可選行動
{', '.join(options)}

## 任務
評估當前狀況，決定最佳下一步行動。

## 輸出格式
請直接給出建議，不要其他說明。
"""
    
    # 調用 Claude
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        decision = result.stdout.strip().split("\n")[0][:50]
    else:
        decision = random.choice(options)
    
    return {
        "type": "complex",
        "decision": decision,
        "options": options,
        "reason": "Claude 評估",
        "claude_output": result.stdout[:200]
    }

# ============================================================================
#  主決策函數
# ============================================================================

def decide(context: str = None, auto: bool = False) -> Dict:
    """主決策函數"""
    
    # 評估上下文
    state = assess_context(context)
    
    # 判斷複雜度
    is_complex = (
        auto or 
        len(state["detected_keywords"]) > 2 or
        "完成" in context or
        "下一步" in context
    )
    
    if is_complex and context:
        # 複雜決策
        result = make_complex_decision(context)
    else:
        # 簡單決策
        result = make_simple_decision(context)
    
    result["state"] = state
    result["timestamp"] = datetime.now().isoformat()
    
    return result

def print_decision(result: Dict):
    """打印決策結果"""
    print(f"\n🎯 決定: {result['decision']}")
    print(f"   類型: {result['type']}")
    print(f"   理由: {result['reason']}")
    
    if result.get("options"):
        print(f"\n📋 可選:")
        for opt in result["options"]:
            marker = "→" if opt == result["decision"] else " "
            print(f"   {marker} {opt}")

# ============================================================================
#  互動模式
# ============================================================================

def interactive_mode():
    """互動模式"""
    print("\n🎯 Auto-Decide System")
    print("=" * 40)
    print("輸入上下文，我來決定下一步")
    print("輸入 'quit' 退出\n")
    
    while True:
        try:
            context = input("> ").strip()
            
            if context.lower() in ["quit", "q", "exit"]:
                break
            
            if not context:
                continue
            
            result = decide(context)
            print_decision(result)
            
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("\n再見！")

# ============================================================================
#  主入口
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto-Decide System")
    parser.add_argument("--context", "-c", help="上下文描述")
    parser.add_argument("--auto", "-a", action="store_true", help="全自動模式（複雜決策）")
    parser.add_argument("--interactive", "-i", action="store_true", help="互動模式")
    
    args = parser.parse_args()
    
    if args.interactive or (not args.context and not args.auto):
        interactive_mode()
    else:
        result = decide(args.context, args.auto)
        print_decision(result)

if __name__ == "__main__":
    main()
