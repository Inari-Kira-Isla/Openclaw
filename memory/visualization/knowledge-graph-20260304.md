# 知識圖譜視覺化數據結構

## 數據結構 (JSON Schema)

```json
{
  "nodes": [
    {
      "id": "string",
      "label": "string",
      "type": "agent|skill|tool|memory|user",
      "group": "string",
      "metadata": {
        "status": "active|idle|error",
        "lastUpdated": "ISO8601"
      }
    }
  ],
  "edges": [
    {
      "source": "node_id",
      "target": "node_id", 
      "relation": "uses|manages|learns_from|collaborates_with"
    }
  ]
}
```

## 節點佈局配置

| 層級 | 節點類型 | 位置 |
|------|----------|------|
| L1 | Agent (Kira, Nei, Cynthia, 史萊姆, Team, Evolution) | 中央 |
| L2 | Skill (gscc_classifier, knowledge_search, etc.) | 環繞 L1 |
| L3 | Tool (Telegram, Notion, Gateway) | 外圍 |

## 前端顯示格式

- **React Flow** / **D3.js** 相容
- 力導向佈局 (Force-directed)
- 節點顏色：
  - Agent: #6366f1 (indigo)
  - Skill: #10b981 (emerald)
  - Tool: #f59e0b (amber)
  - Memory: #8b5cf6 (violet)

## 預設視圖

- 縮放：fit view
- 節點間距：150px
- 顯示標籤：true

---
_更新: 2026-03-04 06:03_
