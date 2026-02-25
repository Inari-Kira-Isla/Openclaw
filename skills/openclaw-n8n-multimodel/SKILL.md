---
name: openclaw_n8n_multimodel
description: OpenClaw + n8n 多模型雙向循環架構。當需要設定或管理 OpenClaw 透過 n8n 調度多模型時觸發，包括：任務路由、模型選擇、Fallback 機制、Webhook 配置。
---

# OpenClaw + n8n 多模型架構

## 功能說明

透過 n8n 作為中間層，讓 OpenClaw 根據任務類型自動路由到最適合的 AI 模型（本地 Ollama / Gemini / Claude），並支援自動 Fallback 切換。

## 架構概覽

```
OpenClaw (決策層)
    ↓ POST webhook
n8n (路由層)
    ├── 簡單任務 → 直接處理 → 回傳
    ├── 即時分析 → Gemini API → 回傳
    └── 複雜邏輯 → Claude API → 回傳
```

## 工作流程

### 第一步：任務分發
- OpenClaw 分析用戶請求的任務類型
- 發送 POST webhook 到 n8n，包含任務內容和建議模型

### 第二步：n8n 模型路由
- Webhook Trigger 接收請求（path: `openclaw-trigger`）
- Switch 節點根據 `json.model` 欄位路由：
  - `local` → 直接回傳本地結果
  - `gemini` → 呼叫 Gemini API
  - `claude` → 呼叫 Claude API

### 第三步：模型執行
- Gemini：`https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent`
- Claude：`https://api.anthropic.com/v1/messages`

### 第四步：Fallback 處理
- 若首選模型失敗，自動切換備選模型
- Gemini 失敗 → Claude → 本地模型

### 第五步：結果回傳
- POST 回 OpenClaw Gateway：`http://localhost:18789/agent/main/respond`
- OpenClaw 存入記憶並回覆用戶

## 模型選擇邏輯

| 模型 | 擅長場景 | 適用任務 |
|------|----------|----------|
| 本地 Ollama | 快速反應 | 簡單對話、筆記 |
| Gemini | 即時分析 | 市場數據、搜尋 |
| Claude | 複雜邏輯 | 程式重構、推理 |

## 工具指引

```bash
# OpenClaw Gateway 設定（允許外部訪問）
# config.yaml:
#   gateway:
#     bind: "0.0.0.0"
#     port: 18789

# 從 n8n 容器測試連線
curl -X POST http://host.docker.internal:18789/agent/main/respond \
  -H "Content-Type: application/json" \
  -d '{"result": "test"}'
```

n8n Workflow 檔案：`n8n/openclaw-multimodel.json`

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| n8n Webhook 無回應 | 檢查 n8n 容器是否運行，確認 webhook path 正確 |
| Gemini API 失敗 | 自動 Fallback 到 Claude |
| Claude API 失敗 | Fallback 到本地模型 |
| 全部模型失敗 | 回傳錯誤訊息給用戶，記錄到日誌 |
| OpenClaw Gateway 連線失敗 | 檢查 port 18789，確認 bind 設定為 0.0.0.0 |
| API Key 無效 | 回傳認證錯誤，提示更新 credentials |

## 使用範例

- 「分析 BTC 今日趨勢」（路由到 Gemini，即時數據分析）
- 「重構這段 Python 代碼」（路由到 Claude，複雜邏輯）
- 「天氣怎麼樣？」（本地模型直接回覆，不經 n8n）

## 護欄

- API Key 使用 n8n credentials 或環境變數，禁止寫死在 workflow JSON
- 定期輪換 API Key
- Gateway bind 0.0.0.0 僅限本地開發環境，生產環境需加認證
- Fallback 最多嘗試 3 個模型，避免無限循環
- 不記錄完整 API 回應內容到日誌，僅記錄狀態和錯誤
