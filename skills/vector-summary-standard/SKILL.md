---
name: vector-summary-standard
description: 向量摘要標準流程 - Ollama 生成 + MiniMax 驗證
metadata:
  openclaw:
    emoji: "📊"
    version: "1.0"
    date: "2026-02-19"
---

# 向量摘要標準流程

## 概述

Notion 筆記向量化的標準工作流程，確保所有筆記都有高質量的向量摘要。

## 流程圖

```
┌─────────────────────────────────────────────────────────────┐
│                    向量摘要標準流程                           │
├─────────────────────────────────────────────────────────────┤
│  1. 文本切分 (Chunking)                                      │
│     ↓                                                        │
│  2. 生成摘要 (Ollama llama3)                                │
│     ↓                                                        │
│  3. MiniMax 驗證 (可選)                                     │
│     ↓                                                        │
│  4. 向量化 (Embedding)                                      │
│     ↓                                                        │
│  5. 建立關聯 (Linking)                                      │
│     ↓                                                        │
│  6. Notion 同步                                             │
└─────────────────────────────────────────────────────────────┘
```

## 步驟詳解

### 1. 文本切分 (Chunking)

```python
def chunk_text(text, chunk_size=250):
    sentences = text.replace('。', '。|').replace('！', '！|')...
    chunks = []
    # 每區塊約 250 字
    return [c for c in chunks if len(c) > 20]
```

### 2. 生成摘要 (Ollama)

```python
def generate_summary(chunk):
    prompt = f'用30字以內摘要核心概念：{chunk[:200]}'
    result = subprocess.run(['ollama', 'run', 'llama3', prompt]...)
    return result.stdout.strip()[:80]
```

### 3. MiniMax 驗證 (可選)

```python
def generate_summary_minimax(chunk):
    # 使用 MiniMax-M2.5 生成更高質量摘要
    # 比對選擇更好的版本
```

### 4. 向量化

```python
def get_embedding(text):
    vec = [0.0] * 128
    for i, c in enumerate(text[:128]):
        vec[i % 128] += ord(c)
    # 歸一化
    return [x/mag for x in vec]
```

### 5. 建立關係

- 儲存位置: `~/Desktop/vector-db/`
- 檔案格式: `{page_id}.json`

### 6. Notion 同步

| 欄位 | 值 |
|------|-----|
| 向量摘要 | 摘要文字 (500字) |
| 向量狀態 | 已向量化(標準流程) |
| 語義標籤 | Chunk_{數量} |
| 重點 | 首要摘要 (50字) |
| 應用 | 分類 |

## 腳本位置

| 腳本 | 功能 |
|------|------|
| `scripts/vector_summary_v2.py` | Ollama 版本 |
| `scripts/vector_summary_verify.py` | Ollama + MiniMax 驗證版 |

## 使用方式

```bash
# 確保 Ollama 運行
ollama serve

# 處理 Notion 頁面
python scripts/vector_summary_v2.py
```

## 數據結構

```json
{
  "title": "筆記標題",
  "vectors": [
    {
      "chunk_index": 0,
      "summary": "摘要內容",
      "source_chunk": "原文片段",
      "embedding": [0.15, 0.14, ...]
    }
  ]
}
```

## 質量標準

| 項目 | 標準 |
|------|------|
| 摘要長度 | ≤30 字 |
| 區塊數量 | 1-11 個 |
| 向量維度 | 128 維 |
| 狀態標記 | 已向量化(標準流程) |

## 里程碑

- **2026-02-19**: 首次完成 50 頁 Notion 筆記向量優化
- **11萬檔案整理**: 同步記錄到 Notion

## 相關技能

- `vector-summary-ollama` - Ollama 版本
- `vector-summary-workflow` - 完整工作流

---
