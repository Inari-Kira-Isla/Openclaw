---
name: performance_analysis
description: 效能分析。定期或按需分析系統整體效能，產出報告與優化建議。
metadata: { "openclaw": { "emoji": "📈" } }
---

# 效能分析

收集與分析系統效能指標，產出健康報告與改進建議。

## 操作 / 工作流程

1. **指標收集** — 從 `memory_search` 取得各項效能數據：
   - 系統指標：CPU、記憶體、磁碟 I/O
   - 應用指標：回應延遲、錯誤率、吞吐量
   - 業務指標：任務完成率、技能觸發次數
2. **趨勢分析** — LLM 分析指標走勢：
   - 日 / 週 / 月趨勢
   - 同期對比（環比、同比）
   - 異常點偵測
3. **歸因分析** — 找出效能變化的原因：
   - 哪個 agent 或 skill 影響最大
   - 是否與外部因素相關（API 延遲、流量突增）
4. **產出報告** — 結構化報告 + 優化建議
5. **記錄基準** — 將分析結果存入 `memory_search` 作為下次基準

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| scope | string | "system" | 分析範圍：system / agent:{name} / skill:{name} |
| period | string | "7d" | 分析時間範圍：24h / 7d / 30d |
| detail | string | "summary" | 報告詳細度：summary / detailed |

## 輸出格式

```
📈 效能分析報告
- 範圍：{scope}
- 期間：{period}
- 整體健康度：{health_score}/100

關鍵指標：
- 系統正常運行時間：{uptime}%
- 平均回應時間：{avg_response_time}
- 錯誤率：{error_rate}%
- 任務完成率：{task_completion_rate}%

趨勢：{trend_summary}

優化建議：
1. [優先] {suggestion_1}
2. [中期] {suggestion_2}
3. [長期] {suggestion_3}
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 指標數據不足 | 回報可用數據的分析，標記缺失項目 |
| 分析期間無數據 | 縮短期間或擴大範圍重試 |
| 健康度突然下降 | 自動觸發 drift_detection 進行深入分析 |
| 報告過長 | 依 detail 參數截斷，detailed 模式才顯示全部 |

## 使用範例

- "系統最近的效能怎麼樣"
- "分析一下過去一週的效能"
- "memory-agent 的回應時間正常嗎"
