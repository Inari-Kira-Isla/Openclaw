---
name: quality-checker-hook
description: |
  質量檢查鉤子。當需要驗證文章質量時觸發。
  檢查：SEO、AEO、結構、代碼範例。
metadata:
  {
    "openclaw": { "emoji": "🔍", "requires": { "anyTools": ["exec", "read"] } },
  }
---

# Quality Checker Hook

## 功能
- SEO 檢查
- AEO 結構驗證
- 代碼範例檢查
- 字數統計

## 使用方式

```bash
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py audit
```

## 質量閾值

| 分數 | 動作 |
|------|------|
| ≥ 90 | 通過 |
| 70-89 | 警告 |
| < 70 | 阻止 |

## Cron
0 8 * * *
