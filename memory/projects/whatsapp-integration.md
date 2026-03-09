# WhatsApp + n8n + OpenClaw 整合計畫

**日期**: 2026-02-18
**狀態**: SKILL 建立完成

---

## 架構

```
WhatsApp → n8n Webhook → OpenClaw API → AI 處理 → 回覆 → n8n → WhatsApp
                    ↓
               Telegram 通知
```

---

## 已建立

| 項目 | 位置 |
|------|------|
| SKILL | `skills/lifeos-agent/whatsapp_handler/SKILL.md` |
| n8n Workflow | `n8n/whatsapp-workflow.json` |

---

## 待辦事項

### 前置作業
- [ ] Twilio 帳號註冊
- [ ] WhatsApp Sandbox 申請
- [ ] Phone Number ID 取得
- [ ] Access Token 取得

### 技術設定
- [ ] n8n workflow 匯入
- [ ] Twilio credentials 設定
- [ ] Webhook 設定
- [ ] 測試訊息接收

---

## 整合方式

### 選項 A: Twilio (推薦)
| 項目 | 說明 |
|------|------|
| 費用 | 免費試用 |
| 難度 | 簡單 |
| 適合 | 測試/小型 |

### 選項 B: WhatsApp Business API
| 項目 | 說明 |
|------|------|
| 費用 | 按訊息收費 |
| 難度 | 複雜 |
| 適合 | 正式營運 |

---

## 參考資源

- Twilio: https://www.twilio.com/
- n8n WhatsApp: https://docs.n8n.io/integrations/builtin/app-nodes/

---

*記錄時間: 2026-02-18 08:55*
