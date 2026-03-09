#!/bin/bash
# Self-Healing Hook - 自動修復系統問題

echo "=== 自動修復系統 ==="
echo "時間: $(date)"
echo ""

# 1. 檢查 Cron Error
echo "1. 檢查 Cron Error..."
CRON_ERRORS=$(openclaw cron list 2>&1 | grep "error" | wc -l)
echo "   發現 $CRON_ERRORS 個錯誤"

# 2. 檢查 Sessions 鎖
echo "2. 檢查 Sessions 鎖..."
LOCKS=$(find ~/.openclaw/agents/*/sessions/*.lock 2>/dev/null | wc -l)
if [ "$LOCKS" -gt 0 ]; then
    echo "   發現 $LOCKS 個鎖檔，嘗試移除..."
    find ~/.openclaw/agents/*/sessions/*.lock -delete 2>/dev/null
    echo "   ✅ 已移除"
else
    echo "   ✅ 無鎖檔"
fi

# 3. 檢查記憶體
echo "3. 檢查記憶體使用..."
MEMORY_USAGE=$(df -h ~ | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$MEMORY_USAGE" -gt 80 ]; then
    echo "   ⚠️ 記憶體使用過高: $MEMORY_USAGE%"
else
    echo "   ✅ 記憶體正常: $MEMORY_USAGE%"
fi

# 4. 檢查 Gateway
echo "4. 檢查 Gateway..."
GATEWAY_STATUS=$(openclaw status 2>&1 | grep "Gateway" | grep -c "running")
if [ "$GATEWAY_STATUS" -eq 1 ]; then
    echo "   ✅ Gateway 正常"
else
    echo "   ⚠️ Gateway 可能問題，嘗試重啟..."
    openclaw gateway restart 2>/dev/null
    echo "   ✅ 已發起重啟指令"
fi

echo ""
echo "=== 自檢完成 ==="
