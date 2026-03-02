# SKILL.md - Lobster System

## 觸發條件

當用戶提及以下關鍵字時觸發：
- 「記錄錯誤」
- 「犯錯」
- 「不要再犯」
- 「學習系統」
- 「lobster」
- 「錯誤記錄」

## 功能

### 1. 記錄錯誤
- 語法: `記錄錯誤 <標題> | <描述> | <標籤>`
- 範例: `記錄錯誤 API 超時 | MiniMax API 回應逾時 | api,minimax`

### 2. 記錄成功
- 語法: `記錄成功 <標題> | <工作流> | <教訓>`
- 範例: `記錄成功 自動化部署 | 使用 GitHub Actions | 需先測試`

### 3. 行動前檢查
- 語法: `檢查 <動作>`
- 範例: `檢查 部署到生產環境`

### 4. 每日回顧
- 語法: `錯誤回顧` 或 `lobster review`

### 5. 統計
- 語法: `錯誤統計` 或 `lobster stats`

### 6. 自動偵測
- 每小時自動執行
- 偵測 Cron errors、Session errors

## 輸出格式

```
🦞 Lobster System

[錯誤/成功記錄]
✅ 已記錄: <標題>

[行動前檢查]
⚠️ 發現 <N> 個相關錯誤:
- [<嚴重程度>] <標題>
  → <預防措施>

[每日回顧]
📊 開放錯誤: <N>
🔴 高嚴重: <N>
趨勢: <improving/stable/worsening>
```

## 調用底層服務

```typescript
import Lobster from './projects/lobster/src/index';

const lobster = new Lobster(config);
await lobster.addError({ ... });
await lobster.checkBeforeAction('deploy', 'production');
```

## 環境依賴

- NOTION_API_KEY: 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
- NOTION_ERROR_DB_ID: 315a1238f49d81efbe80c632e0b5e493
- NOTION_SUCCESS_DB_ID: 315a1238f49d8149b67df138cc7c7f7c

---

*願龍蝦每次蛻殼都會變強 🦞*
