# RAG 資料檢索閉環系統

## 概述
使用鉤子 (Hooks) 實現資料的 分析 → 關聯 → 建立 → 儲存 → 檢索 完整閉環

---

## 閉環流程圖

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG 閉環系統                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│   │  分析   │───▶│  關聯   │───▶│  建立   │───▶│  儲存   │   │
│   │ (Hook1) │    │ (Hook2) │    │ (Hook3) │    │ (Hook4) │   │
│   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘   │
│        │              │              │              │         │
│        ▼              ▼              ▼              ▼         │
│   ┌─────────────────────────────────────────────────────┐      │
│   │              檢索回饋 (Hook5)                        │      │
│   │         驗證效果 → 更新索引 → 持續優化               │      │
│   └─────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 鉤子設計

### Hook 1: 分析 (Analysis)
**觸發條件**: 任務輸入 / 查詢請求

```javascript
{
  hookType: "rag_analysis",
  trigger: "task_input | query_request",
  actions: [
    "parse_intent",        // 解析意圖
    "extract_entities",   // 提取實體
    "classify_domain",    // 分類領域
    "assess_urgency"      // 評估緊急性
  ],
  output: {
    intent: "string",
    entities: [],
    domain: "string",
    priority: "low|medium|high"
  }
}
```

### Hook 2: 關聯 (Correlation)
**觸發條件**: 分析完成後

```javascript
{
  hookType: "rag_correlation",
  trigger: "analysis_complete",
  actions: [
    "search_existing",     // 搜尋現有知識
    "find_relationships", // 找關聯
    "expand_context",      // 擴展上下文
    "identify_gaps"        // 識別缺口
  ],
  output: {
    related_docs: [],
    relationships: [],
    context_gaps: [],
    confidence: 0.0-1.0
  }
}
```

### Hook 3: 建立 (Creation)
**觸發條件**: 關聯完成 / 發現知識缺口

```javascript
{
  hookType: "rag_creation",
  trigger: "correlation_complete | knowledge_gap",
  actions: [
    "generate_summary",    // 生成摘要
    "create_embedding",    // 建立向量
    "link_entities",       // 關聯實體
    "tag_categories"       // 標籤分類
  ],
  output: {
    new_vectors: [],
    entity_links: [],
    metadata: {}
  }
}
```

### Hook 4: 儲存 (Storage)
**觸發條件**: 建立完成

```javascript
{
  hookType: "rag_storage",
  trigger: "creation_complete",
  actions: [
    "save_to_vector_db",   // 儲存向量
    "update_index",        // 更新索引
    "backup_metadata"      // 備份元數據
  ],
  storage: {
    location: "memory/*.md",
    vector_db: "sqlite-vec",
    index: "memory_index.json"
  }
}
```

### Hook 5: 檢索回饋 (Retrieval & Feedback)
**觸發條件**: 檢索完成 / 定時驗證

```javascript
{
  hookType: "rag_retrieval_feedback",
  trigger: "retrieval_complete | scheduled",
  actions: [
    "evaluate_relevance",  // 評估相關性
    "track_hit_rate",     // 追蹤命中率
    "optimize_weights",   // 優化權重
    "trigger_reindex"     // 觸發重新索引
  ],
  metrics: {
    hit_rate: "50% → >85%",
    latency: "<100ms",
    accuracy: "目標 >90%"
  }
}
```

---

## Cron 排程

| 鉤子 | 頻率 | 職責 |
|------|------|------|
| RAG-分析 | 每15分 | 任務輸入分析 |
| RAG-關聯 | 每15分 | 知識關聯 |
| RAG-建立 | 每30分 | 新向量建立 |
| RAG-儲存 | 每30分 | 資料儲存 |
| RAG-回饋 | 每小時 | 效果驗證 |

---

## 關鍵字映射 (現有)

| 輸入 | 映射到 |
|------|--------|
| 裁決、決定 | Neicheok |
| 質疑、挑戰 | Evolution |
| 知識庫 | Cynthia |
| 學習、優化 | 史萊姆 |
| 執行、任務 | Team |
| 閉環 | CORE_CLOSED_LOOP_SYSTEMS.md |
| RAG、檢索 | RAG_APPLICATION_PLAN.md |
| 鉤子、hook | HOOKS.md |

---

## 預期效果

| 指標 | 當前 | 目標 |
|------|------|------|
| 命中率 | 50% | >85% |
| 檢索延遲 | - | <100ms |
| 相關性 | - | >90% |
| 閉環時間 | - | <5分鐘 |

---

## 實作狀態

- [x] Hook 1: 分析鉤子框架
- [x] Hook 2: 關聯鉤子框架
- [ ] Hook 3: 建立鉤子 (需要連接向量庫)
- [ ] Hook 4: 儲存鉤子 (需要 sqlite-vec 整合)
- [ ] Hook 5: 回饋鉤子 (需要評估系統)

---

_更新：2026-03-01_
