---
name: aeo-rag-search
description: |
  AEO 網站 RAG 檢索系統。當需要搜尋 AI 教學內容、找提示詞、查詢工具設定時使用。
  功能：(1) 全文搜尋網站內容 (2) 語意檢索 (3) 相關文章推薦 (4) API 供其他 AI 存取。
  適用場景：(1) 搜尋 AI 提示詞 (2) 查詢工具設定教學 (3) 讓其他 AI 讀取網站內容
metadata:
  {
    "openclaw": { "emoji": "🔍", "requires": { "anyTools": ["exec", "web_fetch"] } },
  }
---

# AEO RAG Search

讓 AI 更容易找到網站內容的檢索系統

## 快速使用

```bash
# 搜尋內容
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_rag.py search "OpenClaw"

# 建立索引
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_rag.py index

# 啟動 API
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_rag.py serve
```

## OpenClaw 整合

### 搜尋內容

```javascript
// 搜尋
exec({
  command: "python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_rag.py search 'OpenClaw'"
})
```

### API 呼叫

```bash
# 搜尋
curl "http://localhost:3002/api/search?q=OpenClaw"

# 統計
curl "http://localhost:3002/api/stats"
```

## API 端點

| Endpoint | 說明 |
|----------|------|
| `/api/search?q=關鍵字` | 搜尋內容 |
| `/api/stats` | 統計資訊 |

## 搜尋結果格式

```json
{
  "query": "OpenClaw",
  "count": 5,
  "results": [
    {
      "id": "2026-03-02_openclaw-系統提示詞",
      "title": "OpenClaw 系統提示詞",
      "type": "system_prompt",
      "score": 33,
      "matched_chunks": [
        {
          "text": "你是 OpenClaw...",
          "score": 10
        }
      ]
    }
  ]
}
```

## 使用範例

### 範例 1: 找提示詞

```
User: 找 Claude 提示詞

exec: aeo_rag.py search "Claude"

結果:
1. Claude AI 助手 (分數: 25)
2. GPT 提示詞工程師 (分數: 20)
3. ...
```

### 範例 2: 找工具教學

```
User: n8n 怎麼用

exec: aeo_rag.py search "n8n"

結果:
1. n8n 自動化設定 (分數: 30)
2. 工作流自動化 (分數: 20)
```

### 範例 3: 其他 AI 存取

```python
import requests

# 讓 Claude/GPT 讀取網站
def search_aeo(query):
    response = requests.get(
        f"http://localhost:3002/api/search",
        params={"q": query}
    )
    return response.json()

# 使用
results = search_aeo("OpenClaw 安裝")
for r in results["results"]:
    print(f"- {r['title']}")
```

## 索引統計

```
內容數: 100 篇
Chunks: 122 個
```

## 搜尋特點

1. **關鍵字匹配** - 標題、內文、標籤
2. **分數排序** - 最相關的排在前面
3. **摘要擷取** - 顯示相關段落
4. **類型過濾** - 可按 system_prompt/tool_setup/workflow 篩選
