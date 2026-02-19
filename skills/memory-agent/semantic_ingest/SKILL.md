---
name: semantic_ingest
description: 語義資料攝入與儲存。當需要將資訊以語義方式存入記憶系統時觸發，包括：向量化處理、分塊策略、索引建立、元資料管理。
---

# Semantic Ingest

## 攝入流程

```
原始資料 → 預處理 → 向量化 → 分塊 → 索引 → 儲存
```

## 預處理

### 文本清理
- 移除多餘空白
- 標準化編碼
- 去除無關字符

### 結構化提取
```json
{
  "content": "文本內容",
  "source": "來源識別",
  "type": "類型",
  "tags": ["標籤"],
  "metadata": {}
}
```

## 向量化

### 模型選擇
| 模型 | 維度 | 適用場景 |
|------|------|----------|
| text-embedding-3-small | 1536 | 通用 |
| text-embedding-3-large | 3072 | 高精度 |
| bge-m3 | 1024 | 多語言 |

### 分塊策略

| 策略 | 大小 | 重疊 | 適用場景 |
|------|------|------|----------|
| Fixed | 512 | 50 | 結構化文本 |
| Semantic | 動態 | 動態 | 語義完整 |
| Recursive | 遞歸 | 100 | 複雜文檔 |

## 索引建立

### 元資料索引
```json
{
  "id": "unique-id",
  "content": "原始內容",
  "embedding": [向量],
  "chunk_index": 1,
  "total_chunks": 5,
  "source": "source-id",
  "created_at": "timestamp",
  "tags": []
}
```

## 儲存優化

- 批量攝入（建議 100 條/批）
- 異步處理
- 失敗重試
- 進度追蹤
