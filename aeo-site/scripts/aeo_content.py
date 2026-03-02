#!/usr/bin/env python3
"""AEO Content Generator V2"""
import sys
from pathlib import Path
from datetime import datetime

SITE_DIR = Path("/Users/ki/.openclaw/workspace/aeo-site")
CONTENT_DIR = SITE_DIR / "content"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

CODE = {
    "python": '''```python
class AITool:
    def __init__(self, name):
        self.name = name
    async def process(self, data):
        return f"[{self.name}] 處理: {data}"
```''',
    "bash": '''```bash
#!/bin/bash
echo "開始安裝..."
pip install -r requirements.txt
echo "完成！"
```''',
    "json": '''```json
{
  "prompt": {
    "role": "專業顧問",
    "task": "分析並提供建議"
  }
}
```''',
    "yaml": '''```yaml
name: 自動化工作流
trigger:
  cron: "0 9 * * 1-5"
steps:
  - name: 獲取數據
```'''
}

def gen(ctype, topic):
    date = datetime.now().strftime("%Y-%m-%d")
    lang = {"system_prompt": "python", "tool_setup": "bash", "prompt_template": "json", "workflow": "yaml"}[ctype]
    
    content = f'''---
title: "{topic}"
type: {ctype}
date: {date}
tags: ["AI", "{topic}", "教學"]
description: "深入了解 {topic} 的完整教學指南"
keywords: ["{topic}", "AI", "教學", "開發"]
---

# {topic}

## 概述

{topic}是現代 AI 應用中非常重要的一個領域。隨著技術的發展，越來越多的開發者和企業開始關注如何有效運用 {topic} 來提升工作效率和創造價值。

本篇文章將深入探討 {topic} 的各個面向，包括基礎概念、安裝設定、實際應用場景以及進階技巧。無論你是初學者還是有經驗的開發者，都能從中找到有價值的資訊。

學習 {topic} 不僅能夠幫助你解決日常工作生活中的問題，還能夠為你的職業發展帶來新的可能性。讓我們一起開始這段學習之旅吧！

## 核心功能

### 1. 專業分析能力
{topic} 具備強大的分析和理解能力，能夠快速理解複雜的問題並提供結構化的解答。這種能力基於大規模語言模型的訓練，使 AI 能夠在多種場景下表現出色。

### 2. 上下文理解
能夠記住對話上下文，理解用戶的真正意圖，無需重複說明背景資訊。這使得交互更加自然流暢，減少了溝通成本。

### 3. 多領域知識
涵蓋科技、商業、創意、教育等多個領域的知識，能夠提供跨學科的綜合建議。

## 安裝與設定

### 環境需求
| 需求 | 最低版本 | 建議版本 |
|------|----------|----------|
| 作業系統 | macOS 10.15 | macOS 12+ |
| 記憶體 | 4GB | 8GB+ |
| 硬碟空間 | 10GB | 50GB+ |

### 安裝步驟

{CODE[lang]}

## 使用技巧

### 明確具體的提問
想要獲得最好的回答，問題要盡量具體明確。避免過於模糊的表述，直接說明你想要什麼。

**範例：**
- ❌ 「幫幫我」
- ✅ 「幫我寫一個 Python 函數，計算列表平均值」

### 提供上下文
在提問時提供足夠的上下文背景，可以幫助 AI 更好地理解你的需求。

### 分步驟處理複雜問題
對於複雜的問題，可以将其拆分成多個小問題，逐步獲得答案。

## 常見問題

### Q: {topic}需要付費嗎？
A: 基礎功能免費使用，進階功能需要訂閱付費方案。

### Q: 支援中文嗎？
A: 是的，完整支援繁體中文和多國語言。

### Q: 數據安全嗎？
A: 所有數據傳輸都使用加密協定，伺服器採用企業級安全標準。

## 相關資源

- [官方文檔](https://example.com/docs)
- [API 參考](https://example.com/api)
- [GitHub](https://github.com/example)

---
由 OpenClaw 自動生成 | 日期：{date}'''
    
    fname = CONTENT_DIR / f"{date}_{topic}.md"
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Generated: {fname}")
    print(f"📝 字數: {len(content)}")

if __name__ == "__main__":
    ctype, topic = "system_prompt", "測試主題"
    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i+1 < len(sys.argv): ctype = sys.argv[i+1]
        if arg == "--topic" and i+1 < len(sys.argv): topic = sys.argv[i+1]
    gen(ctype, topic)
