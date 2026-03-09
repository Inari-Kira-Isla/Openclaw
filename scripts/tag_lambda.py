#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tag λ 自動調整系統 - Tag Lambda Auto-Adjustment System
根據標籤自動調整權重
"""

import os
import json
import math
from datetime import datetime, timedelta

class TagLambdaSystem:
    def __init__(self):
        self.data_path = os.path.expanduser("~/.openclaw/workspace/memory/tag_lambda.json")
        self.load_data()
        
        # 預設 λ 值
        self.default_lambda = 0.5
        
        # 標籤分類與 λ 值
        self.tag_categories = {
            "high_priority": {
                "tags": ["價格", "行情", "報價", "成本", "利潤", "投資", "賺錢"],
                "lambda": 0.9,  # 高 λ，資訊價值 decay 慢
                "description": "商業價值高"
            },
            "low_priority": {
                "tags": ["原理", "理論", "教學", "歷史", "背景"],
                "lambda": 0.1,  # 低 λ，資訊價值 decay 快
                "description": "基礎知識"
            },
            "medium_priority": {
                "tags": ["技術", "代碼", "工具", "應用"],
                "lambda": 0.5,
                "description": "實用知識"
            }
        }
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "records": [],
                "adjustments": []
            }
    
    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def detect_tags(self, text):
        """偵測文本中的標籤"""
        detected = []
        
        for category, config in self.tag_categories.items():
            for tag in config["tags"]:
                if tag in text:
                    detected.append({
                        "tag": tag,
                        "category": category,
                        "lambda": config["lambda"]
                    })
        
        return detected
    
    def calculate_lambda(self, tags):
        """計算綜合 λ 值"""
        if not tags:
            return self.default_lambda
        
        # 平均 λ 值
        avg_lambda = sum(t["lambda"] for t in tags) / len(tags)
        
        return avg_lambda
    
    def apply_time_decay(self, lambda_value, hours_old):
        """應用時間衰減"""
        # decay formula: value * (lambda ^ hours)
        return lambda_value ** (hours_old / 24)  # 每天 decay 一次
    
    def adjust_record(self, record_id, content, timestamp=None):
        """調整記錄的 λ 值"""
        # 偵測標籤
        tags = self.detect_tags(content)
        
        # 計算 λ
        lambda_value = self.calculate_lambda(tags)
        
        # 計算現在的衰減值
        if timestamp:
            record_time = datetime.fromisoformat(timestamp)
            hours_old = (datetime.now() - record_time).total_seconds() / 3600
            decay_value = self.apply_time_decay(lambda_value, hours_old)
        else:
            decay_value = lambda_value
        
        # 記錄調整
        adjustment = {
            "record_id": record_id,
            "content_preview": content[:50],
            "detected_tags": [t["tag"] for t in tags],
            "base_lambda": lambda_value,
            "current_value": decay_value,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["adjustments"].append(adjustment)
        self.save_data()
        
        return adjustment
    
    def analyze_content(self, content):
        """分析內容並返回標籤建議"""
        tags = self.detect_tags(content)
        
        result = {
            "detected": tags,
            "lambda": self.calculate_lambda(tags),
            "recommendations": []
        }
        
        # 根據 λ 給建議
        if result["lambda"] > 0.7:
            result["recommendations"].append("高價值資訊，建議長期保存")
        elif result["lambda"] < 0.3:
            result["recommendations"].append("基礎知識，可考慮歸檔")
        else:
            result["recommendations"].append("實用資訊，定期回顧")
        
        return result
    
    def batch_process(self, records):
        """批量處理記錄"""
        results = []
        
        for record in records:
            result = self.adjust_record(
                record.get("id", "unknown"),
                record.get("content", ""),
                record.get("timestamp")
            )
            results.append(result)
        
        return results
    
    def get_stats(self):
        """獲取統計"""
        return {
            "total_adjustments": len(self.data.get("adjustments", [])),
            "categories": len(self.tag_categories),
            "high_priority_tags": len(self.tag_categories["high_priority"]["tags"]),
            "low_priority_tags": len(self.tag_categories["low_priority"]["tags"])
        }

if __name__ == "__main__":
    import sys
    
    tls = TagLambdaSystem()
    
    if len(sys.argv) < 2:
        print("Tag λ 自動調整系統")
        print("用法:")
        print("  python tag_lambda.py analyze <內容>")
        print("  python tag_lambda.py stats")
        print("  python tag_lambda.py categories")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "analyze" and len(sys.argv) >= 3:
        content = " ".join(sys.argv[2:])
        result = tls.analyze_content(content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "stats":
        stats = tls.get_stats()
        print(json.dumps(stats, indent=2))
    
    elif cmd == "categories":
        print(json.dumps(tls.tag_categories, indent=2, ensure_ascii=False))
