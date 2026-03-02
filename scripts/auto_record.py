#!/usr/bin/env python3
"""
自動記錄鉤子 - Auto-Record Hook
記錄系統中的重要決策、討論和事件
"""

import os
import json
from datetime import datetime

MEMORY_PATH = os.path.expanduser("~/.openclaw/workspace/memory/")

def record_decision(category, title, content, tags=None):
    record = {
        "type": "decision",
        "category": category,
        "title": title,
        "content": content,
        "tags": tags or [],
        "timestamp": datetime.now().isoformat()
    }
    return _save_record(record)

def record_discussion(topic, participants, summary, outcome=None):
    record = {
        "type": "discussion",
        "topic": topic,
        "participants": participants,
        "summary": summary,
        "outcome": outcome,
        "timestamp": datetime.now().isoformat()
    }
    return _save_record(record)

def record_event(event_type, title, details, severity="normal"):
    record = {
        "type": "event",
        "event_type": event_type,
        "title": title,
        "details": details,
        "severity": severity,
        "timestamp": datetime.now().isoformat()
    }
    return _save_record(record)

def record_learnedLesson(area, lesson, source, tags=None):
    record = {
        "type": "learned_lesson",
        "area": area,
        "lesson": lesson,
        "source": source,
        "tags": tags or [],
        "timestamp": datetime.now().isoformat()
    }
    return _save_record(record)

def _save_record(record):
    os.makedirs(MEMORY_PATH, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"auto-records-{date_str}.jsonl"
    filepath = os.path.join(MEMORY_PATH, filename)
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"✅ Recorded: {record['type']} - {record.get('title', record.get('topic', 'N/A'))}")
    return filepath

def get_today_records():
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(MEMORY_PATH, f"auto-records-{date_str}.jsonl")
    if not os.path.exists(filepath):
        return []
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Auto-Record Hook v1.0")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "decision" and len(sys.argv) >= 4:
        record_decision("system", sys.argv[2], sys.argv[3])
    elif cmd == "list":
        records = get_today_records()
        print(f"📋 今日記錄 ({len(records)} 條):")
        for r in records:
            print(f"  • {r['type']}: {r.get('title', r.get('topic', 'N/A'))}")
