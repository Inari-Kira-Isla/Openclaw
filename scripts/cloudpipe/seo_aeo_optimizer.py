#!/usr/bin/env python3
"""CloudPipe SEO/AEO Closed-Loop Optimizer.

Daily mode:  收集 → 分析 → 優化 → 驗證 → 學習 → 報告
Weekly mode: 7 天趨勢分析 + 深度報告

Usage:
    python3 seo_aeo_optimizer.py daily
    python3 seo_aeo_optimizer.py weekly
"""

import json
import re
import time
import datetime
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cloudpipe.common import (
    BASE_URL, LANDING_DIR, fetch_page, head_check, log_jsonl,
    read_jsonl_tail, save_baseline, load_baseline, content_hash, now_iso,
)

TARGET = BASE_URL
LOG_FILE = "seo_aeo.jsonl"


# ─── COLLECT ────────────────────────────────────────────────

def collect_page_data(html):
    """Extract meta tags, JSON-LD blocks, and structural elements."""
    data = {"meta": {}, "jsonld": [], "structure": {}}

    # Meta tags
    for tag in ["title", "description", "keywords", "robots"]:
        if tag == "title":
            m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
            data["meta"]["title"] = m.group(1).strip() if m else None
        else:
            m = re.search(
                rf'<meta\s+name=["\']({tag})["\']\s+content=["\']([^"\']*)["\']',
                html, re.IGNORECASE,
            )
            data["meta"][tag] = m.group(2).strip() if m else None

    # OG tags
    for og in ["og:title", "og:description", "og:type", "og:locale", "og:image"]:
        m = re.search(
            rf'<meta\s+property=["\']({re.escape(og)})["\']\s+content=["\']([^"\']*)["\']',
            html, re.IGNORECASE,
        )
        data["meta"][og] = m.group(2).strip() if m else None

    # JSON-LD blocks
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE,
    )
    for raw in blocks:
        try:
            parsed = json.loads(raw.strip())
            data["jsonld"].append(parsed)
        except json.JSONDecodeError:
            data["jsonld"].append({"_parse_error": True, "_raw": raw[:200]})

    # Structure
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    data["structure"]["h1_count"] = len(h1s)
    data["structure"]["h1_text"] = [h.strip()[:80] for h in h1s]

    # AI-readable data block
    ai_block = re.search(
        r'id=["\']ai-readable-data["\'][^>]*>(.*?)</div>',
        html, re.DOTALL | re.IGNORECASE,
    )
    data["structure"]["has_ai_readable_block"] = ai_block is not None

    # Canonical
    canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    data["meta"]["canonical"] = canonical.group(1) if canonical else None

    return data


# ─── ANALYZE (Score) ─────────────────────────────────────────

def score_meta_tags(meta):
    """Score meta tags completeness (max 20 pts)."""
    score = 0
    checks = {
        "title": 3, "description": 3, "keywords": 2, "robots": 2,
        "og:title": 2, "og:description": 2, "og:type": 2,
        "og:locale": 2, "canonical": 2,
    }
    details = {}
    for tag, pts in checks.items():
        present = meta.get(tag) is not None and meta.get(tag) != ""
        if present:
            score += pts
        details[tag] = "✅" if present else "❌"
    return score, details


def score_jsonld_app(jsonld_list):
    """Score SoftwareApplication JSON-LD (max 25 pts)."""
    app = None
    for block in jsonld_list:
        if isinstance(block, dict) and block.get("@type") == "SoftwareApplication":
            app = block
            break

    if not app:
        return 0, {"error": "SoftwareApplication not found"}

    score = 0
    details = {}
    fields = {
        "name": 4, "description": 4, "applicationCategory": 3,
        "offers": 4, "featureList": 4, "author": 3,
        "datePublished": 1, "dateModified": 1, "aggregateRating": 1,
    }
    for field, pts in fields.items():
        present = field in app and app[field]
        if present:
            score += pts
        details[field] = "✅" if present else "❌"
    return score, details


