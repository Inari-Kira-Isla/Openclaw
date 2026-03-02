#!/bin/bash
# OpenClaw Cron Job Wrapper
# 包含 Lock 機制 + 基本環境檢查

JOB_NAME="${1:-cron_job}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_MANAGER="$SCRIPT_DIR/lock_manager.sh"

# 來源共用函數
source "$SCRIPT_DIR/common_functions.sh" 2>/dev/null

# ===== D3: 時序與併發驗證 =====
# 嘗試取得鎖
if ! "$LOCK_MANAGER" acquire "$JOB_NAME"; then
    echo "❌ 任務已在執行中，跳過"
    exit 1
fi

# 確保退出時釋放鎖
trap '"$LOCK_MANAGER" release "$JOB_NAME"' EXIT

# ===== D1: 功能驗證 =====
echo "🔍 開始任務: $JOB_NAME"

# 檢查必要命令
for cmd in curl jq python3; do
    if ! command -v $cmd &>/dev/null; then
        echo "❌ 缺少必要命令: $cmd"
        exit 1
    fi
done

# 檢查環境變數
if [ -z "$OPENCLAW_API" ] && [ ! -f ~/.openclaw/api_key ]; then
    echo "⚠️ 警告: 未設定 OPENCLAW_API"
fi

# ===== 執行主任務 =====
# 在這裡執行你的實際任務
# 例如: python3 script.py

# ===== D2: 狀態流轉閉環 =====
echo "✅ 任務完成: $JOB_NAME"

# 清理暫存檔
rm -rf /tmp/openclaw_* 2>/dev/null

exit 0
