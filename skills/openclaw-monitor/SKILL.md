---
name: openclaw_monitor
description: OpenClaw 系統監控。當需要查看 token 使用量、session 狀態、上下文使用率時觸發，包括：即時狀態查詢、session 監控、context 管理提示。
---

# OpenClaw 系統監控

## 功能說明

監控 OpenClaw 平台的 token 使用量、session 狀態及上下文使用率，提供即時狀態查詢與自動化監控腳本。

## 工作流程

### 第一步：查詢系統狀態
- 執行 `openclaw status` 查看整體狀態
- 執行 `openclaw sessions --limit 5` 查看近期 session

### 第二步：分析關鍵指標

| 指標 | 說明 | 關注閾值 |
|------|------|----------|
| Tokens (ctx %) | 上下文使用百分比 | > 80% 需注意 |
| Age | session 存活時間 | 過長可能需重建 |
| Model | 使用的模型 | 確認是否正確 |
| Flags | 特殊標記 | 有異常標記需檢查 |

### 第三步：異常處理
- ctx% 超過 80%：建議清理或壓縮上下文
- session 長時間無活動：建議關閉釋放資源
- 模型不匹配：檢查配置

## 工具指引

```bash
# 快速查看狀態
openclaw status

# 查看 session 列表
openclaw sessions --limit 5

# 查看特定 session
openclaw sessions --key agent:main:main
```

### 自動化監控腳本

```bash
# session 監控（每 10 秒刷新）
while true; do
    clear
    echo "=== OpenClaw Session Monitor ==="
    echo "時間: $(date)"
    openclaw sessions --limit 5
    sleep 10
done

# token 監控（每 5 秒）
while true; do
    openclaw sessions --limit 3 | grep -E "(Tokens|ctx)"
    sleep 5
done
```

腳本位置：`~/Desktop/openclaw-monitor/`

## Context 管理特性

OpenClaw 自動處理以下事項（無需手動操作）：
- 對話歷史壓縮
- 記憶分層管理
- 向量搜尋整合

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| openclaw 命令不可用 | 檢查 PATH 設定，確認 OpenClaw 已安裝 |
| session 查詢超時 | 檢查 OpenClaw 服務是否正在運行 |
| ctx% 超過 90% | 立即警告，建議重建 session |
| 監控腳本中斷 | 檢查終端連線，重新啟動腳本 |
| 無法連接 Gateway | 確認 port 18789 是否正常監聽 |

## 使用範例

- 「查看目前 OpenClaw 的 token 使用量」
- 「監控 session 狀態」
- 「OpenClaw 上下文快滿了，怎麼處理？」

## 護欄

- 監控為唯讀操作，不修改任何 session 或配置
- 不自動關閉或重建 session，僅提供建議
- 監控腳本不應佔用過多系統資源（間隔至少 5 秒）
- 不記錄 session 中的對話內容，僅追蹤指標
- 異常告警不應造成額外的 token 消耗