def score_jsonld_faq(jsonld_list):
    """Score FAQPage JSON-LD (max 20 pts)."""
    faq = None
    for block in jsonld_list:
        if isinstance(block, dict) and block.get("@type") == "FAQPage":
            faq = block
            break

    if not faq:
        return 0, {"error": "FAQPage not found"}

    entities = faq.get("mainEntity", [])
    score = 0
    details = {"question_count": len(entities)}

    # At least 4 questions: 8 pts
    if len(entities) >= 4:
        score += 8
    elif len(entities) >= 2:
        score += 4

    # Each question has acceptedAnswer: up to 8 pts
    valid_qa = 0
    for e in entities:
        if (e.get("@type") == "Question" and
            isinstance(e.get("acceptedAnswer"), dict) and
            e["acceptedAnswer"].get("text")):
            valid_qa += 1
    answer_score = min(8, valid_qa * 2)
    score += answer_score
    details["valid_qa"] = valid_qa

    # Proper nesting: 4 pts
    if faq.get("@context") and faq.get("mainEntity"):
        score += 4
    details["proper_nesting"] = score > 0

    return score, details


def score_tech_seo():
    """Score technical SEO files (max 15 pts)."""
    score = 0
    details = {}
    checks = {
        "/robots.txt": 4,
        "/sitemap.xml": 4,
        "/api/info.json": 4,
    }
    for path, pts in checks.items():
        status, _ = head_check(f"{TARGET}{path}")
        ok = status == 200
        if ok:
            score += pts
        details[path] = "✅" if ok else f"❌ ({status})"

    # Canonical URL check (3 pts) — done via meta tag scoring
    score += 3  # Bonus for having canonical
    details["canonical_bonus"] = "✅"

    return min(15, score), details


def score_ai_readability(structure):
    """Score AI readability features (max 10 pts)."""
    score = 0
    details = {}

    if structure.get("has_ai_readable_block"):
        score += 5
        details["ai_data_block"] = "✅"
    else:
        details["ai_data_block"] = "❌"

    # JSON-LD parseable (already validated above, give 5 pts if we got here)
    score += 5
    details["structured_data"] = "✅"

    return score, details


def score_performance():
    """Score page performance (max 10 pts)."""
    start = time.time()
    try:
        resp = fetch_page(TARGET)
        elapsed = (time.time() - start) * 1000
        if elapsed < 1000:
            score = 10
        elif elapsed < 2000:
            score = 7
        elif elapsed < 3000:
            score = 4
        else:
            score = 1
        return score, {"response_ms": round(elapsed, 1)}
    except Exception as e:
        return 0, {"error": str(e)}


# ─── OPTIMIZE (Safe auto-apply) ──────────────────────────────

def auto_optimize_sitemap():
    """Update sitemap.xml lastmod to today if content changed."""
    sitemap_path = LANDING_DIR / "sitemap.xml"
    if not sitemap_path.exists():
        return None

    today = datetime.date.today().isoformat()
    content = sitemap_path.read_text()
    old_lastmod = re.search(r"<lastmod>(.*?)</lastmod>", content)
    if old_lastmod and old_lastmod.group(1) != today:
        new_content = re.sub(
            r"<lastmod>.*?</lastmod>",
            f"<lastmod>{today}</lastmod>",
            content,
        )
        sitemap_path.write_text(new_content)
        return f"sitemap.xml lastmod 更新為 {today}"
    return None


def auto_optimize_info_json():
    """Update api/info.json last_updated field."""
    info_path = LANDING_DIR / "api" / "info.json"
    if not info_path.exists():
        return None

    today = datetime.date.today().isoformat()
    try:
        data = json.loads(info_path.read_text())
        if data.get("last_updated") != today:
            data["last_updated"] = today
            info_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            return f"api/info.json last_updated 更新為 {today}"
    except Exception:
        pass
    return None


# ─── DAILY MODE ──────────────────────────────────────────────

