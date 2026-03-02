---
name: article-generator-hook
description: |
  文章生成鉤子。當需要根據趨勢生成 AI 教學文章時觸發。
  輸入：topics.json
  輸出：高質量 Markdown 文章
metadata:
  {
    "openclaw": { "emoji": "📝", "requires": { "anyTools": ["exec", "write"] } },
  }
---

# Article Generator Hook

## 功能
- 讀取趨勢 topics.json
- 根據模板生成文章
- 品質檢查

## 使用方式

```bash
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate
```

## 品質標準
- 字數：1000+
- 結構：H1 + H2 + H3
- 代碼範例：至少 1 個

## Cron
0 7 * * *
