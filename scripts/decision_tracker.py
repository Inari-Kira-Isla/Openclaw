#!/usr/bin/env python3
"""
Decision Tracker & Optimizer
===========================
決策追蹤、統計分析、信心度校準

Usage:
    python3 decision_tracker.py record --context "部署網站" --decision "preview" --confidence 0.8
    python3 decision_tracker.py result --id <uuid> --result success
    python3 decision_tracker.py stats
    python3 decision_tracker.py optimize
"""

import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DATA_FILE = Path.home() / ".openclaw_decisions.json"

# ============================================================================
#  數據管理
# ============================================================================

def load_data() -> dict:
    """載入數據"""
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {
        "decisions": [],
        "statistics": {
            "total": 0,
            "success": 0,
            "by_type": {},
            "confidence_ranges": {}
        }
    }

def save_data(data: dict):
    """保存數據"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================================
#  記錄決策
# ============================================================================

def record_decision(context: str, decision: str, confidence: float, claude_used: bool = False) -> str:
    """記錄新決策"""
    data = load_data()
    
    decision_id = str(uuid.uuid4())[:8]
    
    record = {
        "id": decision_id,
        "timestamp": datetime.now().isoformat(),
        "context": context,
        "decision": decision,
        "confidence": confidence,
        "claude_used": claude_used,
        "result": None,
        "duration_ms": None
    }
    
    data["decisions"].append(record)
    data["statistics"]["total"] += 1
    
    save_data(data)
    
    print(f"✅ 記錄決策: {decision_id}")
    print(f"   上下文: {context}")
    print(f"   決定: {decision}")
    print(f"   信心度: {confidence}")
    
    return decision_id

def record_result(decision_id: str, result: str, duration_ms: int = None):
    """記錄執行結果"""
    data = load_data()
    
    for d in data["decisions"]:
        if d["id"] == decision_id:
            d["result"] = result
            d["duration_ms"] = duration_ms
            
            # 更新統計
            if result == "success":
                data["statistics"]["success"] += 1
            
            # 按類型統計
            type_key = "claude" if d.get("claude_used") else "autonomous"
            if type_key not in data["statistics"]["by_type"]:
                data["statistics"]["by_type"][type_key] = {"total": 0, "success": 0}
            data["statistics"]["by_type"][type_key]["total"] += 1
            if result == "success":
                data["statistics"]["by_type"][type_key]["success"] += 1
            
            # 信心度範圍統計
            conf = d["confidence"]
            if conf >= 0.8:
                range_key = "high"
            elif conf >= 0.5:
                range_key = "medium"
            else:
                range_key = "low"
            
            if range_key not in data["statistics"]["confidence_ranges"]:
                data["statistics"]["confidence_ranges"][range_key] = {"total": 0, "success": 0}
            data["statistics"]["confidence_ranges"][range_key]["total"] += 1
            if result == "success":
                data["statistics"]["confidence_ranges"][range_key]["success"] += 1
            
            break
    
    save_data(data)
    print(f"✅ 記錄結果: {decision_id} → {result}")

# ============================================================================
#  統計分析
# ============================================================================

def get_statistics() -> dict:
    """獲取統計"""
    data = load_data()
    stats = data["statistics"]
    
    # 計算準確率
    accuracy = stats["success"] / stats["total"] if stats["total"] > 0 else 0
    
    # 信心度校準
    confidence_calibration = 0
    if stats["confidence_ranges"]:
        calibrations = []
        for range_key, counts in stats["confidence_ranges"].items():
            range_acc = counts["success"] / counts["total"] if counts["total"] > 0 else 0
            
            # 預期信心度
            expected = {"high": 0.85, "medium": 0.65, "low": 0.45}[range_key]
            calibrations.append(abs(range_acc - expected))
        
        confidence_calibration = 1 - (sum(calibrations) / len(calibrations))
    
    # Claude vs 自主
    claude_stats = stats["by_type"].get("claude", {"total": 0, "success": 0})
    auto_stats = stats["by_type"].get("autonomous", {"total": 0, "success": 0})
    
    claude_acc = claude_stats["success"] / claude_stats["total"] if claude_stats["total"] > 0 else 0
    auto_acc = auto_stats["success"] / auto_stats["total"] if auto_stats["total"] > 0 else 0
    
    return {
        "total": stats["total"],
        "success": stats["success"],
        "accuracy": round(accuracy, 3),
        "confidence_calibration": round(confidence_calibration, 3),
        "by_type": {
            "claude": {"total": claude_stats["total"], "accuracy": round(claude_acc, 3)},
            "autonomous": {"total": auto_stats["total"], "accuracy": round(auto_acc, 3)}
        },
        "confidence_ranges": stats["confidence_ranges"]
    }

def print_statistics():
    """打印統計"""
    stats = get_statistics()
    
    print(f"\n📊 決策統計")
    print("=" * 40)
    print(f"   總決策數:    {stats['total']}")
    print(f"   成功次數:    {stats['success']}")
    print(f"   準確率:      {stats['accuracy']:.1%}")
    print(f"   信心度校準:  {stats['confidence_calibration']:.1%}")
    
    print(f"\n📈 按類型")
    print(f"   Claude 決策:  {stats['by_type']['claude']['total']} 次, 準確率 {stats['by_type']['claude']['accuracy']:.1%}")
    print(f"   自主決策:    {stats['by_type']['autonomous']['total']} 次, 準確率 {stats['by_type']['autonomous']['accuracy']:.1%}")
    
    print(f"\n🎯 信心度分佈")
    for range_key, counts in stats["confidence_ranges"].items():
        acc = counts["success"] / counts["total"] if counts["total"] > 0 else 0
        label = {"high": "高(0.8+)", "medium": "中(0.5-0.8)", "low": "低(<0.5)"}[range_key]
        print(f"   {label}: {counts['total']} 次, 準確率 {acc:.1%}")

# ============================================================================
#  優化建議
# ============================================================================

def get_optimizations() -> list:
    """獲取優化建議"""
    stats = get_statistics()
    suggestions = []
    
    # 信心度校準
    if stats["confidence_calibration"] < 0.7:
        suggestions.append("⚠️ 信心度校準不足，可能過度自信或過於保守")
    
    # 決策類型效果
    claude_acc = stats["by_type"]["claude"]["accuracy"]
    auto_acc = stats["by_type"]["autonomous"]["accuracy"]
    
    if stats["by_type"]["claude"]["total"] > 5:
        if claude_acc > auto_acc + 0.15:
            suggestions.append("📈 Claude 決策效果顯著優於自主決策，建議複雜決策使用 Claude")
        elif auto_acc > claude_acc + 0.15:
            suggestions.append("📈 自主決策效果更好，可考慮降低 Claude 使用門檻")
    
    # 高信心度決策
    high_range = stats["confidence_ranges"].get("high", {"total": 0, "success": 0})
    if high_range["total"] > 0:
        high_acc = high_range["success"] / high_range["total"]
        if high_acc < 0.6:
            suggestions.append("⚠️ 高信心度決策準確率過低，需要重新校準")
    
    if not suggestions:
        suggestions.append("✅ 系統運行良好，無需特別優化")
    
    return suggestions

def print_optimizations():
    """打印優化建議"""
    suggestions = get_optimizations()
    
    print(f"\n🎯 優化建議")
    print("=" * 40)
    for s in suggestions:
        print(f"   {s}")

# ============================================================================
#  信心度校準
# ============================================================================

def calibrate():
    """執行信心度校準"""
    stats = get_statistics()
    
    # 計算校準因子
    calibration_factor = stats["confidence_calibration"]
    
    print(f"\n🔧 信心度校準")
    print("=" * 40)
    print(f"   當前校準度: {calibration_factor:.1%}")
    
    if calibration_factor >= 0.8:
        print(f"   狀態: ✅ 良好，無需調整")
    elif calibration_factor >= 0.6:
        print(f"   狀態: ⚠️ 一般，建議觀察")
    else:
        print(f"   狀態: ❌ 需要校準")
        print(f"   動作: 調整信心度權重")
    
    return calibration_factor

# ============================================================================
#  主入口
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Decision Tracker & Optimizer")
    subparsers = parser.add_subparsers()
    
    # record
    rec_parser = subparsers.add_parser("record", help="記錄決策")
    rec_parser.add_argument("--context", required=True, help="上下文")
    rec_parser.add_argument("--decision", required=True, help="決定")
    rec_parser.add_argument("--confidence", type=float, required=True, help="信心度")
    rec_parser.add_argument("--claude", action="store_true", help="是否使用 Claude")
    rec_parser.set_defaults(func=lambda args: record_decision(
        args.context, args.decision, args.confidence, args.claude
    ))
    
    # result
    res_parser = subparsers.add_parser("result", help="記錄結果")
    res_parser.add_argument("--id", required=True, help="決策 ID")
    res_parser.add_argument("--result", required=True, choices=["success", "failure"], help="結果")
    res_parser.add_argument("--duration", type=int, help="耗時(毫秒)")
    res_parser.set_defaults(func=lambda args: record_result(args.id, args.result, args.duration))
    
    # stats
    stats_parser = subparsers.add_parser("stats", help="統計分析")
    stats_parser.set_defaults(func=lambda args: print_statistics())
    
    # optimize
    opt_parser = subparsers.add_parser("optimize", help="優化建議")
    opt_parser.set_defaults(func=lambda args: (print_statistics(), print_optimizations()))
    
    # calibrate
    cal_parser = subparsers.add_parser("calibrate", help="信心度校準")
    cal_parser.set_defaults(func=lambda args: calibrate())
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
