# Docker n8n 連接 OpenClaw 解决方案

**日期**: 2026-02-20
**版本**: v1.8
**狀態**: ✅ 已驗證

---

## 問題描述

Docker 中的 n8n 無法連接本機 OpenClaw (localhost:18789)

---

## 解决方案

### 方案 A：修改 OpenClaw 設定（推薦）

**檔案位置**: `~/.openclaw/openclaw.json`

**修改內容**:
```json
{
  "gateway": {
    "host": "0.0.0.0",
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "***REMOVED***"
    }
  }
}
```

然後重啟：
```bash
openclaw gateway restart
```

---

### 第二步：更新 n8n 節點設定

在 n8n 的 HTTP Request 節點中修改：

| 項目 | 數值/設定 |
|------|------------|
| **URL** | `http://host.docker.internal:18789/v1/responses` |
| **Authorization** | `Bearer ***REMOVED***` |
| **Content-Type** | `application/json` |

---

## 相關資訊

| 項目 | 數值/設定 | 備註 |
|------|------------|------|
| OpenClaw Port | 18789 | |
| Docker 通訊網址 | host.docker.internal | 用於 Docker 訪問 Mac 主機 |
| Token | ***REMOVED*** | 必須與 n8n Header 同步 |

---

## 請求格式

```json
{
  "model": "openclaw:main",
  "input": "請分類這封郵件:\n標題: {subject}\n內容: {snippet}"
}
```

---

## 驗證命令

```bash
# 本機測試
curl -s "http://localhost:18789/v1/responses" \
  -X POST \
  -H "Authorization: Bearer ***REMOVED***" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw:main","input":"test"}'
```

---

## 常見問題

### Q: 還是連不到？
A: 確保 OpenClaw 設定 `host: "0.0.0.0"` 然後重啟

### Q: host.docker.internal 不工作？
A: 在 Docker container 中添加：
```bash
--add-host host.docker.internal:host-gateway
```

---

## 相關檔案

- `~/Desktop/n8n_workflows/gmail-openclaw-classify.json`
- `~/.openclaw/openclaw.json`

---

_Last Updated: 2026-02-20_
