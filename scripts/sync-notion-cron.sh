#!/bin/bash
# Notion to ChromaDB Sync Cron Job
# Run at 18:00 daily

source /Users/ki/Desktop/chromadb-env/bin/activate
python /Users/ki/.openclaw/workspace/scripts/notion_chroma_sync.py >> /Users/ki/.openclaw/logs/notion-sync.log 2>&1
