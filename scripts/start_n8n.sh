#!/bin/bash
# n8n Setup Script
# Run this to start n8n

echo "Starting n8n..."

# Check if already running
if docker ps | grep -q n8n; then
    echo "n8n is already running!"
    echo "Access at: http://localhost:5678"
    exit 0
fi

# Run n8n container
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.openclaw/workspace/n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=false \
  -e N8N_HOST=localhost \
  -e WEBHOOK_URL=http://localhost:5678 \
  n8nio/n8n

echo "n8n starting..."
echo "Access at: http://localhost:5678"
