# OpenClaw 自動化修復系統

**版本**: v1.0
**日期**: 2026-02-18

---

## 🎯 目標

建立類似 Claude Code 的自動化錯誤修復流程：
- 錯誤偵測 → Slack 通知 → AI 修復 → PR → 回報

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────────────────────────────────┐
│              OpenClaw 自動化修復系統                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  監控腳本   │───▶│   n8n      │───▶│   Slack    │      │
│  │ (專案中)    │    │  Webhook   │    │  #alerts   │      │
│  └─────────────┘    └─────────────┘    └──────┬──────┘      │
│                                                 │               │
│                                                 ▼               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    model-dispatcher                     │   │
│  │              (決定用 Ollama 或 MiniMax)                  │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            │                                   │
│                            ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   skill-creator                         │   │
│  │               (Code Review + Fix)                      │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            │                                   │
│                            ▼                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  GitHub    │◀───│   修復     │───▶│   PR       │      │
│  │  Repo      │    │   程式碼    │    │   發送     │      │
│  └─────────────┘    └─────────────┘    └──────┬──────┘      │
│                                                 │               │
│                                                 ▼               │
│                                          ┌─────────────┐      │
│                                          │   Slack     │      │
│                                          │   回報      │      │
│                                          └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 組成部分

### 1. 監控腳本

**位置**: `~/openclaw/workspace/scripts/error-monitor.py`

```python
# 功能
- 監控 error log
- 偵測 Error / Critical
- 發送到 n8n Webhook
```

### 2. n8n Workflow

**位置**: `~/Desktop/N8n/auto-fix-workflow.json`

```
Slack Webhook 接收
    ↓
解析錯誤內容
    ↓
觸發 model-dispatcher
    ↓
選擇模型進行修復
    ↓
發送 PR
    ↓
回報 Slack
```

### 3. Slack 設定

| 項目 | 說明 |
|------|------|
| Webhook URL | Slack 接收錯誤 |
| Channel | #openclaw-alerts |
| Bot | @OpenClaw |

---

## 🔧 實作步驟

### Step 1: 建立 Slack App

1. 前往 https://api.slack.com/apps
2. 建立新 App
3. 設定 Incoming Webhooks
4. 取得 Webhook URL

### Step 2: 部署監控腳本

```bash
# 部署到伺服器
cp error-monitor.py /path/to/your/project/

# 設定 crontab 執行
*/5 * * * * python /path/to/error-monitor.py
```

### Step 3: 設定 n8n Workflow

1. Import `auto-fix-workflow.json`
2. 設定 Slack Credentials
3. 設定 GitHub Credentials

### Step 4: 測試流程

```bash
# 模擬錯誤
python test_error.py
```

---

## 📋 Workflow 節點

| 節點 | 功能 |
|------|------|
| Slack Trigger | 接收錯誤訊息 |
| Error Parser | 解析錯誤內容 |
| Model Dispatcher | 選擇修復模型 |
| Code Analyzer | 分析錯誤程式碼 |
| Code Fixer | 產生修復方案 |
| GitHub | 發送 PR |
| Slack Notify | 回報結果 |

---

## 🎯 使用方式

### 方式 1: 自動觸發

```
專案 Error Log → n8n → AI 修復 → PR
```

### 方式 2: 手動觸發

```
Slack: @OpenClaw 幫我修這個 bug
    ↓
AI 調查 → 修復 → PR
    ↓
回報結果
```

---

## 📊 預期效益

| 指標 | 效果 |
|------|------|
| 修復時間 | 縮短 80% |
| 值班壓力 | 減少 50% |
| 24/7 監控 | ✅ |

---

## ⚠️ 注意事項

1. **安全性**: 確認 GitHub 權限設定正確
2. **測試**: 先在測試環境驗證
3. **人類審核**: PR 需要人類審核才能合併

---

*記錄時間: 2026-02-18*
