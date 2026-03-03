#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 系統健康監測 + 自動優化
System Health Monitor with Auto-Fix Hooks
v2.0 — 2026-03-03
"""

import os, json, time, subprocess, sys
from datetime import datetime, timezone
from collections import Counter

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
JOBS_FILE    = os.path.join(OPENCLAW_DIR, "cron", "jobs.json")
METRICS_FILE = os.path.join(OPENCLAW_DIR, "logs", "health_metrics.json")
HOOKS_LOG    = os.path.join(OPENCLAW_DIR, "logs", "hooks_auto_fix.log")

# ─── Thresholds ────────────────────────────────────────────────────────────────
THRESHOLDS = {
    "error_rate_pct":      10,    # error jobs > 10% → alert
    "real_error_count":     5,    # real (non-stale) errors > 5 → auto-fix
    "timeout_risky_pct":   20,    # ≤60s timeout jobs > 20% → fix timeouts
    "agent_overload_pct":  55,    # single agent > 55% of jobs → redistribute hint
    "tmp_files_mb":       100,    # orphaned tmp files > 100MB → auto-clean
    "no_run_minutes":      90,    # if no job ran in 90min → alert stall
}

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(HOOKS_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_jobs():
    with open(JOBS_FILE, encoding="utf-8") as f:
        d = json.load(f)
    return d, d.get("jobs", [])

def save_jobs(d):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

# ─── Checks ────────────────────────────────────────────────────────────────────

def check_errors(jobs):
    """偵測真實 errors（非 stale）"""
    enabled = [j for j in jobs if j.get("enabled", True)]
    errors = [j for j in enabled if j.get("state",{}).get("lastRunStatus") == "error"]
    stale  = [j for j in errors if j.get("updatedAtMs",0) > j.get("state",{}).get("lastRunAtMs",0)]
    real   = [j for j in errors if j.get("updatedAtMs",0) <= j.get("state",{}).get("lastRunAtMs",0)]
    return {
        "total": len(enabled),
        "error_count": len(errors),
        "stale_count": len(stale),
        "real_count": len(real),
        "error_rate_pct": round(len(errors)*100/max(len(enabled),1), 1),
        "real_error_rate_pct": round(len(real)*100/max(len(enabled),1), 1),
        "real_errors": [{"id": j["id"][:8], "name": j.get("name","?"),
                         "agent": j.get("agentId","?"),
                         "err": j.get("state",{}).get("lastError","")[:100]} for j in real],
    }

def check_timeouts(jobs):
    """偵測 timeout 風險"""
    enabled = [j for j in jobs if j.get("enabled", True)]
    risky = [j for j in enabled
             if j.get("payload",{}).get("timeoutSeconds", 60) <= 60
             and "heartbeat" not in j.get("name","").lower()]
    return {
        "risky_count": len(risky),
        "risky_pct": round(len(risky)*100/max(len(enabled),1), 1),
        "sample": [j.get("name","?") for j in risky[:5]],
    }

def check_agent_balance(jobs):
    """偵測 agent 負載不均"""
    enabled = [j for j in jobs if j.get("enabled", True)]
    counts = Counter(j.get("agentId","(none)") for j in enabled)
    total  = len(enabled)
    top_agent, top_count = counts.most_common(1)[0] if counts else ("?", 0)
    return {
        "distribution": dict(counts.most_common(8)),
        "top_agent": top_agent,
        "top_pct": round(top_count*100/max(total,1), 1),
        "no_agent_count": counts.get("(none)", 0) + sum(1 for j in enabled if not j.get("agentId")),
    }

def check_tmp_files():
    """偵測 memory/ 暫存垃圾"""
    mem_dir = os.path.join(OPENCLAW_DIR, "memory")
    tmp_files = [os.path.join(mem_dir, f) for f in os.listdir(mem_dir)
                 if ".tmp-" in f] if os.path.isdir(mem_dir) else []
    total_mb = sum(os.path.getsize(p) for p in tmp_files) / 1024 / 1024
    return {"count": len(tmp_files), "size_mb": round(total_mb, 1), "files": tmp_files}

def check_last_run(jobs):
    """偵測 cron 是否卡住（長時間無任何 job 執行）"""
    enabled = [j for j in jobs if j.get("enabled", True)]
    last_runs = [j.get("state",{}).get("lastRunAtMs", 0) for j in enabled]
    latest_ms = max(last_runs) if last_runs else 0
    if latest_ms == 0:
        return {"last_run_ago_min": 9999, "stalled": True}
    ago_min = (time.time()*1000 - latest_ms) / 60000
    return {"last_run_ago_min": round(ago_min, 1), "stalled": ago_min > THRESHOLDS["no_run_minutes"]}

# ─── Auto-Fix Actions ──────────────────────────────────────────────────────────

def autofix_timeouts(d, jobs):
    """自動把 ≤60s（非 heartbeat）的 jobs 改成 300s"""
    fixed = 0
    for j in d["jobs"]:
        if "heartbeat" in j.get("name","").lower():
            continue
        t = j.get("payload",{}).get("timeoutSeconds", 60)
        if t <= 60:
            j.setdefault("payload", {})["timeoutSeconds"] = 300
            fixed += 1
    if fixed:
        save_jobs(d)
        log(f"[AUTO-FIX] timeout: fixed {fixed} jobs → 300s")
    return fixed

def autofix_tmp_files(tmp_info):
    """自動刪除 memory/ tmp 暫存檔"""
    removed = 0
    for f in tmp_info["files"]:
        try:
            os.remove(f)
            removed += 1
        except Exception as e:
            log(f"[WARN] cannot remove {f}: {e}")
    if removed:
        log(f"[AUTO-FIX] tmp-clean: removed {removed} files ({tmp_info['size_mb']:.1f} MB freed)")
    return removed

def autofix_orphan_agents(d, jobs):
    """把沒有 agentId 的 enabled jobs 指派給 main"""
    fixed = 0
    for j in d["jobs"]:
        if j.get("enabled", True) and not j.get("agentId"):
            j["agentId"] = "main"
            fixed += 1
    if fixed:
        save_jobs(d)
        log(f"[AUTO-FIX] orphan-agent: assigned {fixed} jobs → main")
    return fixed

# ─── Report + Hooks ────────────────────────────────────────────────────────────

def build_report(checks):
    issues = []
    if checks["errors"]["real_count"] >= THRESHOLDS["real_error_count"]:
        issues.append(f"🔴 真實錯誤 {checks['errors']['real_count']} 個（閾值 {THRESHOLDS['real_error_count']}）")
    if checks["errors"]["real_error_rate_pct"] >= THRESHOLDS["error_rate_pct"]:
        issues.append(f"🟡 真實錯誤率 {checks['errors']['real_error_rate_pct']}%（閾值 {THRESHOLDS['error_rate_pct']}%）")
    if checks["timeouts"]["risky_pct"] >= THRESHOLDS["timeout_risky_pct"]:
        issues.append(f"🟡 高風險 timeout {checks['timeouts']['risky_pct']}%（閾值 {THRESHOLDS['timeout_risky_pct']}%）")
    if checks["balance"]["top_pct"] >= THRESHOLDS["agent_overload_pct"]:
        issues.append(f"🟡 {checks['balance']['top_agent']} 負載 {checks['balance']['top_pct']}%（閾值 {THRESHOLDS['agent_overload_pct']}%）")
    if checks["tmp"]["size_mb"] >= THRESHOLDS["tmp_files_mb"]:
        issues.append(f"🟡 tmp 垃圾 {checks['tmp']['size_mb']} MB（閾值 {THRESHOLDS['tmp_files_mb']} MB）")
    if checks["stall"]["stalled"]:
        issues.append(f"🔴 Cron 疑似卡住（{checks['stall']['last_run_ago_min']:.0f} min 無任何 job 執行）")
    return issues

def run():
    log("=" * 60)
    log("OpenClaw 系統健康監測 啟動")
    d, jobs = load_jobs()

    checks = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors":    check_errors(jobs),
        "timeouts":  check_timeouts(jobs),
        "balance":   check_agent_balance(jobs),
        "tmp":       check_tmp_files(),
        "stall":     check_last_run(jobs),
    }

    # ── Auto-fixes ──
    fixes = {}

    if checks["timeouts"]["risky_pct"] >= THRESHOLDS["timeout_risky_pct"]:
        fixes["timeout"] = autofix_timeouts(d, jobs)
        d, jobs = load_jobs()  # reload after fix

    if checks["tmp"]["size_mb"] >= THRESHOLDS["tmp_files_mb"]:
        fixes["tmp_clean"] = autofix_tmp_files(checks["tmp"])

    if checks["balance"]["no_agent_count"] > 0:
        fixes["orphan"] = autofix_orphan_agents(d, jobs)
        d, jobs = load_jobs()

    checks["auto_fixes"] = fixes

    # ── Report ──
    issues = build_report(checks)

    log(f"Jobs: {checks['errors']['total']} | "
        f"Errors: {checks['errors']['real_count']} real / {checks['errors']['stale_count']} stale | "
        f"Timeout risk: {checks['timeouts']['risky_pct']}% | "
        f"Top agent: {checks['balance']['top_agent']} {checks['balance']['top_pct']}% | "
        f"Tmp: {checks['tmp']['size_mb']}MB | "
        f"Last run: {checks['stall']['last_run_ago_min']}min ago")

    if issues:
        log(f"⚠️  {len(issues)} issue(s) detected:")
        for i in issues:
            log(f"   {i}")
    else:
        log("✅ 系統健康，無需處理")

    if fixes:
        log(f"🔧 自動修復: {fixes}")

    # ── Save metrics ──
    history = []
    if os.path.exists(METRICS_FILE):
        try:
            history = json.load(open(METRICS_FILE))
        except Exception:
            history = []
    history.append(checks)
    history = history[-168:]  # keep last 7 days (168 hourly records)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    # ── Exit code: 0=healthy, 1=has issues ──
    return 0 if not issues else 1

if __name__ == "__main__":
    sys.exit(run())
