#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 整合 - Gemini Integration
"""

import os
import json
import requests

API_KEY = "AIzaSyDaWKpOFphXgQahGELLFRqHFk497it0p-U"
MODEL = "gemini-2.5-flash"

def generate(prompt, max_tokens=100):
    """生成內容"""
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.7
        }
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.text}"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Gemini API 整合")
        print("用法: python gemini.py <prompt>")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    result = generate(prompt)
    print(result)
