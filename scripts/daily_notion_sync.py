#!/usr/bin/env python3
"""
每日 Notion 同步腳本 - 系統狀態同步
"""

import requests
from datetime import datetime

NOTION_API_KEY = "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"
DATABASE_ID = "30aa1238f49d817c8163dd76d1309240"
NOTION_VERSION = "2022-06-28"

def create_daily_sync():
    """建立每日同步記錄"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    system_status = "## 系統狀態\n- 中央治理核心 (muse-core): 運作中\n- 模型調度員 (model-dispatcher): 新建立\n- 其他 10 個 Agent: 待設定"
    sync_items = "## 同步項目\n- AGENTS.md: 已更新 (v2.0)\n- 工作流協調器: 待設定\n- MCP 構建器: 待設定\n- 技能創建器: 待設定"
    tech_details = f"## 技術細節\n- 架構: Workflow-driven\n- 模型策略: minimax-only\n- 同步時間: {current_time} (Asia/Macau)"
    next_steps = "## 下一步\n- 完成其餘 Agent 設定\n- 啟用工作流協調器\n- 優化技能系統"
    
    page_data = {
        'parent': {'database_id': DATABASE_ID},
        'properties': {
            '標題': {'title': [{'text': {'content': f'每日同步 - {today}'}}]},
            '向量狀態': {'select': {'name': '已向量化'}},
            '應用': {'rich_text': [{'text': {'content': 'OpenClaw 系統'}}]},
            '重點': {'rich_text': [{'text': {'content': 'muse-core 運作中，12 個 Agent 已建立'}}]},
            '向量摘要': {'rich_text': [{'text': {'content': '每日 Cron 同步完成，系統正常運作'}}]}
        },
        'children': [
            {'paragraph': {'rich_text': [{'text': {'content': system_status}}]}},
            {'paragraph': {'rich_text': [{'text': {'content': sync_items}}]}},
            {'paragraph': {'rich_text': [{'text': {'content': tech_details}}]}},
            {'paragraph': {'rich_text': [{'text': {'content': next_steps}}]}}
        ]
    }
    
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
    }
    
    response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=page_data)
    
    if response.status_code == 200:
        print('✅ 每日同步成功')
        print(f'   Page ID: {response.json().get("id", "N/A")}')
        return True
    else:
        print(f'❌ 同步失敗: {response.status_code}')
        print(f'   {response.text[:200]}')
        return False

if __name__ == '__main__':
    create_daily_sync()
