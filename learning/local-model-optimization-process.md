# 本地模型優化過程記錄

**日期**: 2026-02-19

---

## 目標

建立本地模型優化閉環，逐步實現完全本地化。

---

## 階段一：混合模式 (現在)

### 架構

```
用戶請求 → model-dispatcher → 本地模型 → 結果
                              ↓
                         MiniMax 驗證 (複雜任務)
                              ↓
                         反饋記錄 → 優化
```

### 模型配置

| 任務 | 本地模型 | 驗證 |
|------|---------|------|
| 簡單對話 | llama3 | 無 |
| 複雜推理 | mistral | MiniMax |
| 程式碼 | codellama | MiniMax |
| 創意寫作 | llama3 | 無 |

---

## 數據收集

### 追蹤指標

| 指標 | 目標 |
|------|------|
| 相似度分數 | > 80% |
| 驗證通過率 | > 90% |
| 本地模型使用率 | 80% |

### 反饋記錄

- 位置: `~/Desktop/local-model-feedback.json`
- 內容: 任務類型、模型、相似度、優化記錄

---

## 每週優化流程

### 1. 數據收集

```bash
python scripts/local_model_optimizer.py --report
```

### 2. 分析報告

- 檢查平均相似度
- 識別弱點任務類型
- 調整模型選擇

### 3. 優化觸發

```
平均相似度 < 70% → 觸發優化
連續3次失敗 → 切換模型
新任務類型 → 添加規則
```

---

## 里程碑

| 階段 | 時間 | 本地化程度 |
|------|------|-----------|
| Phase 1 | 現在 | 50% |
| Phase 2 | 1 個月 | 80% |
| Phase 3 | 3 個月 | 95% |
| Phase 4 | 6 個月 | 99% |

---

## 自我優化觸發條件

1. **相似度過低**: 平均 < 0.7
2. **連續失敗**: 同一任務類型 3 次
3. **新任務**: 未定義的任務類型
4. **定時**: 每週檢視

---

## 技術細節

### 模型選擇邏輯

```python
def select_model(task_type):
    if task_type == "程式碼":
        return "codellama"  # 強化
    elif task_type == "推理":
        return "mistral"
    else:
        return "llama3"
```

### 驗證流程

```python
def verify(local_output, minimax_output):
    similarity = calculate_similarity(local_output, minimax_output)
    
    if similarity < 0.8:
        record_feedback()
        return minimax_output
    
    return local_output
```

---

## 下一步

- [ ] 設定 model-dispatcher 規則
- [ ] 啟動混合模式
- [ ] 收集第一週數據
- [ ] 分析並優化

---
