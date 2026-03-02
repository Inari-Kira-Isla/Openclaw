#!/bin/bash
# 每6小時 Cron 效率分析

echo "=== Cron 效率分析 ==="

# Count crons
TOTAL=$(openclaw cron list 2>/dev/null | grep -c "id:" || echo "0")
echo "總 Cron 數: $TOTAL"

# Check errors
ERRORS=$(openclaw cron list 2>/dev/null | grep -c "error" || echo "0")
echo "錯誤數: $ERRORS"

# Running
RUNNING=$(openclaw cron list 2>/dev/null | grep -c "running" || echo "0")
echo "運行中: $RUNNING"

echo "=== 分析完成 ==="
