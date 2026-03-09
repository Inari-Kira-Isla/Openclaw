#!/usr/bin/env python3
"""CloudPipe Security Audit — runs daily at 08:00 PST.

Checks: security headers, mixed content, dangerous paths, SSL details,
external scripts, content integrity. Outputs a security score (0-100).
"""

import json
import re
import ssl
import socket
import datetime
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cloudpipe.common import (
    BASE_URL, fetch_page, head_check, log_jsonl,
    save_baseline, load_baseline, content_hash, now_iso,
)

TARGET = BASE_URL

REQUIRED_HEADERS = {
    "strict-transport-security": "high",
    "x-frame-options": "medium",
    "x-content-type-options": "medium",
    "referrer-policy": "low",
    "content-security-policy": "high",
    "permissions-policy": "low",
}

DANGEROUS_PATHS = [
    "/.env", "/.git/config", "/wp-admin/", "/admin/",
    "/wp-login.php", "/.htaccess", "/.DS_Store",
    "/server-info", "/server-status", "/phpinfo.php",
]

TRUSTED_DOMAINS = {
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdn.jsdelivr.net",
}


def check_security_headers(resp_headers):
    """Check response headers against required security headers."""
    findings = []
    header_status = {}
    for header, severity in REQUIRED_HEADERS.items():
        value = resp_headers.get(header)
        header_status[header] = value or "MISSING"
        if not value:
            findings.append({
                "type": "missing_header",
                "header": header,
                "severity": severity,
                "detail": f"缺少 {header} 安全標頭",
            })
    return findings, header_status


def check_mixed_content(html):
    """Scan for http:// references in src, href, action attributes."""
    findings = []
    matches = re.findall(
        r'(?:src|href|action)\s*=\s*["\']http://[^"\']+["\']',
        html, re.IGNORECASE,
    )
    if matches:
        findings.append({
            "type": "mixed_content",
            "severity": "medium",
            "detail": f"發現 {len(matches)} 個 http:// 引用",
            "examples": matches[:3],
        })
    return findings


def check_exposed_endpoints(base_url):
    """Probe dangerous paths, alert if any return non-404."""
    findings = []
    for path in DANGEROUS_PATHS:
        status, err = head_check(f"{base_url}{path}")
        if status is not None and status != 404:
            findings.append({
                "type": "exposed_endpoint",
                "path": path,
                "status": status,
                "severity": "high",
                "detail": f"{path} 回傳 {status}（應為 404）",
            })
    return findings


def check_ssl_details(hostname):
    """Check TLS version, cipher suite, certificate details."""
    findings = []
    info = {}
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(10)
            s.connect((hostname, 443))
            cert = s.getpeercert()
            protocol = s.version()
            cipher = s.cipher()

        info = {
            "protocol": protocol,
            "cipher": cipher[0] if cipher else "unknown",
            "cert_subject": dict(x[0] for x in cert.get("subject", [])),
        }

        if protocol in ("TLSv1", "TLSv1.1"):
            findings.append({
                "type": "weak_tls",
                "severity": "critical",
                "detail": f"使用過時的 {protocol}",
            })

        expiry = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)).days
        info["cert_expiry_days"] = days_left
        if days_left < 30:
            findings.append({
                "type": "cert_expiring",
                "severity": "high",
                "detail": f"SSL 憑證將在 {days_left} 天後到期",
            })
    except Exception as e:
        findings.append({
            "type": "ssl_error",
            "severity": "critical",
            "detail": f"SSL 檢查失敗: {e}",
        })
        info["error"] = str(e)

    return findings, info


def check_external_scripts(html):
    """Verify all script src domains are trusted."""
    findings = []
    script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    for src in script_srcs:
        if src.startswith("http"):
            domain = urlparse(src).hostname
            if domain and domain not in TRUSTED_DOMAINS:
                findings.append({
                    "type": "untrusted_script",
                    "severity": "high",
                    "detail": f"外部腳本來自非信任域名: {domain}",
                    "src": src,
                })
    return findings


