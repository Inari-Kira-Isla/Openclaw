#!/bin/bash
# OpenClaw QA Test Script
# 4D 框架測試腳本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common_functions.sh"

# 測試目標
TARGET="${1:-all}"

echo "========================================"
echo "  OpenClaw QA 測試"
echo "  目標: $TARGET"
echo "========================================"

PASS=0
FAIL=0

# ===== D1: 功能驗證 =====
test_d1() {
    log_info "=== D1: 功能驗證 ==="
    
    # 檢查必要命令
    for cmd in curl jq python3; do
        if check_command $cmd; then
            log_success "$cmd 可用"
            ((PASS++))
        else
            log_error "$cmd 不可用"
            ((FAIL++))
        fi
    done
    
    # 檢查腳本可執行
    for script in "$SCRIPT_DIR"/*.sh; do
        if [ -f "$script" ] && [ -x "$script" ]; then
            log_success "$(basename $script) 可執行"
            ((PASS++))
        fi
    done
}

# ===== D2: 狀態流轉閉環 =====
test_d2() {
    log_info "=== D2: 狀態流轉閉環 ==="
    
    # 檢查 lock 目錄
    if [ -d "/tmp/openclaw_locks" ]; then
        log_success "Lock 目錄存在"
        ((PASS++))
    else
        log_warn "Lock 目錄不存在（會自動建立）"
    fi
    
    # 檢查日誌目錄
    if [ -d "$SCRIPT_DIR/../logs" ]; then
        log_success "日誌目錄存在"
        ((PASS++))
    else
        log_warn "日誌目錄不存在"
    fi
}

# ===== D3: 時序與併發驗證 =====
test_d3() {
    log_info "=== D3: 時序與併發驗證 ==="
    
    # 測試 lock manager
    local test_lock="qa_test_$$"
    if "$SCRIPT_DIR/lock_manager.sh" acquire "$test_lock" 2>/dev/null; then
        log_success "Lock 機制正常"
        "$SCRIPT_DIR/lock_manager.sh" release "$test_lock" 2>/dev/null
        ((PASS++))
    else
        log_error "Lock 機制失敗"
        ((FAIL++))
    fi
}

# ===== D4: 跨機環境適應性 =====
test_d4() {
    log_info "=== D4: 跨機環境適應性 ==="
    
    # 檢查路徑變數
    if [ -n "$PATH" ]; then
        log_success "PATH 設定正常"
        ((PASS++))
    fi
    
    # 檢查 home 目錄
    if [ -n "$HOME" ]; then
        log_success "HOME 設定正常: $HOME"
        ((PASS++))
    fi
    
    # 檢查使用者
    if [ -n "$USER" ]; then
        log_success "USER 設定正常: $USER"
        ((PASS++))
    fi
}

# 執行測試
case "$TARGET" in
    d1) test_d1 ;;
    d2) test_d2 ;;
    d3) test_d3 ;;
    d4) test_d4 ;;
    all)
        test_d1
        test_d2
        test_d3
        test_d4
        ;;
    *) 
        echo "用法: $0 [d1|d2|d3|d4|all]"
        exit 1
        ;;
esac

# 輸出結果
echo "========================================"
echo "  測試結果"
echo "========================================"
echo -e "通過: ${GREEN}$PASS${NC}"
echo -e "失敗: ${RED}$FAIL${NC}"
echo "========================================"

[ $FAIL -eq 0 ] && exit 0 || exit 1