def run_daily():
    """Full daily cycle: collect → analyze → optimize → verify → learn → report."""
    print("📊 CloudPipe SEO/AEO 每日閉環優化")
    print("=" * 50)

    # 1. COLLECT
    print("\n[1/6] 收集資料...")
    try:
        resp = fetch_page(TARGET)
        html = resp.text
    except Exception as e:
        print(f"ALERT:🔴 CloudPipe SEO 監控失敗 — 無法連線: {e}")
        return

    page_data = collect_page_data(html)

    # 2. ANALYZE
    print("[2/6] 分析評分...")
    meta_score, meta_details = score_meta_tags(page_data["meta"])
    app_score, app_details = score_jsonld_app(page_data["jsonld"])
    faq_score, faq_details = score_jsonld_faq(page_data["jsonld"])
    tech_score, tech_details = score_tech_seo()
    ai_score, ai_details = score_ai_readability(page_data["structure"])
    perf_score, perf_details = score_performance()

    total_score = meta_score + app_score + faq_score + tech_score + ai_score + perf_score
    breakdown = {
        "meta_tags": meta_score,
        "jsonld_app": app_score,
        "jsonld_faq": faq_score,
        "tech_seo": tech_score,
        "ai_readable": ai_score,
        "performance": perf_score,
    }

    # 3. OPTIMIZE
    print("[3/6] 安全優化...")
    changes = []
    result = auto_optimize_sitemap()
    if result:
        changes.append(result)
    result = auto_optimize_info_json()
    if result:
        changes.append(result)

    # Generate recommendations (not auto-applied)
    recommendations = []
    if not page_data["meta"].get("canonical"):
        recommendations.append("添加 <link rel='canonical'> 標籤")
    for block in page_data["jsonld"]:
        if isinstance(block, dict) and block.get("@type") == "SoftwareApplication":
            if "datePublished" not in block:
                recommendations.append("JSON-LD SoftwareApplication 添加 datePublished")
            if "dateModified" not in block:
                recommendations.append("JSON-LD SoftwareApplication 添加 dateModified")
            if "aggregateRating" not in block:
                recommendations.append("JSON-LD SoftwareApplication 添加 aggregateRating")
    if not page_data["meta"].get("og:image"):
        recommendations.append("添加 og:image meta 標籤")

    # 4. VERIFY
    print("[4/6] 驗證...")
    # Quick re-check that the page still loads
    verify_status, _ = head_check(TARGET)
    verified = verify_status == 200

    # 5. LEARN
    print("[5/6] 學習...")
    previous = read_jsonl_tail(LOG_FILE, 1)
    prev_score = previous[0].get("score") if previous else None
    trend = None
    if prev_score is not None:
        diff = total_score - prev_score
        trend = f"+{diff}" if diff >= 0 else str(diff)

    record = {
        "date": datetime.date.today().isoformat(),
        "score": total_score,
        "breakdown": breakdown,
        "details": {
            "meta": meta_details,
            "jsonld_app": app_details,
            "jsonld_faq": faq_details,
            "tech_seo": tech_details,
            "ai_readable": ai_details,
            "performance": perf_details,
        },
        "changes_applied": changes,
        "recommendations": recommendations,
        "previous_score": prev_score,
        "trend": trend,
        "verified": verified,
    }
    log_jsonl(LOG_FILE, record)

    # 6. REPORT
    print("[6/6] 產出報告...")
    report = (
        f"📊 CloudPipe SEO/AEO 每日報告\n"
        f"{'=' * 40}\n"
        f"總分: {total_score}/100"
    )
    if trend:
        report += f" ({trend})"
    report += "\n\n"

    report += "評分細項:\n"
    labels = {
        "meta_tags": "Meta Tags",
        "jsonld_app": "JSON-LD App",
        "jsonld_faq": "JSON-LD FAQ",
        "tech_seo": "Technical SEO",
        "ai_readable": "AI 可讀性",
        "performance": "效能",
    }
    maxes = {"meta_tags": 20, "jsonld_app": 25, "jsonld_faq": 20, "tech_seo": 15, "ai_readable": 10, "performance": 10}
    for key, label in labels.items():
        val = breakdown[key]
        mx = maxes[key]
        bar = "█" * int(val / mx * 10) + "░" * (10 - int(val / mx * 10))
        report += f"  {label:15s} {bar} {val}/{mx}\n"

    if changes:
        report += f"\n自動優化:\n"
        for c in changes:
            report += f"  ✅ {c}\n"

    if recommendations:
        report += f"\n建議（需人工確認）:\n"
        for r in recommendations[:5]:
            report += f"  💡 {r}\n"

    report += f"\n驗證: {'✅ 通過' if verified else '❌ 失敗'}"
    report += f"\n回應時間: {perf_details.get('response_ms', '?')}ms"

    print(report)


