#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Agent - 郵件自動化 Agent
Gmail 整合、郵件分類、自动回覆
"""

import os
import json
import subprocess
from datetime import datetime

class EmailAgent:
    def __init__(self):
        self.data_path = os.path.expanduser("~/.openclaw/workspace/memory/email_data.json")
        self.templates_path = os.path.expanduser("~/.openclaw/workspace/memory/email_templates.json")
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.emails_data = json.load(f)
        else:
            self.emails_data = {"emails": [], "contacts": []}
        
        if os.path.exists(self.templates_path):
            with open(self.templates_path, "r") as f:
                self.templates_data = json.load(f)
        else:
            self.templates_data = {"templates": []}
    
    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.emails_data if hasattr(self, 'emails_data') else {}, f, indent=2)
        with open(self.templates_path, "w") as f:
            json.dump(self.templates_data if hasattr(self, 'templates_data') else {}, f, indent=2)
    
    def add_template(self, name, subject, body, trigger_keywords=None):
        """新增郵件模板"""
        template = {
            "id": f"tpl_{len(self.templates_data.get('templates', [])) + 1}",
            "name": name,
            "subject": subject,
            "body": body,
            "trigger_keywords": trigger_keywords or [],
            "created_at": datetime.now().isoformat()
        }
        
        if "templates" not in self.templates_data:
            self.templates_data["templates"] = []
        self.templates_data["templates"].append(template)
        
        self.save_data()
        
        return template
    
    def classify_email(self, subject, body):
        """郵件分類"""
        text = (subject + " " + body).lower()
        
        # 分類規則
        rules = {
            "urgent": ["緊急", "urgent", "asap", "立即"],
            "inquiry": ["詢問", "問", "query", "怎麼"],
            "order": ["訂", "order", "購買", "報價"],
            "complaint": ["投訴", "complaint", "不滿", "問題"],
            "newsletter": ["newsletter", "更新", "電子報"]
        }
        
        for category, keywords in rules.items():
            if any(k in text for k in keywords):
                return category
        
        return "general"
    
    def find_template(self, subject, body):
        """尋找匹配模板"""
        classification = self.classify_email(subject, body)
        
        for template in self.templates_data.get("templates", []):
            if template["trigger_keywords"]:
                for keyword in template["trigger_keywords"]:
                    if keyword.lower() in (subject + body).lower():
                        return template
        
        return None
    
    def generate_reply(self, subject, body, tone="professional"):
        """生成回覆"""
        # 根據分類生成回覆
        classification = self.classify_email(subject, body)
        
        replies = {
            "urgent": f"您好，感謝您聯繫。我已收到您的緊急請求，會盡快處理。",
            "inquiry": f"您好，感謝您的詢問。以下是您的問題的回覆...",
            "order": f"您好，感謝您的訂單。我們會盡快處理。",
            "complaint": f"您好，對於造成的不便我們深感抱歉。我們會立即處理。",
            "newsletter": f"感謝您的關注！",
            "general": f"您好，感謝您的來信。我會盡快回覆。"
        }
        
        return replies.get(classification, replies["general"])
    
    def send_email(self, to, subject, body):
        """發送郵件"""
        # 這裡調用 Gmail API
        email = {
            "id": f"email_{len(self.emails_data.get('emails', [])) + 1}",
            "to": to,
            "subject": subject,
            "body": body,
            "sent_at": datetime.now().isoformat(),
            "status": "sent"
        }
        
        if "emails" not in self.emails_data:
            self.emails_data["emails"] = []
        self.emails_data["emails"].append(email)
        
        self.save_data()
        
        return email
    
    def get_draft_count(self):
        """獲取草稿數量"""
        return len([e for e in self.emails_data.get("emails", []) if e.get("status") == "draft"])
    
    def run_analysis(self):
        """運行分析"""
        print("\n📧 Email Agent 分析")
        print("="*40)
        
        # 統計
        total = len(self.emails_data.get("emails", []))
        templates = len(self.templates_data.get("templates", []))
        
        print(f"📨 總郵件: {total}")
        print(f"📝 模板數: {templates}")
        
        # 模板列表
        print(f"\n📋 可用模板:")
        for t in self.templates_data.get("templates", [])[:5]:
            print(f"   - {t['name']}")
        
        return {
            "emails": total,
            "templates": templates
        }

if __name__ == "__main__":
    agent = EmailAgent()
    
    # 添加模板
    agent.add_template(
        "詢問回覆",
        "感謝您的詢問",
        "您好，感謝您的詢問。我們會盡快回覆您。",
        ["問", "query", "怎麼"]
    )
    
    agent.add_template(
        "訂單確認",
        "訂單已確認",
        "您好，您的訂單已確認，我們會盡快處理。",
        ["訂", "order", "購買"]
    )
    
    agent.add_template(
        "報價請求",
        "報價單已發送",
        "您好，感謝您的興趣。請查閱附件中的報價單。",
        ["報價", "quote", "price"]
    )
    
    # 測試分類
    test_email = "你好，我想詢問海膽既價格"
    category = agent.classify_email(test_email, "")
    reply = agent.generate_reply(test_email, "")
    
    print(f"\n📧 測試:")
    print(f"   輸入: {test_email}")
    print(f"   分類: {category}")
    print(f"   回覆: {reply}")
    
    # 運行分析
    agent.run_analysis()
