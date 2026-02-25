---
name: drift_detection
description: 漂移偵測。當系統行為偏離預期時觸發，監控效能、行為與數據漂移。
metadata: { "openclaw": { "emoji": "📡" } }
---

# 漂移偵測

持續監控系統指標，偵測效能、行為或數據偏離預期的漂移現象。

## 操作 / 工作流程

1. **基準建立** — 從 `memory_search` 取得歷史指標作為基準線：
   - 錯誤率基準
   - 回應時間基準
   - 觸發模式基準
2. **定期採樣** — 透過 `cron` 每小時採集當前指標
3. **漂移計算** — LLM 比對當前值與基準線：
   - 效能漂移：回應時間增加、錯誤率上升
   - 行為漂移：輸出模式改變、觸發頻率異常
   - 數據漂移：輸入特徵分布改變
4. **嚴重度分級** — 依偏離幅度分類：
   - `INFO`：輕微偏離（< 20%），僅記錄
   - `WARN`：需要關注（20-50%），記錄 + 觀察
   - `ERROR`：影響功能（50-100%），用 `message` 通知
   - `CRITICAL`：系統異常（> 100%），立即用 `message` 告警
5. **根因定位** — 分析可能原因並記錄到 `memory_search`

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| target | string | "all" | 監控目標：all / agent:{name} / skill:{name} |
| period | string | "24h" | 分析時間窗口 |
| sensitivity | string | "normal" | 敏感度：low / normal / high |

## 輸出格式

```
📡 漂移偵測報告
- 監控範圍：{target}
- 時間窗口：{period}
- 偵測到 {count} 個漂移

{foreach drift}
  [{severity}] {metric}：基準 {baseline} → 當前 {current}（偏離 {deviation}%）
  可能原因：{possible_cause}
{/foreach}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 無歷史基準 | 以當前值作為初始基準，記錄並跳過比對 |
| 指標採集失敗 | 記錄缺失，下次採集時補算 |
| 誤報過多 | 自動降低敏感度，建議調整閾值 |
| CRITICAL 告警 | 立即用 `message` 通知用戶，附帶根因分析 |

## 使用範例

- "最近系統有漂移嗎"
- "檢查 memory-agent 的效能是否正常"
- "為什麼回應變慢了"
