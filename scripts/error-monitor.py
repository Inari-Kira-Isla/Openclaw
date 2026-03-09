#!/usr/bin/env python3
"""
OpenClaw Error Monitor
監控錯誤日誌並發送到 n8n/Slack
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================

# 錯誤日誌路徑
ERROR_LOG_PATHS = [
    "~/.openclaw/logs/error.log",
    "/var/log/openclaw/error.log",
    "./error.log"
]

# n8n Webhook URL
N8N_WEBHOOK_URL = os.environ.get(
    "N8N_WEBHOOK_URL",
    "https://your-n8n-cloud.com/webhook/error"
)

# Slack Webhook URL
SLACK_WEBHOOK_URL = os.environ.get(
    "SLACK_WEBHOOK_URL",
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
)

# 錯誤關鍵詞
ERROR_KEYWORDS = [
    "ERROR",
    "CRITICAL",
    "FATAL",
    "Exception",
    "Traceback",
    "Failed",
    "Error:"
]

# 檢查間隔 (秒)
CHECK_INTERVAL = 60

# ==================== 功能 ====================

def read_last_lines(filepath, num_lines=10):
    """讀取日誌檔案最後幾行"""
    try:
        filepath = os.path.expanduser(filepath)
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[-num_lines:] if len(lines) > num_lines else lines
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def parse_errors(lines):
    """解析錯誤行"""
    errors = []
    for line in lines:
        for keyword in ERROR_KEYWORDS:
            if keyword in line:
                errors.append({
                    "timestamp": datetime.now().isoformat(),
                    "keyword": keyword,
                    "message": line.strip(),
                    "source": "openclaw"
                })
                break
    return errors

def send_to_n8n(errors):
    """發送到 n8n Webhook"""
    if not errors:
        return
    
    payload = {
        "source": "openclaw-error-monitor",
        "errors": errors,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ 發送到 n8n 成功 ({len(errors)} errors)")
        else:
            print(f"❌ n8n 發送失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ n8n 連接錯誤: {e}")

def send_to_slack(errors):
    """發送到 Slack"""
    if not errors:
        return
    
    # 格式化訊息
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 OpenClaw Error Alert"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{len(errors)} 個錯誤被偵測*"
            }
        }
    ]
    
    for error in errors[:5]:  # 最多顯示 5 個
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"• `{error['keyword']}`: {error['message'][:100]}"
            }
        })
    
    # 新增操作按鈕
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "🔧 自動修復"
                },
                "style": "primary",
                "action_id": "auto_fix",
                "value": json.dumps(errors)
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "👀 查看詳情"
                },
                "action_id": "view_details",
                "value": json.dumps(errors)
            }
        ]
    })
    
    payload = {"blocks": blocks}
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ 發送到 Slack 成功 ({len(errors)} errors)")
        else:
            print(f"❌ Slack 發送失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ Slack 連接錯誤: {e}")

def monitor():
    """監控主循環"""
    print("=" * 50)
    print("🔍 OpenClaw Error Monitor 啟動")
    print("=" * 50)
    print(f"檢查間隔: {CHECK_INTERVAL} 秒")
    print(f"監控路徑: {ERROR_LOG_PATHS}")
    print()
    
    # 追蹤已發送的錯誤
    sent_errors = set()
    
    while True:
        try:
            all_errors = []
            
            for log_path in ERROR_LOG_PATHS:
                lines = read_last_lines(log_path)
                if lines:
                    errors = parse_errors(lines)
                    all_errors.extend(errors)
            
            # 過濾重複
            new_errors = []
            for error in all_errors:
                error_key = f"{error['keyword']}:{error['message'][:50]}"
                if error_key not in sent_errors:
                    new_errors.append(error)
                    sent_errors.add(error_key)
            
            # 發送新錯誤
            if new_errors:
                print(f"\n🚨 偵測到 {len(new_errors)} 個新錯誤")
                send_to_n8n(new_errors)
                send_to_slack(new_errors)
            
        except KeyboardInterrupt:
            print("\n\n👋 監控停止")
            break
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        time.sleep(CHECK_INTERVAL)

# ==================== 測試 ====================

def test_send():
    """測試發送"""
    test_errors = [
        {
            "timestamp": datetime.now().isoformat(),
            "keyword": "ERROR",
            "message": "Test error message from OpenClaw",
            "source": "openclaw-test"
        }
    ]
    
    print("🧪 測試發送...")
    send_to_n8n(test_errors)
    send_to_slack(test_errors)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_send()
    else:
        monitor()
