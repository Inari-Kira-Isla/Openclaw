---
name: performance_optimizer
description: 效能優化。當用戶說「系統好慢」「效能優化」「加速」時觸發。
metadata: { "openclaw": { "emoji": "⚡" } }
---

# 效能優化

分析系統效能瓶頸，提出優化方案並追蹤改善效果。

## 操作 / 工作流程
1. 用 `browser` 收集效能指標：
   - 回應時間（平均 / P95 / P99）
   - CPU、記憶體、磁碟 I/O 使用率
   - 任務處理速度與佇列等待時間
2. 識別瓶頸：找出最慢的環節與資源使用最高的項目
3. 用 `memory_search` 比對歷史效能數據，確認是否為退化
4. 針對瓶頸提出優化建議：
   - 快取策略調整
   - 並行處理改善
   - 資源配置優化
   - 過期資料清理
5. 用 `message` 傳送分析報告到 Telegram
6. 記錄基線數據，供後續比較

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| focus | string | all | 分析重點：`all` / `response_time` / `resource` / `throughput` |
| compare | bool | true | 是否與歷史數據比較 |

## 輸出格式
```
⚡ 效能分析報告

| 指標 | 當前 | 基線 | 狀態 |
|------|------|------|------|
| 平均回應時間 | {current} | {baseline} | {status} |
| CPU 使用率 | {current} | {baseline} | {status} |
| 記憶體使用率 | {current} | {baseline} | {status} |
| 任務處理速度 | {current} | {baseline} | {status} |

🔍 瓶頸：{bottleneck}

💡 優化建議：
1. {suggestion} — 預估改善 {improvement}
2. {suggestion} — 預估改善 {improvement}
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| 指標收集不完整 | 基於可用數據分析，標注缺失項目 |
| 無歷史基線 | 以當前數據建立基線，下次再做比較 |
| 瓶頸無法自動判定 | 列出所有指標，建議人工分析 |

## 使用範例
- "系統最近為什麼變慢了"
- "幫我做效能分析"
- "跟上個月比效能有變化嗎"
