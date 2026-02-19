# Notion 資料庫設定指南

**版本**: v1.0
**日期**: 2026-02-18

---

## 📁 資料庫清單

### 1. AI 知識庫（主資料庫）

**建立網址**: https://www.notion.so/my-workspace/AI-%E7%9F%A5%E8%AD%98%E5%BA%AB

**欄位設定**:

| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| 名稱 | 標題 | 筆記標題 |
| 內容 | 文字 | Markdown 格式的完整內容 |
| 向量摘要 | 文字 | AI 生成的 200 字摘要 |
| 語義標籤 | 多選 | 海膽/AI/系統/商務/個人 |
| 角色歸屬 | 多選 | Athena/QI/DDH |
| 建立日期 | 日期 | 自動 |
| 修改日期 | 日期 | 自動 |
| 向量狀態 | 狀態 | 待處理/處理中/已向量化 |
| 關聯筆記 | 關聯 | 關聯其他筆記 |

---

### 2. 術語定義庫（子資料庫）

**建立網址**: https://www.notion.so/my-workspace/%E8%A1%93%E8%AD%9C%E5%AE%9A%E7%BE%A9

**欄位設定**:

| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| 術語 | 標題 | 專有名詞 |
| 定義 | 文字 | 詳細定義 |
| 領域 | 選擇 | AI/海膽/商務/系統 |
| 範例 | 文字 | 使用範例 |

---

## 🔧 API 設定

### Notion API Key

1. 前往 https://www.notion.so/my-integrations
2. 建立新的 Integration
3. 取得 API Key
4. 分享資料庫給 Integration

### 環境變數

```bash
NOTION_API_KEY=secret_xxxxx
NOTION_DATABASE_ID=xxxxx
```

---

## 📝 下一步

完成資料庫建立後，告訴我：
1. API Key 是否取得
2. 資料庫 ID

我幫你設定 n8n 自動化！

---

*設定時間: 2026-02-18*
