#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 使用量分析與預算系統
"""

import os
import json
from datetime import datetime, timedelta

class TokenAnalyzer:
    def __init__(self):
        # MiniMax M2.5 定價 (USD per 1M tokens)
        self.pricing = {
            "minimax": {
                "input": 0.8,   # $0.8/1M
                "output": 4.0,   # $4.0/1M
                "currency": "USD"
            },
            "gemini": {
                "input": 0.075,  # $0.075/1M (Flash)
                "output": 0.3,   # $0.3/1M
                "currency": "USD"
            },
            "ollama": {
                "input": 0,      # 本地運行
                "output": 0,
                "currency": "USD"
            }
        }
        
        self.data_path = os.path.expanduser("~/.openclaw/workspace/memory/token_usage.json")
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "sessions": [],
                "daily_usage": {},
                "budgets": {}
            }
    
    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def record_session(self, session_name, input_tokens, output_tokens, model="minimax"):
        """記錄會話"""
        session = {
            "name": session_name,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["sessions"].append(session)
        self.save_data()
        
        return session
    
    def calculate_cost(self, input_tokens, output_tokens, model="minimax"):
        """計算成本"""
        pricing = self.pricing.get(model, self.pricing["minimax"])
        
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return {
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total_cost": round(input_cost + output_cost, 4),
            "currency": pricing["currency"]
        }
    
    def analyze_current_session(self):
        """分析當前會話"""
        # 從 session_status 獲取的數據
        current = {
            "input_tokens": 164000,
            "output_tokens": 670,
            "cached_tokens": 129000,
            "context_used": 99000,
            "context_limit": 200000,
            "duration_minutes": 57
        }
        
        # 計算成本
        cost = self.calculate_cost(current["input_tokens"], current["output_tokens"])
        
        # 計算效率
        efficiency = (current["cached_tokens"] / current["input_tokens"]) * 100 if current["input_tokens"] > 0 else 0
        
        # 預測
        tokens_per_minute = current["input_tokens"] / current["duration_minutes"]
        tokens_per_hour = tokens_per_minute * 60
        tokens_per_day = tokens_per_hour * 24
        
        daily_cost = self.calculate_cost(tokens_per_day, tokens_per_day * 0.01)  # 假設輸出是輸入的1%
        
        return {
            "current": current,
            "cost": cost,
            "efficiency": round(efficiency, 1),
            "predictions": {
                "tokens_per_minute": round(tokens_per_minute, 1),
                "tokens_per_hour": round(tokens_per_hour, 1),
                "tokens_per_day": round(tokens_per_day, 1),
                "estimated_daily_cost": daily_cost["total_cost"],
                "estimated_monthly_cost": daily_cost["total_cost"] * 30
            }
        }
    
    def set_budget(self, model, daily_limit, monthly_limit):
        """設定預算"""
        self.data["budgets"][model] = {
            "daily_limit": daily_limit,
            "monthly_limit": monthly_limit,
            "set_at": datetime.now().isoformat()
        }
        self.save_data()
    
    def check_budget(self, model="minimax"):
        """檢查預算"""
        if model not in self.data["budgets"]:
            return {"status": "no_budget"}
        
        budget = self.data["budgets"][model]
        analysis = self.analyze_current_session()
        
        daily_spent = analysis["predictions"]["estimated_daily_cost"]
        
        daily_remaining = budget["daily_limit"] - daily_spent
        daily_percent = (daily_spent / budget["daily_limit"]) * 100 if budget["daily_limit"] > 0 else 0
        
        return {
            "budget": budget,
            "daily_spent": round(daily_spent, 2),
            "daily_remaining": round(daily_remaining, 2),
            "daily_percent": round(daily_percent, 1),
            "status": "ok" if daily_percent < 80 else "warning" if daily_percent < 100 else "exceeded"
        }
    
    def generate_report(self):
        """生成報告"""
        analysis = self.analyze_current_session()
        
        print("\n" + "="*60)
        print("📊 Token 使用量分析報告")
        print("="*60)
        
        # 當前會話
        print(f"\n🔵 當前會話:")
        print(f"   輸入: {analysis['current']['input_tokens']:,} tokens")
        print(f"   輸出: {analysis['current']['output_tokens']:,} tokens")
        print(f"   快取: {analysis['current']['cached_tokens']:,} tokens")
        print(f"   上下文: {analysis['current']['context_used']:,}/{analysis['current']['context_limit']:,} ({analysis['current']['context_used']/analysis['current']['context_limit']*100:.1f}%)")
        print(f"   時長: {analysis['current']['duration_minutes']} 分鐘")
        
        # 成本
        print(f"\n💰 成本分析:")
        print(f"   輸入成本: ${analysis['cost']['input_cost']}")
        print(f"   輸出成本: ${analysis['cost']['output_cost']}")
        print(f"   總成本: ${analysis['cost']['total_cost']}")
        
        # 效率
        print(f"\n⚡ 效率指標:")
        print(f"   快取命中率: {analysis['efficiency']}%")
        
        # 預測
        pred = analysis["predictions"]
        print(f"\n📈 預測:")
        print(f"   每分鐘: {pred['tokens_per_minute']:,} tokens")
        print(f"   每小時: {pred['tokens_per_hour']:,} tokens")
        print(f"   每日: {pred['tokens_per_day']:,} tokens")
        print(f"   預估每日成本: ${pred['estimated_daily_cost']}")
        print(f"   預估每月成本: ${pred['estimated_monthly_cost']}")
        
        # 預算檢查
        print(f"\n💵 預算狀態:")
        budget_status = self.check_budget()
        if budget_status["status"] != "no_budget":
            emoji = "✅" if budget_status["status"] == "ok" else "⚠️" if budget_status["status"] == "warning" else "❌"
            print(f"   {emoji} 每日: ${budget_status['daily_spent']}/${budget_status['budget']['daily_limit']} ({budget_status['daily_percent']}%)")
        else:
            print(f"   ⚠️ 未設定預算")
        
        print("\n" + "="*60)
        
        return analysis

if __name__ == "__main__":
    analyzer = TokenAnalyzer()
    
    # 設定預算
    analyzer.set_budget("minimax", daily_limit=50, monthly_limit=1500)
    
    # 生成報告
    analyzer.generate_report()
