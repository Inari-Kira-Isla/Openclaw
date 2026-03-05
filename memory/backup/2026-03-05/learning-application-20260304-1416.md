# 錯誤學習記錄 - 2026-03-04 14:16

## 新錯誤識別

### 1. Gemini API 403 錯誤 (高優先級)
| 時間 | 工具 | 錯誤 |
|------|------|------|
| 12:23 | web_search | Gemini API error (403) |

**原因分析:**
- Gemini API 返回 403 Forbidden
- 可能原因：API Key 過期/權限問題/配額限制

**修復方案:**
- [ ] 檢查 Gemini API Key 狀態
- [ ] 切換到其他搜尋工具 (Brave/Perplexity)

---

### 2. Telegram 發送失敗 (中優先級)
| 時間 | 錯誤 |
|------|------|
| 12:31 | chat not found (-1002381931352) |

**原因分析:**
- Bot 未在 DM 中啟動
- Bot 被移除群組
- 群組 ID 變更

**修復方案:**
- [ ] 確認 bot 是否仍在群組中
- [ ] 檢查 channel ID 是否正確

---

## 應用動作

### 1. 工具 Fallback 機制
- 主要搜尋: 維持 Brave API
- Fallback: Perplexity API
- 監控: Gemini API 錯誤次數

### 2. Telegram 群組驗證
- 定時驗證群組狀態
- 記錄有效的 channel IDs

---

## 記錄時間
2026-03-04 14:16 (學習即時應用鉤子觸發)
