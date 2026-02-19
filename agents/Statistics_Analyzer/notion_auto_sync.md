# Notion 自動同步系統

## 同步流程

```
┌─────────────────────────────────────────────────────────┐
│                  自動同步流程                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 本地數據變更                                       │
│       ↓                                                 │
│  2. 觸發同步條件                                       │
│       ↓                                                 │
│  3. 轉換為 Notion 格式                                  │
│       ↓                                                 │
│  4. 寫入 Notion                                        │
│       ↓                                                 │
│  5. 驗證同步結果                                        │
│       ↓                                                 │
│  6. 更新本地狀態                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 觸發條件

| 觸發類型 | 條件 | 頻率 |
|----------|------|------|
| 即時 | 技能使用記錄 | 實時 |
| 定時 | 每天 18:00 | 每日 |
| 手動 | 用戶觸發 | 按需 |

## Notion API 配置

```python
import os
from notion_client import Client

NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
DATABASE_ID = '304a1238f49d80d18dacde615d0ade5a'

notion = Client(auth=NOTION_API_KEY)
```

## 同步腳本

### 1. 寫入 Notion
```python
def sync_to_notion(usage_data):
    """將使用數據同步到 Notion"""
    
    # 轉換格式
    properties = {
        "Agent": {"title": [{"text": {"content": usage_data["agent"]}}]},
        "Skill": {"select": {"name": usage_data["skill"]}},
        "Context": {"rich_text": [{"text": {"content": usage_data.get("context", "")}}]},
        "Success": {"checkbox": usage_data.get("success", False)},
        "Rating": {"number": usage_data.get("rating", 0)},
        "Timestamp": {"date": {"start": usage_data["timestamp"]}}
    }
    
    # 寫入 Notion
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=properties
    )
```

### 2. 讀取 Notion
```python
def fetch_notion_data():
    """從 Notion 讀取數據"""
    
    response = notion.databases.query(
        database_id=DATABASE_ID,
        sorts=[{"property": "Timestamp", "direction": "descending"}]
    )
    
    return response["results"]
```

### 3. 定時同步
```python
# Cron: 每天 18:00
def daily_sync():
    # 1. 收集今日數據
    today_data = collect_today_data()
    
    # 2. 同步到 Notion
    for data in today_data:
        sync_to_notion(data)
    
    # 3. 生成報告
    generate_daily_report()
```

## Cron Job 設定

```json
{
  "name": "notion-daily-sync",
  "schedule": "0 18 * * *",
  "task": "sync_to_notion",
  "enabled": true
}
```

## 數據對應

| 本地欄位 | Notion 欄位 |
|----------|--------------|
| agent | Agent (Title) |
| skill | Skill (Select) |
| context | Context (Text) |
| success | Success (Checkbox) |
| rating | Rating (Number) |
| timestamp | Timestamp (Date) |

## 錯誤處理

| 錯誤類型 | 處理方式 |
|----------|----------|
| API 錯誤 | 重試 3 次 |
| 網絡錯誤 | 排隊等待 |
| 格式錯誤 | 跳過並記錄 |

## 下一步
1. 部署同步腳本
2. 設定 Cron Job
3. 開始自動同步
