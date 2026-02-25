---
name: security_report
description: 安全報告。當用戶說「安全報告」「安全狀況」「本月安全摘要」時觸發。
metadata: { "openclaw": { "emoji": "📊" } }
---

# 安全報告

彙整金鑰審計、日誌監控、漏洞掃描、異常偵測的結果，產出綜合安全報告。

## 操作 / 工作流程
1. 用 `memory_search` 收集各安全技能的最近結果：
   - api_key_audit 最近報告
   - access_log_monitor 異常紀錄
   - vulnerability_scanner 掃描結果
   - anomaly_detector 異常事件
2. 計算整體安全評分（100 分制）：
   - 金鑰安全 25 分、存取安全 25 分、漏洞狀態 25 分、異常狀態 25 分
3. 與上期報告比較，標示趨勢（改善/持平/惡化）
4. 列出待處理項目，按優先級排序
5. 用 `message` 傳送報告到 Telegram

## 參數
| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| period | string | month | 報告期間：`day` / `week` / `month` / `quarter` |
| detail | string | summary | 詳細程度：`summary` / `full` |

## 輸出格式
```
📊 安全報告 — {period}

整體評分：{score}/100 ({level})
趨勢：{trend} (上期 {prev_score})

| 項目 | 評分 | 狀態 |
|------|------|------|
| 金鑰安全 | {n}/25 | {status} |
| 存取安全 | {n}/25 | {status} |
| 漏洞狀態 | {n}/25 | {status} |
| 異常偵測 | {n}/25 | {status} |

⚠️ 待處理 ({count} 項)：
1. [{priority}] {item}

✅ 本期已修復：{fixed_count} 項
📌 建議下一步：{recommendation}
```

## 錯誤處理
| 錯誤 | 處理 |
|------|------|
| 部分技能無報告 | 該項目標記「無數據」，僅計算有數據的項目 |
| 上期數據缺失 | 跳過趨勢比較，標注「首次報告」 |
| 評分計算異常 | 列出原始數據，讓管理員手動判斷 |

## 使用範例
- "給我這個月的安全報告"
- "目前系統的安全狀況如何"
- "跟上個月比安全有改善嗎"
