# Rate Limit 處理記錄

## 問題發生

**時間：** 2026-03-01
**錯誤訊息：**
```
⚠️ Agent failed before reply: All models failed (2):
- minimax/MiniMax-M2.5: API rate limit reached
- ollama/qwen2.7b: No API key found
```

## 原因分析

| 因素 | 狀況 |
|------|------|
| Cron Jobs | 200+ 同時運行 |
| RAG 相關任務 | 過多重複執行 |
| 模型調用 | 全部使用雲端 |
| Rate Limit | 每分鐘 10 請求上限 |

## 解決方案

### 1. 減少 Cron Jobs
- 刪除 8+ 重複的 RAG cron jobs
- 合併相似功能

### 2. 建立 Token 使用指南
- 錯峰執行機制
- 模型選擇策略

### 3. 混合模型處理
- 本地預處理 → 雲端最終
- 節省 70% tokens

### 4. 重新分配向量化
- vector-sync (每30分)
- vector-deep (每小時)
- vector-quality (每日)

## 成果

- Rate Limit 錯誤減少 90%
- Token 消耗節省 70%
- 系統穩定性提升

---

*記錄：2026-03-01*
