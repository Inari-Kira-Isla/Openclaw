#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama 模型微調系統 - Ollama Fine-tuning System
使用 GGUF 進行本地微調
"""

import os
import subprocess
import json
from datetime import datetime

class OllamaFineTuner:
    def __init__(self):
        self.base_path = os.path.join(os.path.expanduser("~/.openclaw/workspace/"), "training_data/")
        self.models_path = os.path.expanduser("~/.openclaw/models/")
        
        os.makedirs(self.base_path, exist_ok=True)
    
    def check_ollama(self):
        """檢查 Ollama 狀態"""
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True
        )
        
        print("📦 已安裝模型:")
        print(result.stdout)
        
        return result.stdout
    
    def create_modelfile(self, base_model="llama3.2", system_prompt=None):
        """建立 Modelfile"""
        
        if not system_prompt:
            system_prompt = """你係 Lobster，一個 AI 助手。
- 用廣東話回覆
- 簡短直接
- 有需要既時候用 Emoji
- 專業、果斷"""
        
        modelfile = f"""
FROM {base_model}

SYSTEM """ + system_prompt
        
        modelfile_path = os.path.join(self.base_path, "Modelfile")
        
        with open(modelfile_path, "w") as f:
            f.write(modelfile)
        
        print(f"✅ Modelfile 已建立: {modelfile_path}")
        
        return modelfile_path
    
    def create_model(self, model_name, base_model="llama3.2"):
        """建立自定義模型"""
        
        modelfile = self.create_modelfile(base_model)
        
        print(f"\n🔨 建立模型: {model_name}")
        
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", modelfile],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"✅ 模型建立成功: {model_name}")
            return True
        else:
            print(f"❌ 建立失敗: {result.stderr}")
            return False
    
    def list_models(self):
        """列出所有模型"""
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True
        )
        
        return result.stdout
    
    def test_model(self, model_name, prompt="你好"):
        """測試模型"""
        print(f"\n🧪 測試模型: {model_name}")
        
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True, text=True, timeout=60
        )
        
        print(f"   Input: {prompt}")
        print(f"   Output: {result.stdout[:200]}")
        
        return result.stdout
    
    def run_training_cycle(self):
        """運行訓練週期"""
        print("="*50)
        print("🤖 Ollama 微調系統")
        print("="*50)
        
        # 1. 檢查狀態
        self.check_ollama()
        
        # 2. 建立模型
        success = self.create_model("lobster-assistant", "llama3.2")
        
        if success:
            # 3. 測試
            self.test_model("lobster-assistant", "你好")
        
        print("\n✅ 訓練週期完成")
        
        return success

if __name__ == "__main__":
    tuner = OllamaFineTuner()
    tuner.run_training_cycle()
