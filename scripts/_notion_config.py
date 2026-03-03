#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion 共用配置模組 - 從 ~/.openclaw/.env 讀取 API Key
所有 Notion 腳本 import 此模組即可
"""
import os

_ENV_FILE = os.path.expanduser("~/.openclaw/.env")

def _load_env():
    if os.path.exists(_ENV_FILE):
        with open(_ENV_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

_load_env()

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
NOTION_DATABASES = {
    "success":  os.environ.get("NOTION_DB_SUCCESS",  "315a1238-f49d-8149-b67d-f138cc7c7f7c"),
    "error":    os.environ.get("NOTION_DB_ERROR",    "315a1238-f49d-81ef-be80-c632e0b5e493"),
    "learning": os.environ.get("NOTION_DB_LEARNING", "30aa1238-f49d-817c-8163-dd76d1309240"),
    "daily":    os.environ.get("NOTION_DB_DAILY",    "30aa1238-f49d-8136-a813-fb759eb30e47"),
    "members":  os.environ.get("NOTION_DB_MEMBERS",  "302a1238-f49d-80cc-ba55-f83d5704bdb8"),
}
