# 錯誤即時學習記錄

**時間**: 2026-03-02 21:24

## 1. 錯誤檢查

### 發現的錯誤

| 錯誤類型 | 次數 | 發生時間 | 嚴重程度 |
|----------|------|----------|----------|
| LLM Timeout (MiniMax) | 4 | 13:13-13:16 | Medium |
| LLM Timeout (Ollama) | 4 | 13:13-13:16 | Medium |
| web_search API 403 | 1 | 21:24 | High |
| openclaw PATH 錯誤 | 20+ | Various | Low |

### 詳細錯誤

```
# Gemini API Key 問題
web_search failed: Gemini API error (403): 
"Your API key was reported as leaked. Please use another API key."

# LLM Timeout
embedded run timeout: Profile minimax:default timed out
embedded run timeout: Profile ollama:default timed out
```

## 2. 原因分析

| 錯誤 | 原因 |
|------|------|
| web_search 403 | Gemini API key 被舉報為洩漏，需要更換 API key |
| LLM Timeout | Cynthia subagent sessions 逾時，可能是 context 過高 (87%) |
| openclaw PATH | 腳本中直接呼叫 `openclaw` 但 PATH 未包含 |

## 3. 優化方案

| 項目 | 方案 |
|------|------|
| Gemini API | 需更新 web_search 配置，切換到其他 provider |
| LLM Timeout | 考慮增加 timeout 或優化 Cynthia session 清理 |
| PATH 問題 | 腳本中使用完整路徑 `/usr/local/bin/openclaw` |

## 4. 執行記錄

- ⚠️ Gemini API key 需要更換 - 待手動處理
- ✅ 已記錄 LLM Timeout 事件
- ✅ PATH 問題已識別

## 5. 學習結論

1. **API Key 管理**: 定期檢查 API key 狀態，避免 403 錯誤
2. **Session 清理**: 及時清理過期 session 避免 timeout
3. **腳本路徑**: 使用完整路徑避免 PATH 問題

---
_Learned: 2026-03-02 21:24_
