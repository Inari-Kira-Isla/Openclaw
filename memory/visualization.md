# Visualization - Knowledge Graph Structure
Updated: 2026-03-05 06:07

## 知識圖譜數據結構

### 節點定義 (JSON)

```json
{
  "graph": {
    "version": "2.0",
    "lastUpdate": "2026-03-05T06:07:00+08:00",
    "layout": "force-directed"
  },
  "nodes": [
    {
      "id": "core-team",
      "label": "5 Bot 團隊",
      "type": "core",
      "importance": 10,
      "tags": ["kira", "nei", "cynthia", "史萊姆", "team", "evolution"]
    },
    {
      "id": "core-skills",
      "label": "Skills 系統",
      "type": "core",
      "importance": 9,
      "tags": ["skills-over-agents", "mcp", "automation"]
    },
    {
      "id": "core-memory",
      "label": "記憶層",
      "type": "core",
      "importance": 9,
      "tags": ["memory", "vector", "rag"]
    },
    {
      "id": "core-workflow",
      "label": "工作流",
      "type": "core",
      "importance": 8,
      "tags": ["workflow", "automation", "cron"]
    },
    {
      "id": "app-bni",
      "label": "BNI 商業",
      "type": "app",
      "importance": 7,
      "tags": ["notion", "reminders", "crm"]
    },
    {
      "id": "app-content",
      "label": "內容生成",
      "type": "app",
      "importance": 6,
      "tags": ["seo", "aeo", "twitter"]
    }
  ],
  "edges": [
    {"from": "core-team", "to": "core-skills", "relation": "uses", "weight": 10},
    {"from": "core-team", "to": "core-memory", "relation": "manages", "weight": 9},
    {"from": "core-skills", "to": "core-workflow", "relation": "powers", "weight": 8},
    {"from": "core-memory", "to": "core-skills", "relation": "feeds", "weight": 7},
    {"from": "core-workflow", "to": "app-bni", "relation": "automates", "weight": 6},
    {"from": "core-workflow", "to": "app-content", "relation": "generates", "weight": 5}
  ]
}
```

### 前端顯示配置

| 項目 | 配置 |
|------|------|
| 框架 | D3.js / React Flow |
| 布局 | 力導向 (Force-directed) |
| 節點大小 | importance × 10px |
| 顏色 | core=#4A90E2, app=#7ED321, topic=#F5A623 |
| 交互 | 點擊展開 / 拖拽 / 縮放 / 搜尋 |

### 節點佈局層次

```
        ┌─────────────┐
        │  core-team  │ ← 中心 (5 Bot)
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│skills │  │memory │  │workflow│
└───┬───┘  └───┬───┘  └───┬───┘
    │          │          │
    └──────────┼──────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐
│  BNI  │  │content│
└───────┘  └───────┘
```

### 節點統計

| 類型 | 數量 |
|------|------|
| Core | 4 |
| App | 2 |
| 總計 | 6 |

---
_記錄時間: 2026-03-05 06:07 GMT+8_
