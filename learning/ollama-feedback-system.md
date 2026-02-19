# Ollama 反饋學習系統

**日期**: 2026-02-18
**功能**: 追蹤檢索準確率，讓 Ollama 學習並優化

---

## 📊 系統架構

```
用戶查詢
    │
    ▼
Ollama 檢索
    │
    ▼
用戶評分 (relevant: True/False, rating: 1-5)
    │
    ▼
反饋資料庫 (retrieval_feedback)
    │
    ▼
效能分析 + 優化建議
    │
    ▼
Ollama 學習改進
```

---

## 🎯 功能

### 1. 記錄檢索結果

每次檢索後記錄：
- 查詢內容
- 結果數量
- 相關數量
- 用戶評分

### 2. 效能分析

分析：
- 總查詢數
- 平均相關性
- 平均評分
- 熱門查詢

### 3. 優化建議

根據數據給出建議：
- 調整向量模型參數
- 增加訓練數據
- 增加語義標籤

---

## 📁 檔案位置

```
~/openclaw/workspace/scripts/
├── ollama_feedback.py      # 反饋學習腳本
├── notion_chroma_sync.py   # Notion 同步
└── retrieval_test.py       # 檢索測試
```

---

## 🚀 使用方式

### 1. 記錄反饋

```python
from ollama_feedback import log_retrieval

log_retrieval(
    feedback_collection,
    query="海膽價格",
    results=["doc1", "doc2"],
    relevance=[
        {"doc_id": "doc1", "relevant": True, "rating": 5},
        {"doc_id": "doc2", "relevant": False, "rating": 2}
    ]
)
```

### 2. 分析效能

```python
from ollama_feedback import analyze_performance

perf = analyze_performance(feedback_collection)
print(f"平均評分: {perf['avg_rating']}")
```

### 3. 優化檢索

```python
from ollama_feedback import improve_retrieval

improve_retrieval(feedback_collection)
```

---

## 📈 數據追蹤

| 指標 | 說明 |
|------|------|
| total_queries | 總查詢次數 |
| avg_relevant | 平均相關結果數 |
| avg_rating | 平均評分 (1-5) |
| popular_queries | 熱門查詢排行 |

---

## 🔄 持續優化

每次用戶互動：
1. 記錄查詢與結果
2. 收集用戶評分
3. 分析效能數據
4. 產生優化建議
5. 改進檢索策略

---

*記錄時間: 2026-02-18*
