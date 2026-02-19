# Facebook Messenger + n8n + OpenClaw 整合計畫

**日期**: 2026-02-18
**狀態**: 進行中

---

## 粉絲專頁

**名稱**: Inari Global Food

---

## 架構圖

```
Facebook Messenger (Inari Global Food)
        ↓
    n8n Webhook
        ↓
    OpenClaw API
        ↓
    AI 處理 + 回覆
        ↓
    Telegram 通知
```

---

## 已建立 SKILL

| SKILL 名稱 | 描述 | 位置 |
|------------|------|------|
| facebook_messenger_handler | Messenger 訊息處理 | skills/facebook-agent/ |
| faq_auto_reply | FAQ 自動回覆 | skills/facebook-agent/ |
| handoff_manager | 轉接人工管理 | skills/facebook-agent/ |
| conversation_logger | 對話記錄 | skills/facebook-agent/ |

---

## 待辦事項

### 前置作業
- [x] Facebook 開發者帳號 ✅
- [x] Facebook 粉絲專頁 (Inari Global Food) ✅
- [x] 建立 Meta App ✅
- [x] 加入 Messenger 產品 ✅
- [ ] 取得 Page Access Token ⬅️ 現在這裡

### 技術設定
- [ ] n8n workflow: FB Webhook → OpenClaw API
- [ ] OpenClaw API 端點設定
- [ ] 測試訊息接收

---

## 取得 Page Access Token

1. 進入 Meta App 設定
2. 找到 Messenger 設定
3. 點擊「產生 Token」或類似選項
4. 複製 Page Access Token

---

## 📝 Notion 同步

- 筆記總覽: https://www.notion.so/30ba1238f49d81968b1cf9ac2b197eb6
- Database ID: 30aa1238f49d817c8163dd76d1309240

---

*記錄時間: 2026-02-18 09:05*
