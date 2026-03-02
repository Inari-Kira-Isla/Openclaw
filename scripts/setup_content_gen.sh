#!/bin/bash

# Content Generation Workflow Setup Script

echo "📋 Content Generation Workflow - Phase 1 Setup"
echo "================================================"
echo ""

# Check if n8n is running
echo "1. Checking n8n..."
if curl -s http://localhost:5678/ > /dev/null 2>&1; then
    echo "   ✅ n8n is running"
else
    echo "   ❌ n8n is not running"
    echo "   Please start n8n first"
    exit 1
fi

echo ""
echo "2. Environment Variables Needed:"
echo "   - NOTION_CONTENT_DB_ID: Your Notion Database ID"
echo "   - TELEGRAM_CHAT_ID: Your Telegram Chat ID"
echo "   - SERPER_API_KEY: Your Serper API Key"
echo "   - OPENCLAW_TOKEN: Your OpenClaw Token"
echo ""

echo "3. To get Notion Database ID:"
echo "   - Go to Notion"
echo "   - Create a new Database with the schema in scripts/notion_content_db.json"
echo "   - Copy the database URL"
echo "   - The ID is the part after the last /"
echo ""

echo "4. To get Telegram Chat ID:"
echo "   - Message @userinfobot on Telegram"
echo "   - It will tell you your Chat ID"
echo ""

echo "5. To get Serper API Key:"
echo "   - Go to serper.dev"
echo "   - Sign up for free (100 searches/day)"
echo "   - Copy your API key"
echo ""

echo "6. To get OpenClaw Token:"
echo "   - Check your openclaw config"
echo ""

# Create .env file template
cat > ~/.openclaw/content-gen.env << 'EOF'
# Content Generation Workflow Environment Variables
NOTION_CONTENT_DB_ID=your_notion_db_id_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
SERPER_API_KEY=your_serper_api_key_here
OPENCLAW_TOKEN=your_openclaw_token_here
EOF

echo "✅ Created environment template at ~/.openclaw/content-gen.env"
echo ""
echo "Next Steps:"
echo "1. Fill in the environment variables"
echo "2. Import the workflow in n8n: http://localhost:5678"
echo "3. Add the credentials in n8n"
echo "4. Activate the workflow"
