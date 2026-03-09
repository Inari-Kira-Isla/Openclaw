# Rate Limit 處理方法記錄

## 2026-03-01 更新

### 遇到的 Rate Limit 問題

| API | 錯誤碼 | 頻率 | 影響 |
|-----|--------|------|------|
| Web Search (Brave) | 429 | 每小時 | 熱門話題研究中斷 |
| Gemini API | 429 | 頻繁 | 研究任務延遲 |
| MiniMax API | 偶發 | 偶發 | 訂單分析延遲 |

### 處理方法

#### 1. 立即處理 (Immediate)
- **備用數據機制**: 維持一份離線備用數據，當 API 限流時自動切換
- **重試機制**: 實現指數退避 (Exponential Backoff)，首次等待 14s，之後遞增
- **降級服務**: 從即時數據降級為預先收集的資料

#### 2. 短期優化 (Short-term)
- **多 API 來源**: 配置多個搜索 API 作為備用
- **本地模型 fallback**: 使用 Ollama 本地模型 (qwen2.5:7b, llama3) 作為備用
- **快取機制**: 對不常變化的數據實施本地快取

#### 3. 長期架構 (Long-term)
- **API 可用性檢查**: 部署前自動檢查 API Key 有效性
- **健康檢查鉤子**: 定時檢測系統中斷並嘗試修復
- **混合架構**: MiniMax 雲端 + Ollama 本地雙軌制

### 程式碼實作

```javascript
// Rate Limit 處理範例
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (err.status === 429) {
        const waitTime = Math.pow(2, i) * 1000; // 指數退避
        await sleep(waitTime);
      }
    }
  }
  return fallbackData; // 使用備用數據
}
```

### 監控與告警

- 每次 API 調用記錄狀態
- 連續失敗 3 次觸發告警
- 每日健康檢查報告

---

_更新：2026-03-01_
