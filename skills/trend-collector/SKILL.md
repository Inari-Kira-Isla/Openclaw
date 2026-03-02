---
name: trend-collector
description: |
  趨勢收集鉤子。當需要抓取熱門 AI/Tech 話題時觸發。
  數據來源：Hacker News、Reddit、Perplexity。
metadata:
  {
    "openclaw": { "emoji": "📈", "requires": { "anyTools": ["web_search", "exec"] } },
  }
---

# Trend Collector Hook

## 功能
- 抓取 Hacker News 熱門
- 搜尋 Reddit AI 話題
- 查詢 Perplexity 趨勢

## 使用方式

```bash
python3 ~/.openclaw/workspace/scripts/trend_collector.py
```

## 輸出
- topics.json

## Cron
0 6 * * *
