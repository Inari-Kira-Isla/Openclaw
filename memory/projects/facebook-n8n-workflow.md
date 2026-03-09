# Facebook Messenger + n8n + OpenClaw Workflow

## 架構

```
Facebook Messenger → n8n Webhook → OpenClaw → 回覆 → n8n → Messenger
```

---

## n8n Workflow 設定

### Step 1: 打開 n8n
```
http://localhost:5678
```

### Step 2: 建立新 Workflow

1. 點擊「+ New Workflow」
2. 點擊「+」添加節點

### Step 3: 添加節點

#### 節點 1: Facebook Trigger (接收訊息)
- 搜尋「Facebook」
- 選擇「Facebook Messenger Trigger」
- 設定：
  - Access Token: [你的 Page Access Token]
  - Verify Token: [你自己設定的 Token]
- 點擊「Fetch Event」測試

#### 節點 2: HTTP Request (發送到 OpenClaw)
- 選擇「HTTP Request」
- 設定：
  - Method: POST
  - URL: http://localhost:8080/api/v1/messages
  - Headers:
    - Content-Type: application/json
    - Authorization: Bearer [你的 OpenClaw Token]
  - Body: 
    ```json
    {
      "message": "{{ $json.message }}",
      "sender": "{{ $json.sender }}",
      "channel": "facebook"
    }
    ```

#### 節點 3: Telegram (通知你)
- 選擇「Telegram」
- 設定：
  - Chat ID: 8399476482
  - Text: 新 FB 訊息：{{ $json.message }}

---

## 測試流程

1. 儲存 Workflow
2. 啟動 Workflow (點擊開關)
3. 從粉絲專頁發測試訊息
4. 檢查 n8n 是否收到

---

## 疑難排解

| 問題 | 解決方式 |
|------|----------|
| 無法接收訊息 | 檢查 Webhook URL 是否正確 |
| Token 錯誤 | 重新產生 Facebook Access Token |
| OpenClaw 無回應 | 檢查 OpenClaw 是否運行 |

---

*記錄時間: 2026-02-18*
