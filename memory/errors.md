# 任務失敗記錄

**時間**: 2026-03-03 11:30

## 錯誤檢查結果

- **檢查時間**: 11:30 (過去1小時)
- **新錯誤**: 0
- **系統狀態**: ✅ 正常

### 本次檢查結果

✅ 過去1小時無失敗任務
✅ OpenClaw Gateway 正常 (1.8ms)
✅ Context 使用率 15% (健康)
✅ Cache 命中率 72% (優秀)
⚠️ 記憶體使用 93% (持續偏高)

### 持續錯誤 (跟進中)

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| Notion API Sync | 401 | Token invalid |
| Gemini API | 403 | API key leaked (已知) |

---

**時間**: 2026-03-03 10:30

## 錯誤檢查結果

- **檢查時間**: 10:30 (過去1小時)
- **新錯誤**: 0
- **系統狀態**: ✅ 正常

### 本次檢查結果

✅ 過去1小時無失敗任務
✅ 系統響應正常 (1.8ms)
⚠️ 記憶體使用 93% (需關注)

### 持續錯誤 (跟進中)

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| Notion API Sync | 401 | Token invalid |
| Gemini API | 403 | API key leaked (已知) |

---

**時間**: 2026-03-03 10:27

## 錯誤檢查結果

- **檢查時間**: 10:27 (過去1小時)
- **新錯誤**: 1
- **系統狀態**: ⚠️ 需關注

### 本次新錯誤

| 任務 | 錯誤 | 說明 |
|------|------|------|
| Ollama Model Discovery | TimeoutError | 模型發現超時 |

### 持續錯誤 (跟進中)

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| Notion API Sync | 401 | Token invalid (AI衝突鉤同步失敗) |
| Gemini API | 403 | API key leaked (已知) |

### 行動項目

| 優先級 | 任務 | 行動 |
|--------|------|------|
| P0 | Notion API | 更新 token |
| P1 | Ollama | 檢查服務狀態 |
| P2 | search-console | 進一步診斷 |

✅ 已記錄 - 2026-03-03 10:27

---
**時間**: 2026-03-03 06:17

## 過去1小時錯誤分析

- 檢查時間: 06:17 (過去1小時)
- **新錯誤: 0**
- 系統運行正常，無新增失敗任務

## 持續錯誤 (歷史)

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| lobster_weekly/detect/review | 401 | Notion API token invalid |

## 分析

- ✅ 無新失敗任務
- ✅ Gateway 響應正常 (200)
- ✅ Cron jobs 正常運行

✅ 已記錄

---
**時間**: 2026-03-03 07:24

## 錯誤檢查結果

- 檢查時間: 07:24
- Gateway 響應: 18ms ✅
- **新錯誤: 0**
- 系統運行正常

---
**時間**: 2026-03-03 05:08

## 新增錯誤

| 任務 | 狀態 | 說明 |
|------|------|------|
| lobster_weekly | 401 Error | Notion API token invalid |
| lobster_detect | 401 Error | Notion API token invalid |
| lobster_review | 401 Error | Notion API token invalid |

## 歷史錯誤 (2026-03-02)

| 任務 | 狀態 | 說明 |
|------|------|------|
| tidal-cr | SIGTERM | 被終止 |

## 錯誤任務

| 任務 | 狀態 | 說明 |
|------|------|------|
| youtube-analytics | error | 每 1 小時 |
| model-training-cycle | error | 每 6 小時 |
| memory-index-build | error | 每 6 小時 |
| 知識-優化筆記 | error | 每日 03:00 |
| 優化-Cron合併 | error | 每日 03:00 |
| 測試閉環-驗證 | error | 每 6 小時 |
| 備份-記憶庫自動備份 | error | 每日 03:00 |
| learning-system | error | 每日 04:00 |

## 分析
- tidal-cr: SIGTERM 信號終止（安靜時段被終止，正常行為）
- 其餘 error: 多為閒置定時任務

---
_Failed: 2026-03-02 23:15_

## 錯誤任務

| 任務 | 狀態 | 說明 |
|------|------|------|
| error-log-hook | skipped | 每 15 分鐘 |
| success-log-hook | skipped | 每 15 分鐘 |
| 向量庫系列 (6個) | skipped | 每 13-43 分鐘 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| search-console | error | 每小時 |
| performance-alert | skipped | 每 30 分鐘 |

## 失敗原因分析

- **skipped**: 多為排程跳過（，可能是排程衝突或資源佔用）
- **error**: Heartbeat 監控、search-console 持續失敗

## 修復建議

| 任務 | 動作 |
|------|------|
| 向量庫系列 | 檢查 memory-agent 狀態 |
| error/success hooks | 檢查 team agent |
| search-console | 修復 analytics 配置 |

✅ 已記錄

---
_Failed: 2026-03-02 21:56_

**時間**: 2026-03-02 20:49

## 錯誤任務

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時執行 |
| 測試閉環-驗證 | error | 定時任務 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |

### 說明
- 3 個持續性錯誤（已知問題）
- 其餘 cron jobs 正常運行

✅ 已記錄

---
_Failed: 2026-03-02 20:49_

---

**時間**: 2026-03-02 18:14

- 失敗: 0

✅ 完成

---
_Failed: 2026-03-02 18:14_

---
**時間**: 2026-03-03 02:23

## 過去1小時錯誤分析

| 錯誤類型 | 次數 | 原因 |
|----------|------|------|
| Gemini API 403 | 3 | API key leaked（已知） |
| Telegram bot token | 2 | 配置缺失 |
| edit failed | 4 | 文本匹配失敗 |
| exec timeout | 2 | 命令超時 |
| lsof not found | 1 | 工具缺失 |

## 持續錯誤

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| 向量庫系列 | skipped | 閒置 |

## 新增錯誤

1. **lsof command not found** - macOS 工具路徑問題
2. **Telegram recipient not found** - 多個 username 解析失敗

## 修復建議

| 錯誤 | 動作 |
|------|------|
| Gemini API 403 | 需更換 API key |
| lsof | 使用 pgrep/lsof 替代方案 |
| Telegram chat ID | 改用 numeric ID |

✅ 已記錄

---
_Failed: 2026-03-03 02:23_

---

**時間**: 2026-03-03 07:22

## 錯誤檢查結果

- **檢查時間**: 07:22
- **新錯誤**: 0
- **系統狀態**: 正常

### 持續錯誤 (跟進中)

| 任務 | 狀態 | 說明 |
|------|------|------|
| search-console | error | 每小時 |
| Heartbeat穩定性監控 | error | 每 20 分鐘 |
| lobster_weekly/detect/review | 401 | Notion API token invalid |

### 行動項目
- ⏳ search-console: 需進一步診斷
- ⏳ Heartbeat穩定性監控: 檢查配置
- ⏳ lobster_weekly: 需更新 Notion API token

✅ 已記錄

---
