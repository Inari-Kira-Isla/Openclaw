# 模型調度工作流 - 本地優化版

**日期**: 2026-02-19

---

## 工作流概述

```
用戶請求
    │
    ▼
┌─────────────────────┐
│  model-dispatcher  │
│    (模型選擇)       │
└─────────────────────┘
    │
    ├── 簡單任務 → 本地模型
    │
    ├── 複雜任務 → 本地模型 → MiniMax 驗證
    │
    └── 預設 → 本地模型
    │
    ▼
┌─────────────────────┐
│   本地模型執行      │
│  (Ollama)          │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│   結果處理          │
│   (根據任務類型)    │
└─────────────────────┘
    │
    ├── 需要驗證
    │    │
    │    ▼
    │   MiniMax 驗證
    │    │
    │    ▼
    │   相似度計算
    │    │
    │    ▼
    │   記錄反饋
    │    │
    │    ▼
    │   相似度 > 80% → 返回本地結果
    │   相似度 < 80% → 返回 MiniMax 結果
    │
    └── 不需驗證 → 直接返回
    │
    ▼
┌─────────────────────┐
│   自我優化檢查      │
│   (每週)           │
└─────────────────────┘
```

---

## 詳細流程

### 1. 任務分類

| 任務類型 | 模型 | 驗證 |
|----------|------|------|
| 簡單對話 | llama3 | 無 |
| 程式碼 | codellama | MiniMax |
| 複雜推理 | mistral | MiniMax |
| 創意寫作 | llama3 | 無 |
| 預設 | llama3 | 無 |

### 2. 本地模型執行

```python
def execute_local(prompt, model):
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True, text=True, timeout=120
    )
    return result.stdout if result.returncode == 0 else None
```

### 3. MiniMax 驗證

```python
def verify_with_minimax(prompt, local_output):
    minimax_output = call_minimax(prompt)
    similarity = calculate_similarity(local_output, minimax_output)
    
    record_feedback(task_type, model, local_output, minimax_output, similarity)
    
    return {
        "output": local_output if similarity > 0.8 else minimax_output,
        "source": "local" if similarity > 0.8 else "minimax",
        "similarity": similarity
    }
```

### 4. 反饋記錄

```json
{
  "timestamp": "2026-02-19T07:00:00",
  "task_type": "程式碼",
  "model": "codellama",
  "local_output": "...",
  "minimax_output": "...",
  "similarity": 0.85,
  "decision": "use_local"
}
```

### 5. 每週優化

```python
def weekly_optimization():
    # 讀取反饋數據
    feedbacks = load_feedbacks()
    
    # 計算各模型平均相似度
    model_scores = calculate_model_scores(feedbacks)
    
    # 檢查是否觸發優化
    for model, score in model_scores.items():
        if score < 0.7:
            trigger_optimization(model)
        elif score > 0.9:
            reduce_verification(model)
```

---

## 觸發條件

### 自動優化

| 條件 | 動作 |
|------|------|
| 平均相似度 < 70% | 觸發模型參數調整 |
| 連續 3 次失敗 | 切換到更強模型 |
| 新任務類型 | 添加新規則 |
| 驗證通過率 > 90% | 降低驗證頻率 |

### 定時檢查

- **每日**: 記錄使用統計
- **每週**: 分析反饋，生成報告
- **每月**: 評估優化效果

---

## 數據追蹤

### 使用統計

| 指標 | 追蹤 |
|------|------|
| 本地模型使用次數 | 每日 |
| 驗證通過率 | 每週 |
| 平均相似度 | 每週 |
| 節省的 Token | 每日 |
| 模型切換次數 | 每週 |

### 報告格式

```json
{
  "week": "2026-W08",
  "local_usage": {
    "llama3": 150,
    "mistral": 45,
    "codellama": 30
  },
  "verification": {
    "total": 75,
    "passed": 68,
    "rate": "90.7%"
  },
  "similarity": {
    "llama3": 0.82,
    "mistral": 0.78,
    "codellama": 0.85
  },
  "tokens_saved": 2500000,
  "recommendations": [
    "mistral 相似度偏低，建議增加驗證"
  ]
}
```

---

## Agent 整合

### model-dispatcher 行為

```
每次收到請求:
1. 分析任務類型
2. 選擇最適模型
3. 執行任務
4. 根據需要驗證
5. 記錄反饋
6. 定期優化
```

### 與 muse-core 互動

```
muse-core → 分發任務 → model-dispatcher
                            │
                            ▼
                      選擇模型
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
        llama3          mistral         codellama
            │               │               │
            ▼               ▼               ▼
        執行結果 ← 驗證(MiniMax) → 執行結果
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                      返回結果 + 反饋
```

---

## 里程碑

- [x] Phase 1: 配置建立 (2026-02-19)
- [ ] Phase 2: 工作流實現
- [ ] Phase 3: 數據收集 (1 週)
- [ ] Phase 4: 第一次優化
- [ ] Phase 5: 降低驗證頻率

---

## 檔案位置

- 配置: `config/model-dispatcher.yaml`
- 腳本: `scripts/local_model_optimizer.py`
- Skill: `skills/local-model-optimization/`
- 記錄: `learning/local-model-optimization-process.md`
- 工作流: `workflows/model-dispatcher-workflow.md`

---
