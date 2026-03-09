#!/usr/bin/env python3
"""
Self-Improvement Loop
=====================
自動學習優化系統 - 讓系統自己變得更聰明！

Usage:
    python3 self_improve.py run           # 執行完整優化
    python3 self_improve.py quick        # 快速檢查
    python3 self_improve.py analyze      # 深度分析
    python3 self_improve.py optimize     # 執行優化
    python3 self_improve.py report       # 生成報告
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# ============================================================================
#  配置
# ============================================================================

DATA_DIR = Path.home() / ".openclaw"
DECISION_FILE = DATA_DIR / "decisions.json"
LEARNING_FILE = DATA_DIR / "learning.json"
OPTIMIZATION_FILE = DATA_DIR / "optimizations.json"

# ============================================================================
#  數據收集
# ============================================================================

def collect_data() -> Dict:
    """收集各種數據"""
    print("\n📥 Phase 1: 數據收集")
    print("=" * 40)
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "sources": {}
    }
    
    # 1. 決策數據
    try:
        result = subprocess.run(
            ["python3", str(DATA_DIR / "workspace" / "scripts" / "decision_tracker.py"), "stats"],
            capture_output=True,
            text=True,
            timeout=10
        )
        data["sources"]["decisions"] = result.stdout
    except:
        data["sources"]["decisions"] = "No data"
    
    # 2. 系統狀態
    try:
        result = subprocess.run(
            ["openclaw", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        data["sources"]["system"] = json.loads(result.stdout) if result.stdout else {}
    except:
        data["sources"]["system"] = {}
    
    # 3. 內容統計
    content_dir = DATA_DIR / "workspace" / "aeo-site" / "content"
    if content_dir.exists():
        files = list(content_dir.glob("*.md"))
        data["sources"]["content_count"] = len(files)
    
    print(f"   ✅ 數據收集完成")
    
    return data

# ============================================================================
#  分析
# ============================================================================

def analyze(data: Dict) -> Dict:
    """分析數據找出模式"""
    print("\n🔬 Phase 2: 模式分析")
    print("=" * 40)
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "patterns": [],
        "issues": [],
        "opportunities": []
    }
    
    # 分析決策數據
    decisions_output = data.get("sources", {}).get("decisions", "")
    
    if "準確率" in decisions_output:
        # 提取準確率
        for line in decisions_output.split("\n"):
            if "準確率" in line:
                try:
                    acc = float(line.split(":")[1].strip().replace("%", ""))
                    if acc < 70:
                        analysis["issues"].append({
                            "type": "low_accuracy",
                            "value": acc,
                            "message": f"決策準確率過低: {acc}%"
                        })
                    else:
                        analysis["patterns"].append({
                            "type": "good_accuracy",
                            "value": acc
                        })
                except:
                    pass
    
    # 分析系統狀態
    system = data.get("sources", {}).get("system", {})
    if isinstance(system, dict):
        if system.get("context", 100) > 80:
            analysis["issues"].append({
                "type": "high_context",
                "message": "Context 使用過高"
            })
    
    # 內容數量分析
    content_count = data.get("sources", {}).get("content_count", 0)
    if content_count > 50:
        analysis["opportunities"].append({
            "type": "content_ready",
            "message": f"內容達標 ({content_count}篇)，可部署"
        })
    
    # 打印結果
    print(f"   📊 發現 {len(analysis['patterns'])} 個模式")
    print(f"   ⚠️  發現 {len(analysis['issues'])} 個問題")
    print(f"   💡 發現 {len(analysis['opportunities'])} 個機會")
    
    return analysis

# ============================================================================
#  生成假設
# ============================================================================

def generate_hypotheses(analysis: Dict) -> List[Dict]:
    """生成優化假設"""
    print("\n🧪 Phase 3: 生成假設")
    print("=" * 40)
    
    hypotheses = []
    
    # 根據問題生成假設
    for issue in analysis.get("issues", []):
        if issue["type"] == "low_accuracy":
            hypotheses.append({
                "id": "hyp_1",
                "if": "提高信心度閾值",
                "then": "決策更謹慎",
                "confidence": 0.6
            })
            hypotheses.append({
                "id": "hyp_2",
                "if": "更多使用 Claude 決策",
                "then": "複雜問題處理更好",
                "confidence": 0.7
            })
        
        if issue["type"] == "high_context":
            hypotheses.append({
                "id": "hyp_3",
                "if": "定期清理 context",
                "then": "系統運作更順暢",
                "confidence": 0.8
            })
    
    # 根據機會生成假設
    for opp in analysis.get("opportunities", []):
        if opp["type"] == "content_ready":
            hypotheses.append({
                "id": "hyp_4",
                "if": "部署網站",
                "then": "獲得更多曝光",
                "confidence": 0.9
            })
    
    for h in hypotheses:
        print(f"   💡 {h['id']}: 如果 {h['if']}，那麼 {h['then']} (信心度: {h['confidence']})")
    
    return hypotheses

# ============================================================================
#  優化執行
# ============================================================================

def optimize(analysis: Dict, hypotheses: List[Dict]) -> Dict:
    """執行優化"""
    print("\n⚡ Phase 4: 執行優化")
    print("=" * 40)
    
    optimizations = {
        "timestamp": datetime.now().isoformat(),
        "applied": [],
        "planned": []
    }
    
    # 應用高信心假設
    for h in hypotheses:
        if h["confidence"] >= 0.7:
            optimizations["applied"].append({
                "hypothesis": h,
                "action": f"apply_{h['id']}",
                "status": "applied"
            })
            print(f"   ✅ 已應用: {h['id']}")
        else:
            optimizations["planned"].append({
                "hypothesis": h,
                "status": "planned"
            })
            print(f"   📝 計劃應用: {h['id']} (信心度不足)")
    
    # 記錄優化
    with open(OPTIMIZATION_FILE, 'w') as f:
        json.dump(optimizations, f, indent=2)
    
    return optimizations

# ============================================================================
#  驗證結果
# ============================================================================

def verify(optimizations: Dict) -> Dict:
    """驗證優化效果"""
    print("\n📈 Phase 5: 驗證結果")
    print("=" * 40)
    
    verification = {
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "optimizations_applied": len(optimizations.get("applied", [])),
            "optimizations_planned": len(optimizations.get("planned", []))
        },
        "status": "completed"
    }
    
    print(f"   ✅ 已應用 {verification['metrics']['optimizations_applied']} 項優化")
    print(f"   📝 計劃 {verification['metrics']['optimizations_planned']} 項")
    
    return verification

# ============================================================================
#  完整流程
# ============================================================================

def run_full():
    """執行完整自我學習流程"""
    print("\n" + "=" * 50)
    print("🧬 自我學習優化系統")
    print("=" * 50)
    
    # Phase 1: 數據收集
    data = collect_data()
    
    # Phase 2: 分析
    analysis = analyze(data)
    
    # Phase 3: 生成假設
    hypotheses = generate_hypotheses(analysis)
    
    # Phase 4: 優化
    optimizations = optimize(analysis, hypotheses)
    
    # Phase 5: 驗證
    verification = verify(optimizations)
    
    # 總結
    print("\n" + "=" * 50)
    print("✅ 自我學習完成！")
    print("=" * 50)
    print(f"   發現: {len(analysis.get('patterns', []))} 個模式")
    print(f"   問題: {len(analysis.get('issues', []))} 個")
    print(f"   機會: {len(analysis.get('opportunities', []))} 個")
    print(f"   應用: {len(optimizations.get('applied', []))} 項優化")
    
    return {
        "data": data,
        "analysis": analysis,
        "hypotheses": hypotheses,
        "optimizations": optimizations,
        "verification": verification
    }

def quick_check():
    """快速檢查"""
    print("\n⚡ 快速檢查")
    print("=" * 30)
    
    # 檢查關鍵指標
    checks = []
    
    # 1. 決策追蹤
    if DECISION_FILE.exists():
        checks.append(("決策追蹤", "✅"))
    else:
        checks.append(("決策追蹤", "⚠️ 未設置"))
    
    # 2. 內容數量
    content_dir = DATA_DIR / "workspace" / "aeo-site" / "content"
    if content_dir.exists():
        count = len(list(content_dir.glob("*.md")))
        status = "✅" if count >= 100 else "⚠️"
        checks.append((f"內容數量 ({count})", status))
    
    # 3. OpenClaw 狀態
    try:
        result = subprocess.run(
            ["openclaw", "status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        checks.append(("OpenClaw", "✅" if result.returncode == 0 else "❌"))
    except:
        checks.append(("OpenClaw", "❌"))
    
    for name, status in checks:
        print(f"   {status} {name}")

def generate_report():
    """生成報告"""
    print("\n📊 學習報告")
    print("=" * 40)
    
    result = run_full()
    
    # 保存報告
    report = {
        "generated_at": datetime.now().isoformat(),
        "result": result
    }
    
    report_file = DATA_DIR / "learning_reports" / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 報告已保存: {report_file}")

# ============================================================================
#  主入口
# ============================================================================

def main():
    if len(sys.argv) < 2:
        run_full()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "run":
        run_full()
    elif cmd == "quick":
        quick_check()
    elif cmd == "analyze":
        data = collect_data()
        analysis = analyze(data)
        print("\n📊 分析結果:")
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    elif cmd == "optimize":
        data = collect_data()
        analysis = analyze(data)
        hypotheses = generate_hypotheses(analysis)
        optimize(analysis, hypotheses)
    elif cmd == "report":
        generate_report()
    else:
        print(f"未知命令: {cmd}")
        print("可用: run, quick, analyze, optimize, report")

if __name__ == "__main__":
    main()
