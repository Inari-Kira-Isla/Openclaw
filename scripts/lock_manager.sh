#!/bin/bash
# OpenClaw Lock Manager
# 防止重複執行機制

LOCK_DIR="/tmp/openclaw_locks"

# 建立鎖目錄
mkdir -p "$LOCK_DIR"

# 取得鎖
acquire_lock() {
    local job_name="$1"
    local lock_file="$LOCK_DIR/${job_name}.lock"
    
    # 檢查是否已有鎖
    if [ -f "$lock_file" ]; then
        # 檢查程序是否還在運行
        local pid=$(cat "$lock_file" 2>/dev/null)
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "❌ $job_name 正在執行中 (PID: $pid)"
            return 1
        else
            # 舊鎖，清理
            echo "🧹 清理過期鎖: $job_name"
            rm -f "$lock_file"
        fi
    fi
    
    # 建立新鎖
    echo $$ > "$lock_file"
    echo "✅ 取得鎖: $job_name (PID: $$)"
    return 0
}

# 釋放鎖
release_lock() {
    local job_name="$1"
    local lock_file="$LOCK_DIR/${job_name}.lock"
    
    rm -f "$lock_file"
    echo "🔓 釋放鎖: $job_name"
}

# 清理所有鎖
cleanup_locks() {
    rm -rf "$LOCK_DIR"
    echo "🧹 已清理所有鎖"
}

# 顯示狀態
status_locks() {
    echo "=== Lock 狀態 ==="
    ls -la "$LOCK_DIR" 2>/dev/null || echo "無鎖"
}

# 執行主命令
case "$1" in
    acquire)
        acquire_lock "$2"
        ;;
    release)
        release_lock "$2"
        ;;
    cleanup)
        cleanup_locks
        ;;
    status)
        status_locks
        ;;
    *)
        echo "用法: $0 <acquire|release|cleanup|status> <job_name>"
        ;;
esac
