---
name: cloudpipe-uptime-monitor
description: |
  CloudPipe 網站 24/7 監控。每 15 分鐘檢查網站可用性、回應時間、內容完整性。
  功能：(1) HTTP 狀態碼檢查 (2) 回應時間監控 (3) SSL 憑證到期 (4) JSON-LD 驗證 (5) 內容雜湊比對
  異常時透過 Telegram 即時告警。
metadata:
  {
    "openclaw": { "emoji": "🟢", "requires": { "anyTools": ["exec", "message"] } },
  }
---

# CloudPipe 網站監控

24/7 全天候網站可用性與內容完整性監控。

## 監控項目

| 檢查 | 方法 | 告警門檻 |
|------|------|----------|
| HTTP 狀態 | GET 主頁 | 非 200 |
| 回應時間 | 測量耗時 | > 3 秒 |
| SSL 憑證 | ssl 模組 | < 14 天到期 |
| HTML 標題 | 解析 title | 缺失或空 |
| JSON-LD | json.loads | 解析失敗 |
| 外部資源 | HEAD 請求 | 非 200 |
| 內容雜湊 | SHA-256 | 非預期變更 |

## 使用方式

```bash
python3 ~/.openclaw/workspace/scripts/cloudpipe/uptime_monitor.py
```

## 排程

```
*/15 * * * *  (每 15 分鐘)
```

## 日誌

- `~/.openclaw/workspace/logs/cloudpipe/uptime.jsonl`
- 自動輪替，保留最近 9000 筆

## 告警格式

正常：`✅ CloudPipe OK | 234ms | SSL: 89d`
異常：`ALERT:🔴 CloudPipe 網站告警\n• HTTP 503 — 網站可能下線!`

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| 連線逾時 | 記錄錯誤，發送告警 |
| SSL 檢查失敗 | 記錄錯誤，繼續其他檢查 |
| 首次執行 | 建立內容雜湊基準 |
