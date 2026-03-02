# 史萊姆學習記憶優化系統 - 記憶層設計

## 1. 記憶層架構

### 1.1 整體架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                        查詢輸入                                  │
│                   (自然語言問題 / 關鍵字)                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      記憶層管理器                                │
│                  (Memory Layer Manager)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Query      │  │  Fusion     │  │  Sync       │              │
│  │  Processor  │  │  Engine     │  │  Coordinator│              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   SQLite-Vec  │  │   MEMORY.md   │  │    Notion     │
│   (向量檢索)  │  │  (本地筆記)    │  │  (雲端知識庫)  │
└───────────────┘  └───────────────┘  └───────────────┘
     向量相似度        結構化知識           長文檔庫
     語義匹配          快速查詢             團隊共享
```

### 1.2 組件職責

| 組件 | 職責 | 適用場景 |
|------|------|----------|
| **SQLite-Vec** | 向量嵌入儲存與語義檢索 | 語義相似搜索、概念匹配 |
| **MEMORY.md** | 本地結構化筆記、快速訪問 | 個人筆記、靈感記錄 |
| **Notion** | 雲端知識庫、長文檔管理 | 團隊共享、長期歸檔 |

### 1.3 協作流程

```
新增知識時:
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   輸入來源   │────▶│  分類路由     │────▶│  目標儲存    │
│ (對話/閱讀) │     │  (自動判斷)   │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                     ┌────────────────────────────┘
                     │ 生成向量嵌入 + 同步
                     ▼
              ┌──────────────┐
              │  SQLite-Vec  │ (同步索引)
              └──────────────┘
