"""Shared utilities for CloudPipe monitoring agents."""

import requests
import json
import datetime
import hashlib
from pathlib import Path

BASE_URL = "https://cloudpipe-landing.vercel.app"
LOG_DIR = Path.home() / ".openclaw/workspace/logs/cloudpipe"
BASELINE_DIR = LOG_DIR / "baselines"
LANDING_DIR = Path.home() / "Documents/cloudpipe-landing"

# Max log entries to keep (90 days at ~96/day for 15-min interval)
MAX_LOG_LINES = 9000


def fetch_page(url=None, timeout=10):
    """Fetch a URL with standard monitoring headers."""
    url = url or BASE_URL
    return requests.get(url, timeout=timeout, headers={
        "User-Agent": "CloudPipe-Monitor/1.0",
        "Accept": "text/html,application/json",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    })


def head_check(url, timeout=5):
    """HEAD request, return (status_code, error_or_None)."""
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        return resp.status_code, None
    except Exception as e:
        return None, str(e)


def log_jsonl(filename, data):
    """Append a JSON line to a log file. Auto-rotates if too large."""
    filepath = LOG_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data["_ts"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(filepath, "a") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    # Simple rotation: truncate oldest if over limit
    _rotate_if_needed(filepath)


def _rotate_if_needed(filepath):
    """Keep only the last MAX_LOG_LINES entries."""
    try:
        lines = filepath.read_text().strip().split("\n")
        if len(lines) > MAX_LOG_LINES:
            filepath.write_text("\n".join(lines[-MAX_LOG_LINES:]) + "\n")
    except Exception:
        pass


def read_jsonl_tail(filename, n=7):
    """Read last N entries from a JSONL log file."""
    filepath = LOG_DIR / filename
    if not filepath.exists():
        return []
    lines = filepath.read_text().strip().split("\n")
    result = []
    for line in lines[-n:]:
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return result


def save_baseline(name, data):
    """Save a baseline snapshot."""
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    filepath = BASELINE_DIR / f"{name}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_baseline(name):
    """Load a baseline snapshot, return None if not found."""
    filepath = BASELINE_DIR / f"{name}.json"
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def content_hash(text):
    """SHA-256 hash of text content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_iso():
    """Current UTC time as ISO string."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
