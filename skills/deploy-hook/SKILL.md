---
name: deploy-hook
description: |
  部署鉤子。當需要發布網站到 GitHub Pages 時觸發。
  條件：質量檢查通過後執行。
metadata:
  {
    "openclaw": { "emoji": "🚀", "requires": { "anyTools": ["exec", "message"] } },
  }
---

# Deploy Hook

## 功能
- 清理舊 HTML
- 生成新 HTML
- Git commit
- Git push

## 使用方式

```bash
# 手動部署
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py deploy
```

## 流程
1. 讀取 content/*.md
2. 轉換為 HTML
3. 生成 index.html
4. git add → commit → push

## Cron
0 9 * * *

## 觸發條件
- 質量檢查 ≥ 70 分
- 或手動觸發
