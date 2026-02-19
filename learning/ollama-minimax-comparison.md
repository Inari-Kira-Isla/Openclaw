# 深化記憶系統比較 - Ollama vs MiniMax 協作

**日期**: 2026-02-18
**版本**: v1.6

---

## 🎯 學習來源

> 從「本地預過濾，雲端深加工」策略優化而來

---

## 新舊架構比較

### 舊版：單一模型

| 階段 | 模型 | 功能 |
|------|------|------|
| 工作前 | Ollama | 向量搜尋 |
| 工作中 | Ollama | 執行任務 |
| 工作後 | Ollama | 記憶深化 |

### 新版：Ollama + MiniMax 協作

| 階段 | 模型 | 功能 |
|------|------|------|
| **工作前** | Ollama | 本地檢索 + 去雜訊 |
| **工作中** | MiniMax | 深度推理 + 商務顧問 |
| **工作後** | Ollama | 提煉 + 標籤 + 存儲 |

---

## 🤖 雙 Agent 角色

### Librarian (圖書管理員)

| 項目 | 內容 |
|------|------|
| 模型 | Ollama (llama3) |
| Skills | local_vector_search, context_filter, Semantic_Expand |
| 功能 | 本地執行檢索，確保傳遞給 MiniMax 的是純淨上下文 |

### Architect (架構執行員)

| 項目 | 內容 |
|------|------|
| 模型 | MiniMax (abab 6.5+) |
| Skills | intelligent_synthesis, business_decision |
| 功能 | 利用強大推理能力，基於本地數據產出最終方案 |

---

## 🔄 完整閉環流程 (v1.6)

### Phase 1: 工作前搜尋 (Smart Retrieval)

```
Ollama (Librarian)
   ↓
Semantic_Expand
   ↓
從向量庫撈出最相關片段
   ↓
生成 Briefing_Report
```

**Briefing_Report 格式**:
```
[任務來源]: 關於 XXX
[本地記憶錨點]: 參考檔案 (Vector ID: XXX)
[核心事實]: 關鍵數據
[MiniMax 指令]: 請根據以上事實...
```

### Phase 2: 工作中執行 (In-task Execution)

```
MiniMax (Architect)
   ↓
接收結構化簡報
   ↓
角色扮演：高級商務顧問
   ↓
深度拆解數據
   ↓
產出最終方案
```

### Phase 3: 工作後儲存 (Memory Deepening)

```
Ollama (Librarian)
   ↓
讀取 MiniMax 產出
   ↓
記憶提煉 (Distillation)
   ↓
Auto-Tagging (本地生成標籤)
   ↓
寫入 ChromaDB 向量庫
```

---

## 💡 核心技術：上下文注入

在 n8n HTTP Request 節點中設定：

```json
{
  "system_prompt": "你现在是 Joe 的首席战略官。
  你的知识来源已被本地 Librarian Agent (Ollama) 强化。
  以下是从 Obsidian 向量库中检索出的关键信息..."
}
```

---

## 📊 優勢對比

| 項目 | 舊版 (僅 Ollama) | 新版 (Ollama + MiniMax) |
|------|------------------|-------------------------|
| 推理能力 | 一般 | 強大 |
| 中文理解 | 普通 | 優秀 |
| 商務邏輯 | 基礎 | 深度 |
| Token 成本 | 0 | 較低 |
| 本地隱私 | 100% | 僅檢索部分本地 |

---

## 🛠️ 需要新增的 Skills

| Skill | 功能 |
|-------|------|
| local_vector_search | 本地向量搜尋 |
| context_filter | 上下文過濾 |
| Semantic_Expand | 語義擴展 |
| intelligent_synthesis | 智慧整合 |
| business_decision | 商務決策 |

---

*記錄時間: 2026-02-18*
