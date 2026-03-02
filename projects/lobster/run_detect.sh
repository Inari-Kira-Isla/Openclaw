#!/bin/bash
# Lobster Auto-Detect Script
# Run this from OpenClaw cron/heartbeat

cd /Users/ki/.openclaw/workspace/projects/lobster

# Run detection
node dist/index.js detect >> /Users/ki/.openclaw/logs/lobster_detect.log 2>&1

# Log timestamp
echo "$(date): Lobster detect completed" >> /Users/ki/.openclaw/logs/lobster_detect.log