```

## 2. 儲存格式規範

### 2.1 SQLite-Vec 表結構

```sql
-- 主要知識向量表
CREATE TABLE knowledge_vectors (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id        TEXT UNIQUE NOT NULL,        -- 知識塊唯一ID
    content         TEXT NOT NULL,               -- 原始文本內容
    embedding       BLOB NOT NULL,                -- 向量嵌入 (384/768維)
    source_type     TEXT NOT NULL,               -- 來源: 'memory', 'notion', 'learned'
    source_id       TEXT,                        -- 來源記錄ID
    topic           TEXT,                        -- 主題標籤
    tags            TEXT,                        -- JSON 陣列標籤
    importance      INTEGER DEFAULT 1,           -- 重要性 1-5
    access_count    INTEGER DEFAULT 0,           -- 訪問次數
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 向量索引 (使用 sqlite-vec)
CREATE VIRTUAL TABLE knowledge_vec_idx USING vec0(
    embedding FLOAT[768],
    chunk_id TEXT UNIQUE
);

-- 學習記錄表 (追蹤 AI 學習歷程)
CREATE TABLE learning_records (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question        TEXT NOT NULL,               -- 學習的問題
    answer          TEXT NOT NULL,               -- 產出的答案
    feedback        TEXT,                        -- 用戶反饋
    sources         TEXT,                        -- 參考來源 (JSON)
    model_used      TEXT,                        -- 使用的模型
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 索引優化
CREATE INDEX idx_topic ON knowledge_vectors(topic);
CREATE INDEX idx_source ON knowledge_vectors(source_type);
CREATE INDEX idx_importance ON knowledge_vectors(importance DESC);
```

### 2.2 MEMORY.md 文件規範

```markdown
# MEMORY.md - 史萊姆學習記憶

## 索引
- [[概念清單]]
- [[常用指令]]
- [[學習筆記]]

---

## 重要概念 [重要性: 5]

### 核心記憶
- **學習策略**: 主動回憶 > 被動閱讀
- **知識分類**: 概念 → 流程 → 案例

### 技術筆記
<!-- 可嵌入代碼塊 -->
\`\`\`python
def slime_learn(query):
    return retrieve_and_synthesize(query)
\`\`\`

---

## 待學習 [標籤: #pending]

- [ ] 新主題 1
- [ ] 新主題 2
```

### 2.3 Notion 數據模型

```
Notion Database: 知識庫
├── 屬性
│   ├── Name (標題)
│   ├── Type (選擇): 概念/流程/案例/FAQ
│   ├── Status (選擇): 草稿/已整理/已審核
│   ├── Tags (多選)
│   ├── Importance (數字): 1-5
│   └── Related (關聯)
│
└── 頁面內容
    ├── Summary (摘要)
    ├── Content (正文)
    └── RelatedLinks (相關鏈接)
```

### 2.4 統一元數據格式

```json
{
  "chunk_id": "slime_kb_001",
  "title": "學習記憶優化原則",
  "content": "...",
  "embedding": [0.123, -0.456, ...],
  "metadata": {
    "source": "notion",
    "source_id": "notion_page_abc123",
    "topic": "learning",
    "tags": ["optimization", "memory", "AI"],
    "importance": 4,
    "language": "zh-TW",
    "created_at": "2026-02-27T05:00:00Z",
    "updated_at": "2026-02-27T05:00:00Z"
  }
}
```

## 3. 檢索流程

### 3.1 統一檢索入口

```
用户查詢
    │
    ▼
┌─────────────────┐
│ Query Processor │
│ • 意圖識別      │
│ • 關鍵字提取    │
│ • 向量編碼      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  路由策略判斷   │
│                 │
│ IF 語義搜索     │──▶ 向量檢索 (SQLite-Vec)
│ IF 精確匹配     │──▶ 關鍵字搜索 (MEMORY.md)
│ IF 文檔查詢     │──▶ Notion API
│ IF 混合查詢     │──▶ Fusion Engine
└────────┬────────┘
         │
         ▼
    結果融合排序
         │
         ▼
    返回答案 + 引用來源
```

### 3.2 檢索優先級

| 查詢類型 | 優先順序 | 引擎 |
|----------|----------|------|
| 語義相似 | 1st | SQLite-Vec |
| 精確關鍵字 | 1st | MEMORY.md grep |
| 長文檔總結 | 2nd | Notion |
| 綜合回答 | 融合 | Fusion Engine |

### 3.3 向量檢索實現

```python
# 檢索偽代碼
async def semantic_search(query: str, top_k: int = 5):
    # 1. 生成查詢向量
    query_embedding = await encode_embedding(query)
    
    # 2. SQLite-Vec 向量搜索
    results = await vec_search(
        embedding=query_embedding,
        limit=top_k,
        filter="importance >= 2"  # 過濾低重要性
    )
    
    # 3. 重排序 (Rerank)
    reranked = await rerank(query, results)
    
    # 4. 獲取完整上下文
    return await fetch_full_context(reranked)
```

### 3.4 結果融合策略

```python
# 多來源結果融合
def fuse_results(semantic_results, keyword_results, notion_results):
    scored_results = []
    
    # 向量檢索結果 (權重: 0.5)
    for item in semantic_results:
        score = item.similarity * 0.5
        scored_results.append({**item, score})
    
    # 關鍵字結果 (權重: 0.3)
    for item in keyword_results:
        score = item.relevance * 0.3
        scored_results.append({**item, score})
    
    # Notion 結果 (權重: 0.2)
    for item in notion_results:
        score = item.relevance * 0.2
        scored_results.append({**item, score})
    
    # 按分數排序返回
    return sorted(scored_results, key=lambda x: x.score, reverse=True)
```

### 3.5 檢索流程時序

```
Time │
     │
 0ms │────────── Query Input ──────────
     │          │
     │          ▼
 10ms │────── Embedding Encode ───────
     │          │
     │          ▼
 50ms │──▶ SQLite-Vec Search (並行)
     │          │
     │          ▼
 80ms │──▶ MEMORY.md Grep (並行)
     │          │
     │          ▼
120ms │──▶ Notion Query (並行)
     │          │
     │          ▼
150ms │────── Fusion & Rank ───────────
     │          │
     │          ▼
180ms │────── Response + Sources ──────
     │
```

## 4. 同步機制

### 4.1 寫入時同步

```
新增知識
    │
    ├──▶ SQLite-Vec (向量索引)
    │
    ├──▶ MEMORY.md (本地備份)
    │
    └──▶ Notion (可選雲端同步)
```

### 4.2 定期同步排程

| 時間 | 任務 |
|------|------|
| 05:00 | Notion → 本地同步 |
| 18:00 | MEMORY.md 備份 |
| 20:00 | 向量索引重建 |

## 5. 配置範例

```yaml
# slime-memory-config.yaml
memory:
  vector_db:
    type: sqlite-vec
    path: ~/.slime/knowledge.db
    dimensions: 768
  
  local_notes:
    path: ~/.openclaw/workspace/slime-system/MEMORY.md
    auto_backup: true
  
  notion:
    enabled: true
    database_id: ${NOTION_KB_DATABASE_ID}
    sync_interval: 3600  # seconds
  
  retrieval:
    default_top_k: 5
    fusion_weights:
      semantic: 0.5
      keyword: 0.3
      notion: 0.2
```

---

*最後更新: 2026-02-27*
*維護者: Wiki (知識庫管理員)*
