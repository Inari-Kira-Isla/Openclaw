#!/bin/bash
# OpenClaw Common Functions
# 共用函數庫

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日誌函數
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 檢查命令
check_command() {
    local cmd="$1"
    if ! command -v $cmd &>/dev/null; then
        log_error "缺少命令: $cmd"
        return 1
    fi
    return 0
}

# 檢查檔案
check_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        log_error "檔案不存在: $file"
        return 1
    fi
    return 0
}

# 檢查目錄
check_dir() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        log_error "目錄不存在: $dir"
        return 1
    fi
    return 0
}

# 網路檢查
check_network() {
    if ! curl -s --max-time 5 https://api.github.com >/dev/null 2>&1; then
        log_warn "網路可能不可用"
        return 1
    fi
    return 0
}

# API 檢查
check_api() {
    local url="$1"
    local timeout="${2:-5}"
    
    if ! curl -s --max-time $timeout "$url" >/dev/null 2>&1; then
        log_error "API 無法連接: $url"
        return 1
    fi
    return 0
}

# 清理暫存
cleanup_temp() {
    rm -rf /tmp/openclaw_* 2>/dev/null
    log_info "已清理暫存檔"
}

# 錯誤處理
error_exit() {
    log_error "$1"
    exit 1
}

# 成功輸出
success_exit() {
    log_success "$1"
    exit 0
}
