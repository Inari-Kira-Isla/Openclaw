# OpenClaw ↔ n8n ↔ 多模型 雙向循環

**日期**: 2026-02-19
**來源**: Joe 分享的架構

---

## 核心概念

```
OpenClaw (Orchestrator)
    │
    ▼ webhook
n8n (Pipeline & Router)
    │
    ├── Gemini API
    ├── Claude API
    └── Fallback
    │
    ▼ callback
OpenClaw
```

---

## 優勢

| 項目 | 說明 |
|------|------|
| 模型分工 | 本地快速、Gemini 即時、Claude 複雜 |
| 自動 Fallback | Gemini 失敗 → Claude → 本地 |
| 永遠在線 | 不會 401 卡死 |

---

## 已建立

| 檔案 | 說明 |
|------|------|
| `skills/openclaw-n8n-multimodel/SKILL.md` | 完整架構文檔 |
| `n8n/openclaw-multimodel.json` | n8n workflow |

---

## 使用方式

### 發送任務到 n8n

```json
{
  "model": "gemini",
  "prompt": "分析 BTC 趨勢",
  "context": "..."
}
```

### OpenClaw 回傳

```json
{
  "result": "分析結果...",
  "source": "gemini"
}
```

---

## 檔案位置

- Skill: `skills/openclaw-n8n-multimodel/SKILL.md`
- n8n: `~/Desktop/n8n_workflows/openclaw-multimodel.json`

---
