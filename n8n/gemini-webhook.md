# OpenClaw + n8n + Gemini Webhook 整合

**日期**: 2026-02-19

---

## 概述

使用 OpenClaw Webhook 連接 n8n，傳送 Gemini 工作。

---

## 工作流程

```
OpenClaw
    │
    ▼ Webhook
n8n (gemini-webhook)
    │
    ▼ 呼叫
Gemini API
    │
    ▼ 回應
OpenClaw
```

---

## n8n Workflow

### 節點

1. **Webhook** - 接收 OpenClaw 請求
2. **Gemini API** - 呼叫 Gemini
3. **Respond** - 返回結果

### Webhook URL

```
https://your-n8n.com/webhook/gemini-job
```

---

## OpenClaw 設定

### 方法 1：使用 message 工具

在 OpenClaw 中：

```
/sendwebhook https://your-n8n.com/webhook/gemini-job {"prompt": "你的問題"}
```

### 方法 2：使用 cron 觸發

設定定時任務呼叫 webhook

---

## 使用方式

### 1. 啟動 n8n

```bash
cd ~/Desktop/n8n_workflows
n8n
```

### 2. 匯入 Workflow

- 打開 n8n (http://localhost:5678)
- 匯入 `gemini-webhook.json`
- 啟用 Webhook

### 3. 取得 Webhook URL

```
http://localhost:5678/webhook/gemini-job
```

### 4. 測試

```bash
curl -X POST http://localhost:5678/webhook/gemini-job \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好，請介紹自己"}'
```

---

## Gemini API Key

需要在環境變數中設定：

```bash
export GEMINI_API_KEY="your-api-key"
```

或在 n8n credentials 中設定。

---

## 進階功能

### 多模型支援

| 模型 | Endpoint |
|------|----------|
| Gemini Pro | gemini-pro |
| Gemini Pro Vision | gemini-pro-vision |
| Gemini Ultra | gemini-ultra |

### 參數調整

```json
{
  "temperature": 0.9,
  "maxOutputTokens": 2048,
  "topP": 0.95,
  "topK": 40
}
```

---

## 檔案位置

- n8n workflow: `~/Desktop/n8n_workflows/gemini-webhook.json`

---
