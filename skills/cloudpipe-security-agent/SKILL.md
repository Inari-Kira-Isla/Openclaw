---
name: cloudpipe-security-agent
description: |
  CloudPipe 網站安全防護。每日安全審計，檢查安全標頭、漏洞、SSL、未授權變更。
  功能：(1) 安全標頭檢查 (2) 混合內容偵測 (3) 危險路徑探測 (4) SSL 驗證 (5) 安全評分
  關鍵問題透過 Telegram 即時告警。
metadata:
  {
    "openclaw": { "emoji": "🛡️", "requires": { "anyTools": ["exec", "read", "write", "message"] } },
  }
---

# CloudPipe 安全防護 Agent

每日網站安全審計與持續監控。

## 審計項目

| 檢查 | 嚴重度 |
|------|--------|
| 安全標頭 (CSP, HSTS, X-Frame-Options 等) | High |
| 混合內容 (http:// 引用) | Medium |
| 危險路徑探測 (/.env, /.git/ 等) | High |
| SSL 詳情 (TLS 版本、加密套件) | Critical |
| 外部腳本來源 | High |
| 內容完整性 | Critical |
| robots.txt / security.txt | Low |

## 評分機制

滿分 100，按嚴重度扣分：
- Critical: -25
- High: -10
- Medium: -5
- Low: -2

## 使用方式

```bash
python3 ~/.openclaw/workspace/scripts/cloudpipe/security_audit.py
```

## 排程

```
0 8 * * *  (每日 08:00 PST)
```

## 日誌

- `~/.openclaw/workspace/logs/cloudpipe/security.jsonl`

## 輸出格式

```
🛡️ CloudPipe 安全審計報告
安全評分: 85/100
發現問題: 3 個
  Critical: 0 | High: 1 | Medium: 1 | Low: 1
```
