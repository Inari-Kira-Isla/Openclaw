---
name: vector-summary-ollama
description: 使用本地 Ollama 生成向量摘要
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["ollama"]}}}
---

# 向量摘要 Workflow (Ollama 版本)

## 功能
使用本地 Ollama 生成向量摘要，用於 Notion 筆記優化

## 工作流程

### 1. 文本切分 (Chunking)
```
將長文本切分成多個段落 (每段約 250 字)
```

### 2. 生成摘要 (Summarization)
```
使用 Ollama llama3 生成精簡摘要
```

### 3. 向量化 (Embedding)
```
將摘要轉為 128 維向量
```

### 4. 建立關聯 (Linking)
```
儲存到 ~/Desktop/vector-db/
```

### 5. 檢索 (Retrieval)
```
相似度比對檢索
```

## 使用方式

```bash
# 處理最新 Notion 頁面
python scripts/vector_summary_ollama.py

# 處理所有頁面
python scripts/vector_summary_ollama.py --all
```

## 腳本位置

- `scripts/vector_summary_v2.py` - Ollama 版本
- `scripts/vector_summary_minimax.py` - MiniMax 版本

## 模型選擇

| 版本 | 模型 | 品質 | 速度 | 成本 |
|------|------|------|------|------|
| MiniMax | M2.5 | 高 | 慢 | API 費用 |
| Ollama | llama3 | 中 | 快 | 免費 |

## 建議流程

1. **首次** - 使用 MiniMax 確保高品質
2. **後續** - 使用 Ollama 自動化

---
