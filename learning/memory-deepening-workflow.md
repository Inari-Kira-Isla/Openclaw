# 深化學習應用 - 閉環式記憶系統

**來源**: AI 知識工程師建議
**日期**: 2026-02-18
**版本**: v1.4

---

## 🎯 核心理念

> 打破「單向儲存」僵局，建立閉環式記憶系統

---

## 🔄 深化記憶全流程

### 1. 工作前：智慧檢索 (Pre-task Retrieval)

| 項目 | 說明 |
|------|------|
| Skill | Hybrid_Search_Skill |
| 動作 | 同時執行 Vector Search + Keyword Search |
| 目的 | 意圖對齊檢索 |

### 2. 工作中：動態標註 (In-task Enrichment)

| 項目 | 說明 |
|------|------|
| Skill | Active_Thought_Logger |
| 動作 | 暫存「發現的規律」或「解決的難點」 |
| 範例 | 週三價格波動受物流影響 |

### 3. 工作後：記憶深化 (Post-task Deepening)

| 步驟 | 功能 |
|------|------|
| 歸納 (Summarize) | 提煉成一條「經驗規則」 |
| 連結 (Linking) | 尋找相似記憶 |
| 衝突檢測 | 標記「記憶更新」或「資料矛盾」 |
| 權重調整 | 增加 importance_score |

---

## 🛠️ Agent Skill 核心邏輯

| 步驟 | 功能描述 | 實現邏輯 |
|------|----------|----------|
| Step A: Reflection | 自我反思 | LLM 總結：學到什麼新邏輯？ |
| Step B: Tagging | 自動打標籤 | 提取關鍵字 |
| Step C: Cross-Reference | 跨節點關聯 | 建立連結 |
| Step D: Store | 寫入 ChromaDB | 存入向量庫 |

---

## 🏗️ 雙 Agent 協作架構

| Agent | 角色 |
|-------|------|
| Worker (執行 Agent) | 負責業務執行 |
| Librarian (記憶 Agent) | 由 Athena 擔任 |

### Librarian 職責

- **工作前**: 為 Worker 準備相關筆記
- **工作後**: 觀察產出，寫「學習心得」存回向量庫

---

## 💡 深化核心公式

```
深化向量 = 語義標籤 + 提煉摘要 + 原始路徑 + importance_score
```

---

## 📝 下一步

需要在 n8n 中串接「工作後自動深化」的節點嗎？

---

*記錄時間: 2026-02-18*
