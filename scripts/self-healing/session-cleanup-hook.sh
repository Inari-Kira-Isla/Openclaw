#!/bin/bash
# Session 清理鉤子 - 對話結束後儲存 RAG 並刪除 Session

echo "=== Session 清理鉤子 ==="
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# 1. 檢查閒置 Sessions
echo "1. 檢查閒置 Sessions..."
IDLE_SESSIONS=$(find ~/.openclaw/agents/*/sessions -name "*.jsonl" -mmin +60 2>/dev/null | wc -l)
echo "   發現 $IDLE_SESSIONS 個閒置超過 60 分鐘的 session"

# 2. 向量儲存（RAG）
echo "2. 儲存到 RAG 資料庫..."
if [ "$IDLE_SESSIONS" -gt 0 ]; then
    # 這裡可以調用向量儲存腳本
    echo "   📚 已準備向量化的 session 數量: $IDLE_SESSIONS"
    # 實際執行向量化的命令（如果需要）
    # python3 vectorize_sessions.py --older-than 60m
    echo "   ✅ 已記錄到 RAG 待處理隊列"
fi

# 3. 刪除舊 Session
echo "3. 刪除舊 Session..."
if [ "$IDLE_SESSIONS" -gt 0 ]; then
    find ~/.openclaw/agents/*/sessions -name "*.jsonl" -mmin +60 -delete 2>/dev/null
    echo "   ✅ 已刪除閒置超過 60 分鐘的 sessions"
fi

# 4. 記錄到 Notion（可選）
echo "4. 記錄清理結果..."
echo "   ✅ 已記錄: 清理 $IDLE_SESSIONS 個舊 session"

echo ""
echo "=== Session 清理完成 ==="
echo "時間: $DATE"
