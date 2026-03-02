# Notion 資料庫模板

## 錯誤資料庫 (Error Database)

建立新資料庫，添加以下欄位：

| 欄位名稱 | 類型 | 選項/說明 |
|---------|------|----------|
| 類型 | 單一選擇 | 錯誤、成功 |
| 來源 | 單一選擇 | cron, api, session, manual |
| 嚴重程度 | 單一選擇 | high, medium, low |
| 標題 | 標題 | - |
| 描述 | 文字 | - |
| 原因 | 文字 | (可選) |
| 解決方案 | 文字 | (可選) |
| 預防措施 | 文字 | (可選) |
| 標籤 | 多選 | cron, api, automation, openclaw, decision, code, other |
| 狀態 | 單一選擇 | Open, Resolved, Monitoring |
| 發生次數 | 數字 | 預設 1 |
| 發生時間 | 創建時間 | 自動 |

---

## 成功資料庫 (Success Database)

建立新資料庫，添加以下欄位：

| 欄位名稱 | 類型 | 選項/說明 |
|---------|------|----------|
| 類型 | 單一選擇 | 錯誤、成功 |
| 標題 | 標題 | - |
| 工作流 | 文字 | 描述這個成功的工作流程 |
| 描述 | 文字 | 詳細說明 |
| 標籤 | 多選 | automation, workflow, best-practice, integration |
| Lessons | 文字 | 學到的教訓（可多行） |
| 記錄時間 | 創建時間 | 自動 |

---

## 取得 Database ID

1. 打開資料庫頁面
2. 點擊 Share → Copy link
3. ID 是網址中的最後一段：
   ```
   https://notion.so/[workspace]/[DATABASE_ID]?v=...
   ```
4. 將 `DATABASE_ID` 複製到 `.env` 文件

---

## 設定環境變數

```bash
# 在 projects/lobster/.env 中填入：
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_ERROR_DB_ID=你的錯誤資料庫ID
NOTION_SUCCESS_DB_ID=你的成功資料庫ID
```

---

## 取得 Notion API Key

1. 前往 https://www.notion.so/my-integrations
2. 點擊 "New integration"
3. 名稱輸入 "Lobster System"
4. 取得 API Key
5. 在你的 Notion 資料庫中，點擊 "..." → "Connections" → 添加 "Lobster System"

---

*設定完成後，運行 `npm run build` 編譯，然後 `npm start detect` 測試 🦞*
