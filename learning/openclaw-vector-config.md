# OpenClaw 向量資料庫配置

**版本**: v1.0
**日期**: 2026-02-18

---

## 🎯 配置目標

1. 自動讀取本地向量資料夾
2. 統一 Embedding 模型設定
3. 支援多設備同步

---

## 📁 目錄結構

```
~/.openclaw/
├── config/
│   └── vector-db.yaml
├── vectors/
│   ├── notion-knowledge/
│   │   ├── index/
│   │   └── metadata/
│   └── retrieval_feedback/
│       ├── index/
│       └── metadata/
└── memory/
```

---

## ⚙️ 配置檔案

### vector-db.yaml

```yaml
# OpenClaw 向量資料庫配置
# 版本: 1.0

# ============================================
# 基本設定
# ============================================

# 啟用向量功能
enabled: true

# 向量資料庫類型
vector_db:
  type: "chroma"  # chroma, faiss, lancedb
  persist_directory: "~/.openclaw/vectors"

# ============================================
# Embedding 模型設定
# ============================================

embedding:
  # 模型類型: local, openai, voyage
  provider: "local"
  
  # 本地模型 (Ollama)
  model: "nomic-embed-text"
  
  # 模型參數
  dimensions: 768
  batch_size: 32
  
  # 備用模型
  fallback:
    - "bge-m3"
    - "sentence-transformers/all-MiniLM-L6-v2"

# ============================================
# 檢索設定
# ============================================

retrieval:
  # 預設檢索數量
  default_top_k: 5
  
  # 相似度閾值
  similarity_threshold: 0.7
  
  # 混合搜尋權重
  hybrid_weights:
    semantic: 0.7
    keyword: 0.3

# ============================================
# 資料庫集合
# ============================================

collections:
  - name: "notion-knowledge"
    description: "Notion 筆記向量庫"
    path: "~/.openclaw/vectors/notion-knowledge"
    enabled: true
    
  - name: "retrieval_feedback"
    description: "檢索反饋資料庫"
    path: "~/.openclaw/vectors/retrieval_feedback"
    enabled: true

# ============================================
# 同步設定
# ============================================

sync:
  # 自動同步開關
  auto_sync: true
  
  # 同步間隔 (分鐘)
  sync_interval: 60
  
  # 雲端同步 (可選)
  cloud:
    enabled: false
    provider: "icloud"  # icloud, dropbox, google-drive
    remote_path: "/OpenClaw/vectors"

# ============================================
# 反饋學習設定
# ============================================

feedback:
  # 啟用反饋收集
  enabled: true
  
  # 收集項目
  collect:
    - query
    - results
    - relevance_rating
    - click_through
  
  # 自動優化 (實驗性)
  auto_optimize: false
  
  # 優化觸發閾值
  optimization_threshold:
    min_queries: 10
    min_rating: 3.5

# ============================================
# 效能設定
# ============================================

performance:
  # 快取設定
  cache:
    enabled: true
    ttl: 3600  # 秒
    
  # 預熱設定
  warmup:
    enabled: true
    on_startup: true
    
  # 並行處理
  parallel:
    enabled: true
    max_workers: 4
```

---

## 🔧 使用方式

### 1. 放置配置檔

```bash
mkdir -p ~/.openclaw/config
cp vector-db.yaml ~/.openclaw/config/
```

### 2. 設定環境變數

```bash
# Ollama Embedding 模型
export OLLAMA_EMBED_MODEL="nomic-embed-text"

# 或使用 HuggingFace
export HF_EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
```

### 3. 初始化向量資料庫

```python
from openclaw.vector import VectorDB

# 初始化
db = VectorDB(config_path="~/.openclaw/config/vector-db.yaml")

# 建立索引
db.build_index()

# 開始使用
results = db.search("你的查詢", top_k=5)
```

---

## 📋 檢索範例

### Python 使用

```python
from openclaw.vector import VectorDB
from openclaw.embedding import LocalEmbedding

# 初始化
embedding = LocalEmbedding(model="nomic-embed-text")
db = VectorDB(persist_dir="~/.openclaw/vectors")

# 搜尋
results = db.search(
    query="海膽市場價格",
    collection="notion-knowledge",
    top_k=5
)

# 記錄反饋
db.log_feedback(
    query="海膽市場價格",
    results=results,
    relevant=True,
    rating=5
)
```

### 命令列使用

```bash
# 搜尋
openclaw vector search "AI 系統架構"

# 新增文件
openclaw vector add --collection notion-knowledge --file /path/to/note.md

# 查看統計
openclaw vector stats
```

---

## 🔄 多設備同步

### iCloud 同步

```yaml
cloud:
  enabled: true
  provider: "icloud"
  remote_path: "/OpenClaw/vectors"
```

### 手動同步

```bash
# 匯出
openclaw vector export --output ./vectors_backup/

# 匯入
openclaw vector import --input ./vectors_backup/
```

---

## ⚠️ 注意事項

1. **向量空間對齊**: 確保所有設備使用相同 Embedding 模型
2. **同步延遲**: 雲端同步可能有延遲，建議重要操作前先本地同步
3. **儲存空間**: 向量資料會佔用空間，約每 1000 個文檔 1MB

---

## 📝 變更日誌

| 版本 | 日期 | 變更 |
|------|------|------|
| v1.0 | 2026-02-18 | 初始版本 |

---

*記錄時間: 2026-02-18*
