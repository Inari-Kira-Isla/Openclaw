# Notion Database 設定教學

## 方法 1: 手動建立 (推薦)

### Step 1: 建立 Page
1. 去 https://notion.so
2. 建立一個新 Page

### Step 2: 建立 Database
1. 係 Page 入面 type `/database` 
2. 選擇 "Table" view

### Step 3: 加入欄位

| 欄位名 | 類型 | 設定 |
|--------|------|------|
| Topic | Title | 預設 |
| Status | Select | Pending, In Progress, Ready for Review, Approved, Published, Rejected |
| Platform | Multi-select | Twitter/X, Instagram, TikTok, YouTube, LinkedIn |
| Created | Date | 預設 |
| Published Date | Date | 可選 |
| Thread Content | Text | 可選 |
| Source Links | URL | 可選 |
| Notes | Text | 可選 |

### Step 4: 取得 Database ID
1. 係 Database URL 度
2. 例如: `https://notion.so/{workspace}/{database_id}?v=...`
3. copy `database_id` (32 characters)

---

## 方法 2: 用 API 建立

如果你想用既 Notion API...

```
NOTION_API_KEY: 係 https://www.notion.so/my-integrations 度取得
```

---

## 下一步

1. 建立 Database
2. Copy Database ID
3. 告诉我，我會幫你入去 n8n
