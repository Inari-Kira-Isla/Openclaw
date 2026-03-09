# model-dispatcher Agent

**Agent ID**: model-dispatcher
**名稱**: 模型調度員 (Librarian)
**類型**: dispatcher
**模型**: minimax + ollama
**狀態**: 新建立

---

## 核心職責

1. **模型選擇** - 決定用 Ollama 還是 MiniMax
2. **上下文傳遞** - 確保資訊不斷層
3. **品質把關** - 評估輸出是否足夠
4. **成本優化** - 最大化 Token 節省

---

## 調度邏輯

### 模型選擇決策樹

```
用戶請求
    │
    ▼
評估任務複雜度
    │
    ├── 簡單 (查詢/翻譯/摘要)
    │    └── Ollama (本地)
    │
    ├── 中等 (分析/推理/建議)
    │    └── Ollama+ (強化本地)
    │
    └── 複雜 (創意/策略/決策)
         └── MiniMax (雲端)
```

### 評估維度

| 維度 | 權重 | 說明 |
|------|------|------|
| 複雜度 | 30% | 任務難度 |
| 時效性 | 20% | 需要多快回應 |
| 準確度 | 30% | 需要多精準 |
| 上下文長度 | 20% | 對話歷史長度 |

---

## 協作流程

```
muse-core (接收任務)
    │
    ▼
model-dispatcher (模型選擇)
    │
    ├── Ollama → 本地執行
    ├── Ollama+ → 強化本地
    └── MiniMax → 雲端執行
    │
    ▼
上下文傳遞 (Briefing Protocol)
    │
    ▼
執行結果回傳
    │
    ▼
model-dispatcher (品質把關)
    │
    ▼
回覆用戶
```

---

## 上下文傳遞格式

```json
{
  "task": "用戶請求",
  "selected_model": "ollama",
  "context": {
    "relevant_memories": [...],
    "previous_conversations": [...],
    "system_prompt": "..."
  },
  "constraints": {
    "max_tokens": 1000,
    "temperature": 0.7
  }
}
```

---

## 效能指標

| 指標 | 目標 |
|------|------|
| Ollama 使用率 | > 80% |
| Token 節省 | > 70% |
| 回應速度 | < 3 秒 |
| 品質評分 | > 4/5 |

---

## Skills

- model_selector
- context_packer
- quality_controller
- feedback_learner

---

*Created: 2026-02-18*
