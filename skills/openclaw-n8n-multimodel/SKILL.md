---
name: openclaw-n8n-multimodel
description: OpenClaw ↔ n8n ↔ 多模型雙向循環架構
metadata:
  openclaw:
    emoji: "🔄"
    version: "1.0"
    date: "2026-02-19"
---

# OpenClaw ↔ n8n ↔ 多模型 雙向循環架構

## 整體資料流

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenClaw (Orchestrator)                    │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │ 本地模型      │    │ Gemini       │    │ Claude      │    │
│  │ (快速反應)   │    │ (即時分析)   │    │ (複雜邏輯)  │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
└─────────────────────────────────────────────────────────────────┘
         ↑                        ↑                        ↑
         │                        │                        │
    ┌────┴────────────────────────┴────────────────────────┴────┐
    │                      n8n (Pipeline & Router)               │
    │                                                               │
    │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐    │
    │  │ Webhook     │ → │ Model       │ → │ Fallback   │    │
    │  │ Trigger     │   │ Router      │   │ Logic      │    │
    │  └─────────────┘   └─────────────┘   └─────────────┘    │
    └─────────────────────────────────────────────────────────────┘
```

---

## 架構組件

### 1. OpenClaw (Orchestrator)

| 功能 | 說明 |
|------|------|
| 任務分發 | 判斷任務類型，發送 webhook |
| 結果整合 | 接收 n8n 回傳，存入記憶 |
| 本地模型 | 快速反應、簡單任務 |

### 2. n8n (Pipeline & Router)

| 功能 | 說明 |
|------|------|
| Webhook Trigger | 接收 OpenClaw 請求 |
| Model Router | 根據任務選擇模型 |
| Fallback Logic | 自動切換模型 |
| API 整合 | Gemini / Claude API |

### 3. 多模型 (Specialist AI)

| 模型 | 擅長 | 場景 |
|------|------|------|
| 本地 Ollama | 快速反應 | 簡單對話、筆記 |
| Gemini | 即時分析 | 市場數據、搜尋 |
| Claude | 複雜邏輯 | Code 重構、推理 |

---

## 工作流設計

### Flow 1: OpenClaw 發送到 n8n

```
OpenClaw
    │
    ▼ POST webhook
n8n Webhook (openclaw-trigger)
    │
    ▼
n8n Model Router
    │
    ├── 簡單任務 → 直接處理 → 回傳 OpenClaw
    │
    ├── Gemini 任務 → Gemini API → 回傳 OpenClaw
    │
    └── Claude 任務 → Claude API → 回傳 OpenClaw
```

### Flow 2: Fallback 機制

```
IF Gemini 失敗
    → 呼叫 Claude
    → IF Claude 失敗
        → 回傳本地模型結果
```

---

## n8n Workflow 節點

### 節點 1: Webhook Trigger
- Path: `openclaw-trigger`
- Method: POST

### 節點 2: Router (Switch)
- 根據 `json.model` 判斷
  - `gemini` → Gemini flow
  - `claude` → Claude flow
  - `local` → 直接回傳

### 節點 3: Gemini HTTP Request
- URL: `https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent`
- Auth: API Key in env

### 節點 4: Claude HTTP Request
- URL: `https://api.anthropic.com/v1/messages`
- Auth: API Key in header

### 節點 5: Fallback Logic
- IF 失敗 → 切換模型
- IF 全部失敗 → 回傳錯誤

### 節點 6: HTTP Request (回傳 OpenClaw)
- POST 到 OpenClaw Gateway
- URL: `http://localhost:18789/agent/main/respond`

---

## 使用場景

### 場景 1: 市場分析

```
用戶: "分析 BTC 今日趨勢"
    │
    ▼
OpenClaw 判斷: 需要即時數據
    │
    ▼ POST webhook {task: "分析", context: "...", model: "gemini"}
    │
    ▼
n8n 接收 → 呼叫 Gemini API
    │
    ▼
Gemini 分析結果回傳
    │
    ▼
n8n POST 回 OpenClaw
    │
    ▼
OpenClaw 存入記憶 → 回覆用戶
```

### 場景 2: 程式重構

```
用戶: "重構這段 Python 代碼"
    │
    ▼
OpenClaw 判斷: 需要複雜邏輯
    │
    ▼ POST webhook {task: "重構", code: "...", model: "claude"}
    │
    ▼
n8n → Claude API
    │
    ▼
Claude 重構結果回傳
    │
    ▼
OpenClaw 存入記憶 → 回覆用戶
```

### 場景 3: 簡單任務

```
用戶: "天氣怎麼樣?"
    │
    ▼
OpenClaw 直接用本地模型回覆
    │
    (不需要發送到 n8n)
```

---

## API Key 設定

### n8n 環境變數

```bash
# Docker 環境
docker exec -e GEMINI_API_KEY="your-key" n8n
docker exec -e ANTHROPIC_API_KEY="your-key" n8n

# 或在 n8n credentials 中設定
```

### 安全原則

- ❌ 不要寫死在 workflow JSON 中
- ✅ 使用環境變數或 n8n credentials
- ✅ 定期輪換 API Key

---

## OpenClaw Gateway 設定

### 允許外部訪問

```yaml
# config.yaml
gateway:
  bind: "0.0.0.0"  # 允許外部訪問
  port: 18789
```

### 測試連接

```bash
# 從 n8n 容器測試
curl -X POST http://host.docker.internal:18789/agent/main/respond \
  -H "Content-Type: application/json" \
  -d '{"result": "test"}'
```

---

## 檔案清單

| 檔案 | 說明 |
|------|------|
| `n8n/openclaw-multimodel.json` | n8n workflow |
| `skills/openclaw-n8n-multimodel/SKILL.md` | Skill 文檔 |
| `learning/openclaw-n8n-architecture.md` | 學習筆記 |

---

## 下一步

- [ ] 設定 OpenClaw Gateway 允許外部訪問
- [ ] 建立 n8n Multimodel Workflow
- [ ] 測試雙向循環
- [ ] 監控與優化

---
