# 數據 Schema 定義

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Skill Usage Record",
  "type": "object",
  "required": ["agent", "skill", "timestamp"],
  "properties": {
    "agent": {
      "type": "string",
      "description": "Agent 名稱"
    },
    "skill": {
      "type": "string",
      "description": "技能名稱"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO8601 時間戳"
    },
    "context": {
      "type": "string",
      "description": "應用場景"
    },
    "success": {
      "type": "boolean",
      "description": "是否成功"
    },
    "rating": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "description": "滿意度 1-5"
    },
    "duration_seconds": {
      "type": "integer",
      "minimum": 0,
      "description": "完成時間（秒）"
    }
  }
}
```

## 數據驗證規則

| 欄位 | 必填 | 類型 | 範圍 |
|------|------|------|------|
| agent | ✅ | string | - |
| skill | ✅ | string | - |
| timestamp | ✅ | ISO8601 | - |
| context | ❌ | string | - |
| success | ❌ | boolean | true/false |
| rating | ❌ | integer | 1-5 |
| duration_seconds | ❌ | integer | 0+ |

## 示例數據

```json
{
  "agent": "Agent_Builder",
  "skill": "需求分析",
  "timestamp": "2026-02-16T18:30:00Z",
  "context": "新Agent設計",
  "success": true,
  "rating": 5,
  "duration_seconds": 300
}
```
