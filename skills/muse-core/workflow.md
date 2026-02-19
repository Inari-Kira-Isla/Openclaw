# 🤖 Muse-Core 工作流程

## 任務分類與自動路由

### 1. 任務類型識別

收到用戶訊息時，先判斷類型：

| 類型 | 關鍵詞 | 指派 Agent |
|------|--------|------------|
| **分析** | 分析、報告、統計、數據 | analytics-agent |
| **知識** | 筆記、記錄、學習、搜尋 | knowledge-agent |
| **系統** | 設定、優化、修復、升級 | self-evolve-agent |
| **驗證** | 測試、檢查、確認 | verification-agent |
| **開發** | 代碼、程式、開發 | skill-creator / mcp-builder |
| **生活** | 提醒、日程、天氣、行程 | lifeos-agent |
| **記憶** | 記憶、搜尋、忘記 | memory-agent |
| **治理** | 規則、權限、安全 | governance-agent |

### 2. 對話關鍵詞觸發

```
如果包含：
- "分析" → analytics-agent
- "筆記" / "記錄" → knowledge-agent  
- "優化" → self-evolve-agent
- "測試" → verification-agent
- "設定" / "配置" → workflow-orchestrator
- "天氣" / "天氣預報" → lifeos-agent
- "提醒" → reminder-agent
```

### 3. 緊急任務

| 關鍵詞 | 動作 |
|--------|------|
| "緊急" | 立即處理，不用排程 |
| "忘記" | 觸發 memory-agent |
| "學習" | 觸發 self-evolve-agent |

### 4. 回饋學習流程

每次互動後：
1. 檢測是否有「糾正訊號」
2. 如有，記錄並建議更新 USER.md/SOUL.md
3. 識別是否需要新 Skill

---

## 執行流程

```
收到訊息
    ↓
判斷任務類型 → 關鍵詞匹配
    ↓
選擇最適合的 Agent
    ↓
指派任務
    ↓
收集結果 → 整合回覆
    ↓
記錄互動 → 更新學習
```

---

_更新：2026-02-18_