def check_content_integrity(html):
    """Full page hash vs baseline."""
    findings = []
    current = content_hash(html)
    baseline = load_baseline("security_content_hash")

    if baseline is None:
        save_baseline("security_content_hash", {"hash": current, "set_at": now_iso()})
        return findings, {"status": "baseline_established"}

    if current != baseline["hash"]:
        findings.append({
            "type": "content_changed",
            "severity": "medium",
            "detail": "頁面內容與安全基準不同（可能是正常部署）",
        })
        # Update baseline after flagging
        save_baseline("security_content_hash", {"hash": current, "set_at": now_iso()})
        return findings, {"status": "changed"}

    return findings, {"status": "unchanged"}


def check_supporting_security_files():
    """Check robots.txt and security.txt exist."""
    findings = []
    for path, name in [("/robots.txt", "robots.txt"), ("/.well-known/security.txt", "security.txt")]:
        status, err = head_check(f"{TARGET}{path}")
        if status != 200:
            findings.append({
                "type": "missing_security_file",
                "severity": "low",
                "detail": f"{name} 不存在或無法存取 (status={status})",
            })
    return findings


def calculate_score(findings):
    """Score out of 100. Deduct points per finding by severity."""
    score = 100
    deductions = {"critical": 25, "high": 10, "medium": 5, "low": 2}
    for f in findings:
        score -= deductions.get(f.get("severity", "low"), 2)
    return max(0, score)


def main():
    report = {
        "timestamp": now_iso(),
        "target": TARGET,
        "checks": {},
        "findings": [],
    }

    # 1. Fetch page
    try:
        resp = fetch_page(TARGET)
        html = resp.text
        report["checks"]["http_status"] = resp.status_code
    except Exception as e:
        print(f"ALERT:🔴 CloudPipe 安全審計失敗 — 無法連線: {e}")
        return

    # 2. Security headers
    header_findings, header_status = check_security_headers(resp.headers)
    report["findings"].extend(header_findings)
    report["checks"]["headers"] = header_status

    # 3. Mixed content
    report["findings"].extend(check_mixed_content(html))

    # 4. Exposed endpoints
    report["findings"].extend(check_exposed_endpoints(TARGET))

    # 5. SSL details
    ssl_findings, ssl_info = check_ssl_details("cloudpipe-landing.vercel.app")
    report["findings"].extend(ssl_findings)
    report["checks"]["ssl"] = ssl_info

    # 6. External scripts
    report["findings"].extend(check_external_scripts(html))

    # 7. Content integrity
    integrity_findings, integrity_info = check_content_integrity(html)
    report["findings"].extend(integrity_findings)
    report["checks"]["content_integrity"] = integrity_info

    # 8. Supporting security files
    report["findings"].extend(check_supporting_security_files())

    # 9. Score
    score = calculate_score(report["findings"])
    report["score"] = score

    # Count by severity
    by_severity = {}
    for f in report["findings"]:
        sev = f.get("severity", "low")
        by_severity[sev] = by_severity.get(sev, 0) + 1
    report["by_severity"] = by_severity

    # 10. Log
    log_jsonl("security.jsonl", report)

    # 11. Output
    critical = by_severity.get("critical", 0)
    high = by_severity.get("high", 0)
    medium = by_severity.get("medium", 0)
    low = by_severity.get("low", 0)
    total = len(report["findings"])

    summary = (
        f"🛡️ CloudPipe 安全審計報告\n"
        f"安全評分: {score}/100\n"
        f"發現問題: {total} 個\n"
        f"  Critical: {critical} | High: {high} | Medium: {medium} | Low: {low}\n"
    )

    if report["findings"]:
        summary += "\n主要發現:\n"
        for f in report["findings"][:8]:
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}.get(f["severity"], "⚪")
            summary += f"  {icon} [{f['severity'].upper()}] {f['detail']}\n"

    if critical > 0:
        print(f"ALERT:{summary}")
    else:
        print(summary)


if __name__ == "__main__":
    main()
