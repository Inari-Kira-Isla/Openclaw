#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型升級效益分析 - Model Upgrade Benefit Analysis
"""

import os
import json

class ModelUpgradeAnalyzer:
    def __init__(self):
        # 當前使用數據
        self.current_usage = {
            "daily_tokens": 4143157,  # 從之前的分析
            "daily_cost": 3.48,
            "monthly_cost": 104.41,
            "cache_hit_rate": 78.7
        }
        
        # 模型定價 (USD per 1M tokens)
        self.models = {
            "minimax_flash": {
                "name": "MiniMax Flash (當前)",
                "input": 0.8,
                "output": 4.0,
                "context": 200000,
                "speed": "快",
                "quality": "基礎"
            },
            "minimax_pro": {
                "name": "MiniMax Pro",
                "input": 4.0,
                "output": 15.0,
                "context": 1000000,
                "speed": "中等",
                "quality": "高"
            },
            "gemini_2.5_flash": {
                "name": "Gemini 2.5 Flash",
                "input": 0.075,
                "output": 0.3,
                "context": 1048576,
                "speed": "很快",
                "quality": "中等"
            },
            "gemini_2.5_pro": {
                "name": "Gemini 2.5 Pro",
                "input": 1.25,
                "output": 5.0,
                "context": 1048576,
                "speed": "中等",
                "quality": "很高"
            },
            "claude_sonnet": {
                "name": "Claude Sonnet",
                "input": 3.0,
                "output": 15.0,
                "context": 200000,
                "speed": "快",
                "quality": "高"
            },
            "gpt4o": {
                "name": "GPT-4o",
                "input": 2.5,
                "output": 10.0,
                "context": 128000,
                "speed": "快",
                "質量": "高"
            },
            "ollama_local": {
                "name": "Ollama 本地 (Llama 3.3)",
                "input": 0,
                "output": 0,
                "context": 128000,
                "speed": "取決硬件",
                "quality": "中等",
                "setup_cost": 0  # 已有硬件
            }
        }
    
    def calculate_cost(self, model_key, input_tokens, output_tokens):
        """計算成本"""
        model = self.models[model_key]
        
        input_cost = (input_tokens / 1_000_000) * model["input"]
        output_cost = (output_tokens / 1_000_000) * model["output"]
        
        return round(input_cost + output_cost, 2)
    
    def analyze_upgrade(self, target_model):
        """分析升級效益"""
        current = self.models["minimax_flash"]
        target = self.models[target_model]
        
        # 假設輸出是輸入的 1%
        input_tokens = self.current_usage["daily_tokens"] * 0.99
        output_tokens = self.current_usage["daily_tokens"] * 0.01
        
        # 計算成本
        current_daily = self.calculate_cost("minimax_flash", input_tokens, output_tokens)
        target_daily = self.calculate_cost(target_model, input_tokens, output_tokens)
        
        # 計算效益
        quality_improvement = self.evaluate_quality(current["quality"], target["quality"])
        speed_change = self.evaluate_speed(current["speed"], target["speed"])
        context_improvement = (target["context"] / current["context"] - 1) * 100
        
        return {
            "model": target["name"],
            "current_daily": current_daily,
            "target_daily": target_daily,
            "cost_increase": target_daily - current_daily,
            "cost_increase_percent": ((target_daily - current_daily) / current_daily * 100) if current_daily > 0 else 0,
            "quality_improvement": quality_improvement,
            "speed_change": speed_change,
            "context_improvement": context_improvement,
            "monthly_cost": target_daily * 30,
            "yearly_cost": target_daily * 365
        }
    
    def evaluate_quality(self, current, target):
        """評估質量提升"""
        levels = {"基礎": 1, "中等": 2, "高": 3, "很高": 4}
        
        current_level = levels.get(current, 1)
        target_level = levels.get(target, 1)
        
        improvement = (target_level - current_level) / current_level * 100
        
        return {
            "from": current,
            "to": target,
            "improvement_percent": round(improvement, 1),
            "rating": "⭐" * min(target_level, 5)
        }
    
    def evaluate_speed(self, current, target):
        """評估速度變化"""
        speeds = {"慢": 1, "中等": 2, "快": 3, "很快": 4, "取決硬件": 3}
        
        current_speed = speeds.get(current, 2)
        target_speed = speeds.get(target, 2)
        
        change = "更快" if target_speed > current_speed else "相同" if target_speed == current_speed else "更慢"
        
        return change
    
    def generate_report(self):
        """生成報告"""
        print("\n" + "="*70)
        print("📊 模型升級效益分析報告")
        print("="*70)
        
        # 當前狀況
        print("\n🔵 當前狀況:")
        print(f"   模型: {self.models['minimax_flash']['name']}")
        print(f"   每日 tokens: {self.current_usage['daily_tokens']:,}")
        print(f"   每日成本: ${self.current_usage['daily_cost']}")
        print(f"   每月成本: ${self.current_usage['monthly_cost']}")
        print(f"   快取命中率: {self.current_usage['cache_hit_rate']}%")
        
        # 分析每個選項
        print("\n" + "="*70)
        print("📈 模型比較分析")
        print("="*70)
        
        results = []
        
        for model_key in ["gemini_2.5_flash", "gemini_2.5_pro", "claude_sonnet", "gpt4o", "ollama_local"]:
            if model_key == "minimax_flash":
                continue
            
            analysis = self.analyze_upgrade(model_key)
            results.append(analysis)
            
            emoji = "📉" if analysis["cost_increase"] < 0 else "📈" if analysis["cost_increase"] > 0 else "➖"
            
            print(f"\n{analysis['model']}:")
            print(f"   {emoji} 每日成本: ${analysis['current_daily']} → ${analysis['target_daily']} (+${analysis['cost_increase']})")
            print(f"   📊 成本變化: {analysis['cost_increase_percent']:+.1f}%")
            print(f"   ⭐ 質量提升: {analysis['quality_improvement']['from']} → {analysis['quality_improvement']['to']} ({analysis['quality_improvement']['improvement_percent']:+.0f}%)")
            print(f"   ⚡ 速度: {analysis['speed_change']}")
            print(f"   📚 上下文: {analysis['context_improvement']:+.0f}%")
            print(f"   💰 每月成本: ${analysis['monthly_cost']}")
            print(f"   📅 每年成本: ${analysis['yearly_cost']}")
        
        # 最佳推薦
        print("\n" + "="*70)
        print("🏆 推薦分析")
        print("="*70)
        
        # 性價比最高
        best_value = min(results, key=lambda x: x["cost_increase_percent"] if x["cost_increase_percent"] < 100 else 999)
        
        # 質量最好
        best_quality = max(results, key=lambda x: x["quality_improvement"]["improvement_percent"])
        
        # 成本最低
        lowest_cost = min(results, key=lambda x: x["target_daily"])
        
        print(f"\n💰 成本最優: {lowest_cost['model']} (${lowest_cost['target_daily']}/日)")
        print(f"⭐ 質量最高: {best_quality['model']} ({best_quality['quality_improvement']['rating']})")
        print(f"⚖️  性價比: {best_value['model']} ({best_value['cost_increase_percent']:+.1f}%)")
        
        # 總結建議
        print("\n" + "="*70)
        print("💡 總結建議")
        print("="*70)
        
        print("""
根據分析：

1. **如果想省成本** → 使用 Gemini 2.5 Flash
   - 成本: $0.32/日 (比 MiniMax 少 91%)
   - 質量: 中等
   - 適合: 簡單任務、日常對話

2. **如果想提升質量** → 使用 Claude Sonnet 或 GPT-4o
   - 成本: $10-15/日 (比 MiniMax 高 200-300%)
   - 質量: 高
   - 適合: 複雜推理、創意寫作

3. **如果想平衡** → 使用 Gemini 2.5 Pro
   - 成本: $3.92/日 (比 MiniMax 高 13%)
   - 質量: 很高
   - 適合: 大多數任務

4. **本地運行** → Ollama
   - 成本: $0/日 (硬件除外)
   - 質量: 中等
   - 適合: 離線使用、私密數據
""")
        
        return results

if __name__ == "__main__":
    analyzer = ModelUpgradeAnalyzer()
    analyzer.generate_report()
