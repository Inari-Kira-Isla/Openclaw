# OpenClaw GitHub Release 檢查 Workflow

## 📥 匯入方式

1. 打開 n8n (http://localhost:5678)
2. 點擊 "Import from File"
3. 選擇 `n8n/openclaw-github-release-check.json`

## ⚙️ 設定步驟

### 1. 環境變數
在 n8n 設定環境變數：
```
TELEGRAM_CHAT_ID = 你的Telegram Chat ID
TELEGRAM_API_TOKEN = 你的Telegram Bot Token
```

### 2. 啟用 Workflow
- 匯入後自動設為 inactive
- 點擊 "Active" 啟用

### 3. 驗證
- 手动觸發一次測試
- 確認 Telegram 收到訊息

## 🔧 自定義選項

| 項目 | 預設 | 說明 |
|------|------|------|
| 執行時間 | 8:00 AM PST | 可調整 |
| 比對方式 | 版本號比對 | 自動比對 |
| 通知格式 | HTML | 支援連結 |

## 📁 檔案位置
- Workflow: `n8n/openclaw-github-release-check.json`
- 版本記錄: `last-release.txt` (自動建立)

---
_建立日期: 2026-02-24_
