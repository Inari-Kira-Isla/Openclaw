#!/usr/bin/env python3
"""CloudPipe Uptime Monitor — runs every 15 minutes.

Checks: HTTP status, response time, SSL expiry, JSON-LD validity,
content integrity (hash), external resources, supporting files.
"""

import json
import re
import ssl
import socket
import time
import datetime
import sys
from pathlib import Path

# Add parent to path for common module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cloudpipe.common import (
    BASE_URL, fetch_page, head_check, log_jsonl,
    save_baseline, load_baseline, content_hash, now_iso,
)

TARGET = BASE_URL


def check_http(url):
    """GET request, return (status, response_ms, html_text)."""
    start = time.time()
    resp = fetch_page(url)
    elapsed_ms = (time.time() - start) * 1000
    return resp.status_code, round(elapsed_ms, 1), resp.text


def check_ssl_expiry(hostname):
    """Check SSL certificate days until expiry."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(10)
            s.connect((hostname, 443))
            cert = s.getpeercert()
        expiry_str = cert["notAfter"]
        expiry = datetime.datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)).days
        return days_left, None
    except Exception as e:
        return None, str(e)


def validate_jsonld(html):
    """Extract JSON-LD blocks, validate parse and required @types."""
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE,
    )
    if not blocks:
        return False, {"error": "no JSON-LD blocks found", "count": 0}

    parsed = []
    types_found = set()
    for i, raw in enumerate(blocks):
        try:
            data = json.loads(raw.strip())
            t = data.get("@type", "unknown")
            types_found.add(t)
            parsed.append({"index": i, "type": t, "valid": True})
        except json.JSONDecodeError as e:
            parsed.append({"index": i, "valid": False, "error": str(e)})
            return False, {"blocks": parsed, "count": len(blocks)}

    required = {"SoftwareApplication", "FAQPage"}
    missing = required - types_found
    ok = len(missing) == 0
    return ok, {
        "count": len(blocks),
        "types": list(types_found),
        "missing_types": list(missing),
        "valid": ok,
    }


def check_title(html):
    """Check <title> tag exists and is non-empty."""
    match = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if not match:
        return False, "missing"
    title = match.group(1).strip()
    if not title:
        return False, "empty"
    return True, title


def check_content_integrity(html):
    """Hash body content, compare against baseline."""
    body_match = re.search(r"<body[^>]*>(.*)</body>", html, re.DOTALL | re.IGNORECASE)
    if not body_match:
        return False, {"error": "no <body> found"}

    current = content_hash(body_match.group(1))
    baseline = load_baseline("content_hash")

    if baseline is None:
        # First run — establish baseline
        save_baseline("content_hash", {"hash": current, "set_at": now_iso()})
        return False, {"status": "baseline_established", "hash": current[:16]}

    if current != baseline["hash"]:
        return True, {
            "status": "changed",
            "previous": baseline["hash"][:16],
            "current": current[:16],
            "baseline_set": baseline.get("set_at", "unknown"),
        }

    return False, {"status": "unchanged", "hash": current[:16]}


def check_supporting_files():
    """Check robots.txt, sitemap.xml, api/info.json existence."""
    results = {}
    for path in ["/robots.txt", "/sitemap.xml", "/api/info.json"]:
        status, err = head_check(f"{TARGET}{path}")
        results[path] = {"status": status, "error": err}
    return results


def check_external_resources():
    """HEAD request key external resources."""
    urls = [
        "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Space+Mono:wght@400;700&family=Sora:wght@300;400;500;600;700&display=swap",
    ]
    results = []
    for url in urls:
        status, err = head_check(url)
        results.append({"url": url[:60], "status": status, "error": err})
    return results


def main():
    results = {"timestamp": now_iso(), "checks": {}}
    alerts = []

    # 1. HTTP Status + Response Time
    try:
        status, elapsed, html = check_http(TARGET)
        results["checks"]["http"] = {"status": status, "response_ms": elapsed}
        if status != 200:
            alerts.append(f"HTTP {status} — 網站可能下線!")
        if elapsed > 3000:
            alerts.append(f"回應過慢: {elapsed:.0f}ms")
    except Exception as e:
        results["checks"]["http"] = {"error": str(e)}
        alerts.append(f"無法連線: {e}")
        html = ""

    # 2. SSL Certificate
    ssl_days, ssl_err = check_ssl_expiry("cloudpipe-landing.vercel.app")
    results["checks"]["ssl"] = {"days_until_expiry": ssl_days, "error": ssl_err}
    if ssl_err:
        alerts.append(f"SSL 檢查失敗: {ssl_err}")
    elif ssl_days is not None and ssl_days < 14:
        alerts.append(f"SSL 憑證將在 {ssl_days} 天後到期!")

    if html:
        # 3. Title
        title_ok, title_info = check_title(html)
        results["checks"]["title"] = {"ok": title_ok, "value": title_info}
        if not title_ok:
            alerts.append(f"HTML title 異常: {title_info}")

        # 4. JSON-LD
        jsonld_ok, jsonld_info = validate_jsonld(html)
        results["checks"]["jsonld"] = jsonld_info
        if not jsonld_ok:
            alerts.append(f"JSON-LD 驗證失敗: {jsonld_info.get('missing_types', jsonld_info.get('error', ''))}")

        # 5. Content Integrity
        changed, hash_info = check_content_integrity(html)
        results["checks"]["content_hash"] = hash_info
        if changed:
            alerts.append("內容雜湊變更 — 可能有未授權修改")

    # 6. External Resources
    ext = check_external_resources()
    results["checks"]["external_resources"] = ext
    for r in ext:
        if r.get("error") or (r.get("status") and r["status"] >= 400):
            alerts.append(f"外部資源異常: {r['url']} (status={r.get('status')})")

    # 7. Supporting Files
    supporting = check_supporting_files()
    results["checks"]["supporting_files"] = supporting

    # Final
    results["alert_count"] = len(alerts)
    results["status"] = "ALERT" if alerts else "OK"

    log_jsonl("uptime.jsonl", results)

    if alerts:
        msg = "🔴 CloudPipe 網站告警\n\n" + "\n".join(f"• {a}" for a in alerts)
        print(f"ALERT:{msg}")
    else:
        ssl_info = f"SSL: {ssl_days}d" if ssl_days else "SSL: N/A"
        elapsed_info = results["checks"].get("http", {}).get("response_ms", "?")
        print(f"✅ CloudPipe OK | {elapsed_info}ms | {ssl_info}")


if __name__ == "__main__":
    main()