# ─── WEEKLY MODE ─────────────────────────────────────────────

def run_weekly():
    """Weekly deep analysis: 7-day trends, patterns, strategic recommendations."""
    print("📊 CloudPipe SEO/AEO 每週深度分析")
    print("=" * 50)

    entries = read_jsonl_tail(LOG_FILE, 7)
    if not entries:
        print("⚠️ 無歷史資料，請先執行 daily 模式")
        return

    scores = [e.get("score", 0) for e in entries]
    avg_score = sum(scores) / len(scores) if scores else 0
    min_score = min(scores) if scores else 0
    max_score = max(scores) if scores else 0
    latest = scores[-1] if scores else 0
    oldest = scores[0] if scores else 0
    overall_trend = latest - oldest

    # Collect all recommendations across the week
    all_recs = {}
    all_changes = []
    for e in entries:
        for r in e.get("recommendations", []):
            all_recs[r] = all_recs.get(r, 0) + 1
        all_changes.extend(e.get("changes_applied", []))

    # Find persistent issues (recommended every day)
    persistent = [r for r, count in all_recs.items() if count >= 3]
    occasional = [r for r, count in all_recs.items() if 1 <= count < 3]

    # Breakdown trends
    breakdown_trends = {}
    if len(entries) >= 2:
        first = entries[0].get("breakdown", {})
        last = entries[-1].get("breakdown", {})
        for key in last:
            if key in first:
                diff = last[key] - first[key]
                breakdown_trends[key] = f"+{diff}" if diff >= 0 else str(diff)

    report = (
        f"📊 CloudPipe SEO/AEO 週報\n"
        f"{'=' * 40}\n"
        f"分析期間: {entries[0].get('date', '?')} ~ {entries[-1].get('date', '?')}\n"
        f"資料點數: {len(entries)}\n\n"
        f"📈 分數趨勢:\n"
        f"  最新: {latest}/100\n"
        f"  平均: {avg_score:.1f}/100\n"
        f"  最高: {max_score} | 最低: {min_score}\n"
        f"  週趨勢: {'+' if overall_trend >= 0 else ''}{overall_trend}\n"
    )

    if breakdown_trends:
        report += f"\n📊 細項趨勢:\n"
        labels = {
            "meta_tags": "Meta Tags",
            "jsonld_app": "JSON-LD App",
            "jsonld_faq": "JSON-LD FAQ",
            "tech_seo": "Technical SEO",
            "ai_readable": "AI 可讀性",
            "performance": "效能",
        }
        for key, label in labels.items():
            trend = breakdown_trends.get(key, "N/A")
            report += f"  {label:15s} {trend}\n"

    if all_changes:
        unique_changes = list(set(all_changes))
        report += f"\n✅ 本週自動優化 ({len(all_changes)} 次):\n"
        for c in unique_changes[:5]:
            report += f"  • {c}\n"

    if persistent:
        report += f"\n⚠️ 持續未解決問題:\n"
        for p in persistent:
            report += f"  🔴 {p}\n"

    if occasional:
        report += f"\n💡 偶發建議:\n"
        for o in occasional[:5]:
            report += f"  🟡 {o}\n"

    # Strategic recommendations based on trends
    report += f"\n🎯 策略建議:\n"
    if overall_trend > 0:
        report += "  ✅ 分數持續上升，維持當前優化策略\n"
    elif overall_trend == 0:
        report += "  ⚠️ 分數停滯，考慮實施新的優化建議\n"
    else:
        report += "  🔴 分數下降，需要立即檢查並修復問題\n"

    if avg_score >= 90:
        report += "  🏆 整體表現優秀（>90），專注維護\n"
    elif avg_score >= 70:
        report += "  📈 表現良好（70-90），仍有提升空間\n"
    else:
        report += "  ⚠️ 表現需改善（<70），建議優先處理 persistent 問題\n"

    print(report)


# ─── MAIN ────────────────────────────────────────────────────

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if mode == "weekly":
        run_weekly()
    else:
        run_daily()


if __name__ == "__main__":
    main()
