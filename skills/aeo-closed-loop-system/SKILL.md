---
name: aeo-closed-loop-system
description: |
  AEO 內容閉環系統。當需要自動生成、檢查、發布 AI 教學內容時觸發。
  工作流：(1) 趨勢收集 (2) 文章生成 (3) 質量檢查 (4) 技術審計 (5) 部署發布。
metadata:
  {
    "openclaw": { "emoji": "🔄", "requires": { "anyTools": ["exec", "message", "web_search"] } },
  }
---

# AEO Closed Loop System

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                  AEO 內容閉環系統                           │
└──────────────────────┬────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ 趨勢收集  │    │ 文章生成 │    │ 質量檢查 │
│  (Cron) │───▶│ (Team)  │───▶│(Cynthia)│
└──────────┘    └──────────┘    └──────────┘
       │                           │
       │                           ▼
       │                   ┌──────────┐
       │                   │ 質量閾值 │
       │                   │ < 70 分  │
       │                   └────┬─────┘
       │                        │
       ▼                        ▼
┌──────────┐            ┌──────────┐
│ 技術審計 │            │ 部署發布 │
│ (Slime) │            │  (Team) │
└──────────┘            └──────────┘
```

## 步驟說明

### 1. 趨勢收集 (Trend Collector)
- **負責**: Cron
- **任務**: 抓取 HN/Reddit/Perplexity 熱門 AI/Tech 話題
- **輸出**: topics.json

### 2. 文章生成 (Article Generator)
- **負責**: Team
- **任務**: 根據模板生成高質量文章
- **輸入**: topics.json + content-prompt-v2.md
- **輸出**: articles/

### 3. 質量檢查 (Quality Checker)
- **負責**: Cynthia
- **任務**: 執行 quality-check.mjs 驗證質量
- **閾值**: < 70 分 → 阻止發布

### 4. 技術審計 (Technical Audit)
- **負責**: 史萊姆
- **任務**: Lighthouse 測試、連結檢查

### 5. 部署發布 (Deploy)
- **負責**: Team
- **任務**: git commit → push → GitHub Pages

## Hooks 配置

### Trend Collector Hook
```yaml
name: trend-collector
trigger: "0 6 * * *"  # 每天早上 6 點
action: web_search
```

### Article Generator Hook
```yaml
name: article-generator
trigger: "after:trend-collector"
action: exec
script: "python3 aeo_content.py"
```

### Quality Checker Hook
```yaml
name: quality-checker
trigger: "after:article-generator"
action: exec
script: "python3 seo_audit.py audit"
threshold: 70
```

### Deploy Hook
```yaml
name: aeo-deploy
trigger: "after:quality-checker + threshold_passed"
action: git_push
```

## Cron 排程

| 時間 | 任務 |
|------|------|
| 06:00 | 趨勢收集 |
| 07:00 | 文章生成 |
| 08:00 | 質量檢查 |
| 09:00 | 部署發布 |
| 每週 | 技術審計 |

## 品質閾值

| 分數 | 動作 |
|------|------|
| ≥ 90 | 立即發布 |
| 70-89 | 審核後發布 |
| < 70 | 阻止發布 |

## 自動化狀態

| 步驟 | 狀態 | 負責 Bot |
|------|------|----------|
| 趨勢收集 | ✅ | Cron |
| 文章生成 | ⏳ | Team |
| 質量檢查 | ✅ | Cynthia |
| 技術審計 | ⏳ | 史萊姆 |
| 部署發布 | ⏳ | Team |
