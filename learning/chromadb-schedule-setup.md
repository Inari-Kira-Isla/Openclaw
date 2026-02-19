# Notion → ChromaDB 定時同步設定

**日期**: 2026-02-18

---

## 同步腳本位置

```
~/Desktop/chromadb-env/bin/python ~/openclaw/workspace/scripts/notion_chroma_sync.py
```

---

## 執行方式

### 手動執行
```bash
source ~/Desktop/chromadb-env/bin/activate
python ~/openclaw/workspace/scripts/notion_chroma_sync.py
```

### crontab 設定

```bash
# 編輯 crontab
crontab -e

# 每日 18:00 自動同步
0 18 * * * source ~/Desktop/chromadb-env/bin/activate && python ~/openclaw/workspace/scripts/notion_chroma_sync.py >> ~/logs/notion-sync.log 2>&1
```

---

## ChromaDB 查詢測試

```python
import sys
sys.path.insert(0, "~/Desktop/chromadb-env/lib/python3.12/site-packages")

import chromadb

client = chromadb.Client(Settings(
    persist_directory="~/Desktop/chromadb-data",
    anonymized_telemetry=False
))

collection = client.get_collection("notion-knowledge")

# 查詢
results = collection.query(
    query_texts=["你的查詢內容"],
    n_results=5
)

# 顯示結果
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"標題: {meta.get('title')}")
    print(f"內容: {doc[:200]}...")
    print("---")
```

---

*記錄時間: 2026-02-18*
