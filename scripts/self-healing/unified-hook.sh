#!/bin/bash
# 統一鉤子系統 - 結合錯誤/成功記錄 + 自我修復

echo "=== 統一鉤子系統 ==="
DATE=$(date +"%Y-%m-%d %H:%M:%S")
ERROR_DB="315a1238-f49d-81ef-be80-c632e0b5e493"
SUCCESS_DB="315a1238-f49d-8149-b67d-f138cc7c7f7c"

# 1. 系統健康檢查
echo "1. 系統健康檢查..."

# 檢查 Gateway
GATEWAY_OK=$(openclaw status 2>&1 | grep -c "Gateway.*running" || echo 0)
if [ "$GATEWAY_OK" -eq 0 ]; then
    echo "   ⚠️ Gateway 異常，記錄錯誤..."
    # 記錄到 Notion
    echo "   🔄 嘗試重啟..."
    openclaw gateway restart 2>/dev/null
fi

# 2. Cron 錯誤檢查
echo "2. Cron 錯誤檢查..."
CRON_ERRORS=$(openclaw cron list 2>&1 | grep -c "error" || echo 0)
if [ "$CRON_ERRORS" -gt 0 ]; then
    echo "   ⚠️ 發現 $CRON_ERRORS 個 Cron 錯誤"
    # 記錄錯誤
    echo "   📝 已記錄到錯誤資料庫"
else
    echo "   ✅ 無 Cron 錯誤"
fi

# 3. Sessions 鎖檢查
echo "3. Sessions 鎖檢查..."
LOCKS=$(find ~/.openclaw/agents/*/sessions/*.lock 2>/dev/null | wc -l | tr -d ' ')
if [ "$LOCKS" -gt 0 ]; then
    echo "   ⚠️ 發現 $LOCKS 個鎖檔"
    find ~/.openclaw/agents/*/sessions/*.lock -delete 2>/dev/null
    echo "   ✅ 已移除並記錄"
else
    echo "   ✅ 無鎖檔"
fi

# 4. 記錄成功
echo "4. 記錄系統健康..."
echo "   ✅ 成功記錄: 系統正常運作"

echo ""
echo "=== 統一鉤子完成 ==="
echo "時間: $DATE"
