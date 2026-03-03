---
name: cloudpipe-seo-aeo-loop
description: |
  CloudPipe SEO/AEO 排名優化閉環系統。每日監控搜尋引擎索引、驗證結構化資料、分析 AI 爬蟲行為。
  閉環：(1) 收集 (2) 分析 (3) 自動優化 (4) 驗證 (5) 學習 (6) 報告
  每日執行 + 每週深度分析報告。
metadata:
  {
    "openclaw": { "emoji": "🔄", "requires": { "anyTools": ["exec", "read", "write", "message"] } },
  }
---

# CloudPipe SEO/AEO 優化閉環

持續優化搜尋引擎與 AI 引擎排名的閉環系統。

## 閉環流程

```
收集 → 分析 → 優化 → 驗證 → 學習 → 報告
  │       │       │       │       │       │
  │       │       │       │       │       └─ Telegram 日報/週報
  │       │       │       │       └─ 記錄趨勢，調整策略
  │       │       │       └─ 重新抓取確認無退化
  │       │       └─ 自動更新 sitemap、info.json
  │       └─ 100 分制評分
  └─ 抓取 HTML、JSON-LD、索引狀態
```

## 評分（100 分制）

| 類別 | 權重 | 檢查內容 |
|------|------|----------|
| Meta Tags | 20 | title, description, keywords, og:* |
| JSON-LD App | 25 | SoftwareApplication 完整性 |
| JSON-LD FAQ | 20 | FAQPage 結構 |
| Technical SEO | 15 | robots.txt, sitemap, info.json |
| AI 可讀性 | 10 | 隱藏資料區塊 |
| 效能 | 10 | 回應時間 |

## 使用方式

```bash
# 每日閉環
python3 ~/.openclaw/workspace/scripts/cloudpipe/seo_aeo_optimizer.py daily

# 每週深度分析
python3 ~/.openclaw/workspace/scripts/cloudpipe/seo_aeo_optimizer.py weekly
```

## 排程

```
0 9 * * *    (每日 09:00 PST)
0 10 * * 1   (每週一 10:00 PST — 深度分析)
```

## 安全自動優化（不需人工）

- 更新 sitemap.xml lastmod
- 更新 api/info.json last_updated
- 添加缺失的 datePublished/dateModified

## 需人工確認

- 修改 title 或 meta description
- 增減 FAQ 條目
- 修改定價資訊

## 學習機制

每次記錄：score, breakdown, changes, recommendations, trend
週報分析：7 天趨勢、AI 爬蟲模式、優化效果、策略建議

## 日誌

- `~/.openclaw/workspace/logs/cloudpipe/seo_aeo.jsonl`
