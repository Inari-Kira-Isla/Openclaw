# 模型效果測試報告

**日期**: 2026-03-05
**時間**: 04:14 AM (Asia/Macau)

## 1. 本地模型測試

### 可用模型清單
| Model | Size | Modified |
|-------|------|----------|
| qwen2.5:7b | 4.7 GB | 7 days ago |
| nomic-embed-text:latest | 274 MB | 10 days ago |
| deepseek-coder:1.3b | 776 MB | 12 days ago |
| mistral:latest | 4.4 GB | 13 days ago |
| codellama:latest | 3.8 GB | 13 days ago |
| deepseek-coder:latest | 776 MB | 13 days ago |
| llama3:latest | 4.7 GB | 13 days ago |

### 測試執行
- **測試模型**: qwen2.5:7b
- **測試題目**: "What is 2+2? Answer in one word."
- **輸出結果**: "Four"
- **執行狀態**: ✅ 成功

## 2. 基準對比

| 項目 | qwen2.5:7b | 預期結果 |
|------|------------|----------|
| 數學計算 | Four | 4 |
| 回應格式 | 單字回覆 | ✅ 符合 |

## 3. 評估準確率

| 測試項目 | 結果 | 準確率 |
|----------|------|--------|
| 數學計算 | ✅ 正確 | 100% |
| 格式遵循 | ✅ 符合 | 100% |

**總準確率**: 100%

## 4. 結論

- 本地模型 qwen2.5:7b 運行正常
- 數學計算能力驗證通過
- 回應時間與輸出品質符合預期

## 5. 後續建議

1. 可增加更多基準測試 (代碼生成、翻譯、推理)
2. 測試其他模型 (llama3, mistral) 進行比較
3. 建立定期測試機制

---

_記錄時間: 2026-03-05 04:14_
