#!/bin/bash
# Article Deploy via Claude CLI - Spawn 版本

ARTICLES_DIR="$HOME/.openclaw/workspace/articles"
REPO_DIR="$HOME/.openclaw/workspace"

echo "🤖 Spawn Claude CLI 部署文章..."

# 檢查是否有新文章
cd "$REPO_DIR" || exit 1
if [ -z "$(git status --porcelain articles/)" ]; then
    echo "✅ 沒有新文章需要部署"
    exit 0
fi

# 使用 claude-cli 執行部署
claude --dangerously-skip-permissions -p "
請執行以下 Git 命令將 articles/ 目錄的變更部署到 GitHub:

cd $REPO_DIR
git add articles/
git commit -m 'feat: 新增文章 $(date +%Y-%m-%d)'
git push origin main

回報執行結果。"
