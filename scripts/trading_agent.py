#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trading Agent - 報價/採購自動化 Agent
自動生成報價、採購追蹤、價格監控
"""

import os
import json
import subprocess
from datetime import datetime

class TradingAgent:
    def __init__(self):
        self.data_path = os.path.expanduser("~/.openclaw/workspace/memory/trading_data.json")
        self.quotes_path = os.path.expanduser("~/.openclaw/workspace/memory/quotes.json")
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.products_data = json.load(f)
        else:
            self.products_data = {"products": [], "suppliers": [], "price_history": []}
        
        if os.path.exists(self.quotes_path):
            with open(self.quotes_path, "r") as f:
                self.quotes_data = json.load(f)
        else:
            self.quotes_data = {"quotes": []}
    
    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.products_data if hasattr(self, 'products_data') else {}, f, indent=2)
        with open(self.quotes_path, "w") as f:
            json.dump(self.quotes_data if hasattr(self, 'quotes_data') else {}, f, indent=2)
    
    def add_product(self, name, category, unit_price, supplier=""):
        """新增產品"""
        product = {
            "id": f"prod_{len(self.products_data.get('products', [])) + 1}",
            "name": name,
            "category": category,
            "unit_price": unit_price,
            "supplier": supplier,
            "created_at": datetime.now().isoformat()
        }
        
        if "products" not in self.products_data:
            self.products_data["products"] = []
        self.products_data["products"].append(product)
        
        self.save_data()
        
        return product
    
    def add_supplier(self, name, contact, products=None):
        """新增供應商"""
        supplier = {
            "id": f"sup_{len(self.products_data.get('suppliers', [])) + 1}",
            "name": name,
            "contact": contact,
            "products": products or [],
            "created_at": datetime.now().isoformat()
        }
        
        if "suppliers" not in self.products_data:
            self.products_data["suppliers"] = []
        self.products_data["suppliers"].append(supplier)
        
        self.save_data()
        
        return supplier
    
    def generate_quote(self, customer_name, items, discount=0):
        """生成報價單"""
        # 計算總價
        total = 0
        quote_items = []
        
        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)
            
            # 找產品
            product = None
            for p in self.products_data.get("products", []):
                if p["id"] == product_id:
                    product = p
                    break
            
            if product:
                line_total = product["unit_price"] * quantity * (1 - discount/100)
                total += line_total
                
                quote_items.append({
                    "product": product["name"],
                    "quantity": quantity,
                    "unit_price": product["unit_price"],
                    "discount": discount,
                    "line_total": line_total
                })
        
        quote = {
            "id": f"quote_{len(self.quotes_data.get('quotes', [])) + 1}",
            "customer": customer_name,
            "items": quote_items,
            "subtotal": total,
            "discount": discount,
            "total": total,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        if "quotes" not in self.quotes_data:
            self.quotes_data["quotes"] = []
        self.quotes_data["quotes"].append(quote)
        
        self.save_data()
        
        return quote
    
    def update_price(self, product_id, new_price):
        """更新價格"""
        for product in self.products_data.get("products", []):
            if product["id"] == product_id:
                old_price = product["unit_price"]
                product["unit_price"] = new_price
                product["updated_at"] = datetime.now().isoformat()
                
                # 記錄歷史
                if "price_history" not in self.products_data:
                    self.products_data["price_history"] = []
                
                self.products_data["price_history"].append({
                    "product_id": product_id,
                    "old_price": old_price,
                    "new_price": new_price,
                    "timestamp": datetime.now().isoformat()
                })
                
                self.save_data()
                
                return {
                    "product": product["name"],
                    "old_price": old_price,
                    "new_price": new_price,
                    "change": ((new_price - old_price) / old_price * 100)
                }
        
        return None
    
    def check_price_alert(self, product_id, threshold_percent=10):
        """價格預警"""
        history = [h for h in self.products_data.get("price_history", []) 
                  if h["product_id"] == product_id]
        
        if len(history) < 2:
            return {"status": "no_history"}
        
        # 計算變化
        last = history[-1]
        change = ((last["new_price"] - last["old_price"]) / last["old_price"]) * 100
        
        if abs(change) >= threshold_percent:
            return {
                "status": "alert",
                "product_id": product_id,
                "change_percent": change,
                "direction": "up" if change > 0 else "down"
            }
        
        return {"status": "normal", "change_percent": change}
    
    def get_pending_quotes(self):
        """獲取待處理報價"""
        return [q for q in self.quotes_data.get("quotes", []) if q["status"] == "pending"]
    
    def send_quote(self, quote_id):
        """發送報價"""
        for quote in self.quotes_data.get("quotes", []):
            if quote["id"] == quote_id:
                quote["status"] = "sent"
                quote["sent_at"] = datetime.now().isoformat()
                self.save_data()
                return quote
        
        return None
    
    def run_monitoring(self):
        """運行監控"""
        print("\n🔔 報價/採購監控")
        print("="*40)
        
        # 產品數量
        product_count = len(self.products_data.get("products", []))
        supplier_count = len(self.products_data.get("suppliers", []))
        quote_count = len(self.quotes_data.get("quotes", []))
        
        print(f"📦 產品: {product_count}")
        print(f"🏭 供應商: {supplier_count}")
        print(f"📄 報價單: {quote_count}")
        
        # 待處理報價
        pending = self.get_pending_quotes()
        if pending:
            print(f"\n⏳ 待處理報價: {len(pending)}")
            for p in pending[:3]:
                print(f"   - {p['customer']}: ${p['total']}")
        
        # 價格預警
        print("\n💰 價格變動:")
        for product in self.products_data.get("products", [])[:5]:
            alert = self.check_price_alert(product["id"])
            if alert.get("status") == "alert":
                emoji = "🔺" if alert["direction"] == "up" else "🔻"
                print(f"   {emoji} {product['name']}: {alert['change_percent']:.1f}%")
        
        return {
            "products": product_count,
            "suppliers": supplier_count,
            "quotes": quote_count,
            "pending": len(pending)
        }

if __name__ == "__main__":
    agent = TradingAgent()
    
    # 添加測試數據
    agent.add_product("北海道海膽", "海產", 500, "東京水產")
    agent.add_product("龍蝦", "海產", 800, "悉尼海產")
    agent.add_product("帝王蟹", "海產", 1200, "俄羅斯漁業")
    
    agent.add_supplier("東京水產", "info@tokyo-fish.jp", ["北海道海膽"])
    agent.add_supplier("悉尼海產", "sales@sydney-seafood.com", ["龍蝦"])
    
    # 生成報價
    quote = agent.generate_quote("王老闆", [
        {"product_id": "prod_1", "quantity": 10},
        {"product_id": "prod_2", "quantity": 5}
    ], discount=10)
    
    # 運行監控
    agent.run_monitoring()
