#!/bin/bash
# n8n Workflow Import Script

N8N_URL="http://127.0.0.1:5678"
WORKFLOW_FILE="n8n/workflows/telegram_command_handler.json"

echo "Importing workflow to n8n..."

# Read workflow JSON
WORKFLOW_JSON=$(cat $WORKFLOW_FILE)

# Try to import (may need manual auth)
echo "Please open n8n at: http://localhost:5678"
echo ""
echo "To import the workflow:"
echo "1. Click 'Workflows' in the menu"
echo "2. Click 'Import from File'"
echo "3. Select: $WORKFLOW_FILE"
echo ""
echo "Or use curl with authentication:"
echo "curl -X POST -H 'Content-Type: application/json' -d @\$WORKFLOW_JSON http://127.0.0.1:5678/rest/workflows"
