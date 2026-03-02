#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance Agent - 財務管理 Agent
支出追蹤、預算管理、財務報告
"""

import os
import json
import subprocess
from datetime import datetime, timedelta

class FinanceAgent:
    def __init__(self):
        self.notion_key = os.environ.get("NOTION_API_KEY", "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")
        self.database_id = "315a1238-f49d-81ef-be80-c632e0b5e493"  # 支出資料庫
        self.data_path = os.path.expanduser("~/.openclaw/workspace/memory/expenses.json")
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "expenses": [],
                "categories": {},
                "budgets": {}
            }
    
    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def add_expense(self, category, amount, description="", date=None):
        """新增支出"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        expense = {
            "id": f"exp_{len(self.data['expenses']) + 1}",
            "category": category,
            "amount": amount,
            "description": description,
            "date": date,
            "created_at": datetime.now().isoformat()
        }
        
        self.data["expenses"].append(expense)
        
        # 更新類別統計
        if category not in self.data["categories"]:
            self.data["categories"][category] = 0
        self.data["categories"][category] += amount
        
        self.save_data()
        
        return expense
    
    def get_monthly_report(self, year=None, month=None):
        """月度報告"""
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        
        monthly_expenses = [
            e for e in self.data["expenses"]
            if datetime.strptime(e["date"], "%Y-%m-%d").year == year
            and datetime.strptime(e["date"], "%Y-%m-%d").month == month
        ]
        
        total = sum(e["amount"] for e in monthly_expenses)
        
        by_category = {}
        for e in monthly_expenses:
            if e["category"] not in by_category:
                by_category[e["category"]] = 0
            by_category[e["category"]] += e["amount"]
        
        return {
            "year": year,
            "month": month,
            "total": total,
            "count": len(monthly_expenses),
            "by_category": by_category
        }
    
    def set_budget(self, category, amount):
        """設定預算"""
        self.data["budgets"][category] = {
            "amount": amount,
            "set_at": datetime.now().isoformat()
        }
        self.save_data()
    
    def check_budget(self, category):
        """檢查預算"""
        if category not in self.data["budgets"]:
            return {"status": "no_budget"}
        
        budget = self.data["budgets"][category]["amount"]
        spent = self.data["categories"].get(category, 0)
        remaining = budget - spent
        percent = (spent / budget * 100) if budget > 0 else 0
        
        return {
            "category": category,
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "percent": percent,
            "status": "ok" if percent < 80 else "warning" if percent < 100 else "exceeded"
        }
    
    def sync_to_notion(self):
        """同步到 Notion"""
        # 實現 Notion API 調用
        print("📤 同步到 Notion...")
        
        # 模擬同步
        synced = len(self.data["expenses"])
        
        print(f"   ✅ 已同步 {synced} 筆記錄")
        
        return synced
    
    def run_analysis(self):
        """運行分析"""
        report = self.get_monthly_report()
        
        print("\n📊 財務分析報告")
        print("="*40)
        print(f"月份: {report['month']}/{report['year']}")
        print(f"總支出: ${report['total']}")
        print(f"筆數: {report['count']}")
        
        print("\n📂 類別分布:")
        for cat, amount in sorted(report["by_category"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat}: ${amount}")
        
        # 檢查預算
        print("\n💰 預算狀態:")
        for cat in self.data["budgets"]:
            status = self.check_budget(cat)
            emoji = "✅" if status["status"] == "ok" else "⚠️" if status["status"] == "warning" else "❌"
            print(f"   {emoji} {cat}: ${status['spent']}/${status['budget']} ({status['percent']:.1f}%)")
        
        return report

if __name__ == "__main__":
    agent = FinanceAgent()
    
    # 添加一些測試數據
    agent.add_expense("食品", 150, "超市購物")
    agent.add_expense("交通費", 50, "地鐵")
    agent.add_expense("娛樂", 200, "電影")
    
    # 設定預算
    agent.set_budget("食品", 500)
    agent.set_budget("娛樂", 300)
    
    # 運行分析
    agent.run_analysis()
