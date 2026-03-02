#!/usr/bin/env python3
"""
AEO Quality Checker
================
檢查文章質量是否符合標準

標準：~/.openclaw/workspace/memory/aeo_quality/quality-check.json
"""

import json
import re
import sys
from pathlib import Path

# 標準配置
CONFIG_PATH = Path("/Users/ki/.openclaw/workspace/memory/aeo_quality/quality-check.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def check_article(filepath):
    """檢查單篇文章"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    score = 0
    details = []
    
    # 1. 字數檢查
    word_count = len(content)
    if word_count >= 1500:
        wc_score = 20
    elif word_count >= 1000:
        wc_score = 15
    else:
        wc_score = 5
    score += wc_score
    details.append(f"字數: {word_count} → {wc_score}/20")
    
    # 2. 結構檢查
    h1_count = len(re.findall(r'^#\s+', content, re.MULTILINE))
    h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
    h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
    
    struct_score = 0
    if h1_count >= 1: struct_score += 10
    if h2_count >= 3: struct_score += 10
    if h3_count >= 2: struct_score += 10
    score += struct_score
    details.append(f"結構 (H1:{h1_count}, H2:{h2_count}, H3:{h3_count}) → {struct_score}/30")
    
    # 3. 代碼範例
    code_blocks = len(re.findall(r'```\w+', content))
    code_score = min(code_blocks * 10, 20)
    score += code_score
    details.append(f"代碼範例: {code_blocks} → {code_score}/20")
    
    # 4. SEO 檢查
    seo_score = 0
    if 'title:' in content: seo_score += 5
    if 'description:' in content: seo_score += 5
    if 'tags:' in content: seo_score += 5
    if 'keywords:' in content: seo_score += 5
    score += seo_score
    details.append(f"SEO → {seo_score}/20")
    
    # 5. 內容深度
    depth_score = 10 if word_count > 1500 else 5
    score += depth_score
    details.append(f"深度 → {depth_score}/10")
    
    return score, details

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quality_check.py <article.md>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    score, details = check_article(filepath)
    
    print(f"\n📊 質量檢查: {filepath}")
    print("=" * 40)
    for d in details:
        print(f"   {d}")
    print(f"\n🎯 總分: {score}/100")
    
    if score >= 90:
        print("✅ 評級: Excellent")
    elif score >= 70:
        print("⚠️ 評級: Good (通過)")
    else:
        print("❌ 評級: Poor (未通過)")
    
    return 0 if score >= 70 else 1

if __name__ == "__main__":
    sys.exit(main())
