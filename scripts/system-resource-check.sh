#!/bin/bash
# 每小時系統資源檢查

echo "=== 系統資源檢查 ==="

# CPU
CPU=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')
echo "CPU: $CPU%"

# Memory
MEM=$(vm_stat | head -10 | grep "Pages active" | awk '{print $3}' | sed 's/\.//')
echo "Memory: $MEM pages"

# Disk
DISK=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
echo "Disk: $DISK%"

# Network connections
NET=$(netstat -an | grep ESTABLISHED | wc -l)
echo "Network: $NET connections"

echo "=== 檢查完成 ==="
