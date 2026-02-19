#!/usr/bin/env python3
import requests

NOTION_API_KEY = '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'
headers = {'Authorization': 'Bearer ' + NOTION_API_KEY, 'Notion-Version': '2022-06-28'}

page_data = {
    'parent': {'database_id': '30aa1238f49d817c8163dd76d1309240'},
    'properties': {
        '標題': {'title': [{'text': {'content': '奇點時刻 - 11萬檔案整理里程碑'}}]},
        '向量狀態': {'select': {'name': '已向量化(標準流程)'}},
        '應用': {'rich_text': [{'text': {'content': '里程碑'}}]},
        '重點': {'rich_text': [{'text': {'content': '50小時 AI 協作完成不可能的任務'}}]},
        '向量摘要': {'rich_text': [{'text': {'content': '整理11萬檔案：桌面60K + Dropbox 31K + Facebook 19K，取消 Dropbox Plus'}}]}
    },
    'children': [
        {'paragraph': {'rich_text': [{'text': {'content': '## 成就\n- 桌面檔案整理: 60,102\n- Dropbox → Google Drive: 31,615\n- Facebook 清理: 19,135\n- 總計: ~110,000+'}}}},
        {'paragraph': {'rich_text': [{'text': {'content': '## 洞見\n以前時間被瑣事切割；現在被高度壓縮後，集中在決策、架構與優化。'}}}},
        {'paragraph': {'rich_text': [{'text': {'content': '## 行動\n- 取消 Dropbox Plus 訂閱\n- AI 從執行工具升級為策略夥伴'}}}}
    ]
}

response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=page_data)
if response.status_code == 200:
    print('已同步到 Notion')
else:
    print('錯誤:', response.text[:200])
