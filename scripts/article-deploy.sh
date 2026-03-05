#!/bin/bash
# Article Deploy Hook - 自動部署文章到 GitHub

ARTICLES_DIR="$HOME/.openclaw/workspace/articles"
REPO_DIR="$HOME/.openclaw/workspace"

echo "📤 開始部署文章..."

cd "$REPO_DIR" || exit 1

# 檢查是否有新文章
if [ -z "$(git status --porcelain articles/)" ]; then
    echo "✅ 沒有新文章需要部署"
    exit 0
fi

# Git add + commit + push
git add articles/
git commit -m "feat: 新增文章 $(date +%Y-%m-%d)" || echo "⚠️ 沒有變更需要提交"
git push origin main

echo "✅ 文章部署完成"
