# 🦞 Lobster System

錯誤與成功學習系統 - 記錄犯過的錯，避免重複

## 功能

- 🔍 **自動偵測**: Cron errors, API failures, Session errors
- 📝 **記錄學習**: 結構化記錄錯誤與成功經驗
- 🛡️ **預防機制**: 行動前檢查相關歷史錯誤
- 📊 **趨勢分析**: 每日/每週回顧

## 安裝

```bash
cd projects/lobster
npm install
```

## 設定

1. 複製環境變數範本:
```bash
cp .env.example .env
```

2. 編輯 `.env`:
- `NOTION_API_KEY`: 從 https://www.notion.so/my-integrations 取得
- `NOTION_ERROR_DB_ID`: 錯誤資料庫 ID
- `NOTION_SUCCESS_DB_ID`: 成功資料庫 ID

3. 在 Notion 建立資料庫（參考 `docs/notion-templates.md`）

## 使用

```bash
# 編譯
npm run build

# 自動偵測錯誤
npm start detect

# 每日回顧
npm start review

# 每週總結
npm start weekly

# 統計
npm start stats

# 行動前檢查
npm start check "deploy" "production"
```

## 整合 OpenClaw

建立 OpenClaw Skill: `skills/lobster/SKILL.md`

## 架構

```
src/
├── index.ts      # 主入口
├── types.ts      # 類型定義
├── notion.ts    # Notion API
├── detector.ts  # 錯誤偵測
├── recorder.ts  # 記錄模組
└── review.ts    # 回顧引擎
```

---

*願龍蝦每次蛻殼都會變強 🦞*
