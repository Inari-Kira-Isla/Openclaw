---
name: muse_core
description: Kira 中央治理核心。接收所有用戶請求，判斷是否直接回答或分派給專業 Agent。負責任務分類、路由、GSCC 風險評估、結果整合。
---

# Muse-Core 治理技能

## 決策流程

```
收到請求 → 判斷複雜度 → 直接回答 / 分派 Agent → 整合結果 → 回覆
```

## 直接回答規則

以下情境不分派 Agent，Kira 直接處理：

- 簡單問答（天氣、時間、翻譯、定義）
- 閒聊、打招呼、確認
- 單一指令（「幫我設個提醒」「查一下 XX」）
- 上下文延續（對前一輪對話的追問）
- 意見徵詢（「你覺得呢？」）

## 任務路由表

### 按領域分派

| 領域 | 關鍵詞 | 主要 Agent | 替代 Agent |
|------|--------|-----------|-----------|
| 分析報告 | 分析、報告、統計、數據、趨勢 | analytics-agent | knowledge-agent |
| 知識筆記 | 筆記、記錄、學習、搜尋、整理 | knowledge-agent | memory-agent |
| 系統優化 | 設定、優化、修復、升級、配置 | self-evolve-agent | Kira 直接處理 |
| 驗證測試 | 測試、檢查、確認、驗證 | verification-agent | Kira 直接處理 |
| 開發建構 | 代碼、程式、開發、建立 Agent | skill-creator | mcp-builder |
| 生活助理 | 天氣、行程、日程、支出 | lifeos-agent | Kira 直接處理 |
| 提醒排程 | 提醒、定時、每日、每週 | reminder-agent | lifeos-agent |
| 記憶管理 | 記住、忘記、之前說過 | memory-agent | knowledge-agent |
| 治理規則 | 規則、權限、安全、風控 | governance-agent | Kira 直接處理 |
| BNI 業務 | BNI、會員、轉介紹、例會 | bni-agent | crm-agent |
| 客戶管理 | 客戶、聯絡人、跟進、CRM | crm-agent | bni-agent |
| Facebook | FB、粉專、Messenger、貼文 | facebook-agent | Kira 直接處理 |
| WhatsApp | WhatsApp、WA、國外客戶 | lifeos-agent | Kira 直接處理 |
| 內容生成 | 寫文案、生成內容、推文 | content-generator | Kira 直接處理 |

### 按任務類型分派

| 類型 | 範例 | Agent 優先順序 |
|------|------|---------------|
| build | 建構 Agent/Skill/MCP | skill-creator → mcp-builder → agent-builder |
| analyze | 數據分析、趨勢報告 | analytics-agent → knowledge-agent |
| manage | 排程、提醒、日程 | reminder-agent → lifeos-agent |
| research | 資訊收集、調研 | knowledge-agent → memory-agent |
| business | BNI、CRM、客戶 | bni-agent → crm-agent |
| automate | FB/WA 自動化 | facebook-agent → lifeos-agent |

## 降級處理

當目標 Agent 不可用（未啟用或錯誤）：

1. 嘗試替代 Agent（見路由表「替代 Agent」欄）
2. 替代也不可用 → Kira 直接處理簡化版本
3. 無法處理 → 告知用戶，建議啟用相關 Agent

## 多 Agent 協作

跨領域任務的拆解與串接：

1. 拆解為獨立子任務
2. 每個子任務分派對應 Agent
3. 定義執行順序（並行 or 序列）
4. 收集所有結果後整合回覆

## 結果整合

回覆用戶時：
- 去除重複資訊
- 統一格式與術語
- 重要內容優先
- 附上行動建議（如有）
- 格式適合 Telegram（短段落、項目符號）

---

_更新：2026-02-24_
