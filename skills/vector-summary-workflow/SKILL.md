---
name: vector-summary-workflow
description: 向量摘要完整工作流程 - Ollama + MiniMax
metadata: {"openclaw": {"emoji": "📊"}}
---

# 向量摘要完整工作流程

## 概述

使用 Ollama 本地生成向量摘要，配合 MiniMax 驗證優化。

## 工作流程

```
1. 文本切分 (Chunking)
   ↓
2. 生成摘要 (Ollama llama3)
   ↓
3. MiniMax 驗證 (可選)
   ↓
4. 向量化 (Embedding)
   ↓
5. 建立關聯 (本地儲存)
   ↓
6. 檢索 (相似度比對)
```

## 腳本

### 主要腳本

| 腳本 | 功能 |
|------|------|
| `vector_summary_v2.py` | Ollama 版本 |
| `vector_summary_verify.py` | Ollama + MiniMax 驗證版 |

## 配置

### Ollama

```bash
# 確保運行
ollama serve

# 模型
llama3:latest (4.7GB)
```

### MiniMax (驗證用)

```bash
# 環境變數
export MINIMAX_API_KEY="your-key"
```

## 使用方式

```bash
# 使用 Ollama 處理
python scripts/vector_summary_v2.py

# 使用 Ollama + MiniMax 驗證
python scripts/vector_summary_verify.py
```

## 數據存儲

- **本地向量庫**: `~/Desktop/vector-db/`
- **每筆記錄**:
  - chunk_index
  - summary (摘要)
  - source_chunk (原文)
  - embedding (128維向量)

## Notion 同步

- 向量摘要
- 向量狀態
- 語義標籤
- 重點
- 應用分類

## 狀態標記

| 標記 | 意義 |
|------|------|
| 已向量化 | 基礎處理 |
| 已向量化(標準流程) | Ollama 完整流程 |
| 已向量化(Ollama+MiniMax) | 驗證優化版 |

---
