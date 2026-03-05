---
name: article-deploy-hook
description: |
  文章部署鉤子。當需要自動將生成的文章部署到 GitHub 網站時觸發。
  會 spawn Claude CLI 執行 git commit + push。
metadata: {
  "openclaw": { "emoji": "📤", "requires": { "anyTools": ["sessions_spawn", "exec"] } }
}
---

# Article Deploy Hook

## 功能
- 偵測新生成的文章
- Spawn Claude CLI 執行 GitHub 部署
- 自動 commit + push

## 觸發條件
- 文章生成完成後
- 手動觸發

## 使用方式

```bash
# 部署最新文章
~/.openclaw/workspace/scripts/article-deploy.sh
```

## 流程
1. 檢查 articles/ 目錄
2. 識別未部署的文章
3. Spawn Claude CLI 執行部署
4. 回報結果

## Claude CLI 任務
```
cd ~/.openclaw/workspace
git add articles/
git commit -m "feat: 新增文章 $(date +%Y-%m-%d)"
git push origin main
```

## Cron
30 9 * * * (文章生成後執行)
