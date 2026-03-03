import os

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
import requests
import json

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
headers = {'Authorization': 'Bearer ' + NOTION_API_KEY, 'Notion-Version': '2022-06-28'}

url = 'https://api.notion.com/v1/databases/30aa1238f49d817c8163dd76d1309240/query'
response = requests.post(url, headers=headers, json={'page_size': 50})
pages = response.json().get('results', [])

for page in pages:
    props = page.get('properties') or {}
    title = props.get('標題', {}).get('title', [{}])[0].get('plain_text', '')
    page_id = page['id']
    
    app = None
    if 'fastlane' in title.lower():
        app = '自動化'
    elif 'ollama' in title.lower():
        app = '數據分析'
    elif 'n8n' in title.lower():
        app = '自動化'
    
    if app:
        data = {
            "properties": {
                "應用": {
                    "rich_text": [{"text": {"content": app}}]
                }
            }
        }
        patch_url = 'https://api.notion.com/v1/pages/' + page_id
        requests.patch(patch_url, headers=headers, json=data)
        print('更新: ' + title[:30] + ' -> ' + app)

print('\n完成!')
