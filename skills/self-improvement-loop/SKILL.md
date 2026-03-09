---
name: self-improvement-loop
description: |
  自我學習優化閉環。當需要系統自動學習、持續改進時觸發。
  功能：(1) 記錄決策與結果 (2) 分析模式找出問題 (3) 自動優化規則 (4) 持續進化。
  適用場景：(1) 每日自動優化 (2) 決策質量追蹤 (3) 系統自我改進
metadata:
  {
    "openclaw": { "emoji": "🧬", "requires": { "anyTools": ["exec", "read", "write", "message"] } },
  }
---

# Self-Improvement Loop

自我學習優化閉環系統 - 讓系統自己變得更聰明！

## 閉環流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    🧬 自我學習閉環                                │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  📥 Phase 1: 數據收集                                           │
│  • 記錄每次決策                                                 │
│  • 記錄執行結果                                                 │
│  • 記錄用戶反饋                                                 │
│  • 記錄效能指標                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  🔬 Phase 2: 分析模式                                           │
│  • 找出成功模式                                                 │
│  • 找出失敗模式                                                 │
│  • 找出優化空間                                                 │
│  • 預測趨勢                                                    │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  🧪 Phase 3: 生成假設                                           │
│  • 如果改變 X，結果會更好                                       │
│  • 測試新策略                                                  │
│  • 評估影響                                                    │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ⚡ Phase 4: 優化執行                                           │
│  • 更新決策規則                                                 │
│  • 調整信心度                                                  │
│  • 改進 Prompt                                                 │
│  • 最佳化流程                                                  │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  📈 Phase 5: 驗證結果                                           │
│  • 追蹤新決策效果                                              │
│  • 比較改進前後                                                │
│  • 持續監控                                                    │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
                       🔄 回到 Phase 1
```

## 每日自動優化腳本

```bash
#!/bin/bash
# self_improve.sh - 每日自動優化

echo "🧬 開始自我學習優化..."

# 1. 收集數據
python3 ~/.openclaw/workspace/scripts/decision_tracker.py stats

# 2. 分析
python3 ~/.openclaw/workspace/scripts/decision_tracker.py optimize

# 3. 檢查效能
python3 ~/.openclaw/workspace/scripts/performance_analyzer.py

# 4. 優化規則
python3 ~/.openclaw/workspace/scripts/rule_optimizer.py

# 5. 報告
echo "✅ 每日優化完成"
```

## 分析維度

### 1. 決策質量

```
指標:
- 準確率 (accuracy)
- 信心度匹配度 (calibration)
- 決策時間
- 複雜度 vs 效果

分析:
- 哪些類型決策最準確？
- 信心度是否過高/過低？
- 哪些情境需要更多思考？
```

### 2. 執行效率

```
指標:
- 任務完成時間
- 重試次數
- 資源使用

分析:
- 哪些步驟可以優化？
- 哪些任務卡住太久？
- 哪些工具有問題？
```

### 3. 用戶滿意度

```
指標:
- 用戶回覆
- 後續問題
- 持續互動

分析:
- 哪些回覆被接受？
- 哪些需要改進？
- 用戶偏好什麼風格？
```

## 自動優化規則

### 信心度校準

```python
# 根據歷史數據調整信心度
if high_confidence_accuracy < 0.7:
    reduce_confidence("high", 0.1)
elif high_confidence_accuracy > 0.95:
    increase_confidence("high", 0.05)

# 根據信心度範圍調整
confidence_mapping = {
    "very_high": {"range": (0.9, 1.0), "target_accuracy": 0.85},
    "high": {"range": (0.7, 0.9), "target_accuracy": 0.75},
    "medium": {"range": (0.4, 0.7), "target_accuracy": 0.65},
    "low": {"range": (0.0, 0.4), "target_accuracy": 0.5}
}
```

### 決策策略優化

```python
# 根據效果調整策略
strategies = {
    "simple_task": {
        "prefer": "autonomous",
        "threshold": 0.8
    },
    "complex_task": {
        "prefer": "claude",
        "threshold": 0.6
    },
    "uncertain": {
        "prefer": "claude",
        "threshold": 0.4
    }
}
```

### Prompt 優化

```python
# 分析哪些 Prompt 效果更好
def optimize_prompt(prompt, results):
    successful_prompts = [p for p in results if p.success]
    failed_prompts = [p for p in results if not p.success]
    
    # 提取成功模式
    success_patterns = extract_patterns(successful_prompts)
    
    # 更新 Prompt
    return apply_patterns(prompt, success_patterns)
```

## 學習週期

### 每小時
- 檢查錯誤
- 記錄異常
- 快速修復

### 每天
- 統計分析
- 信心度校準
- 規則更新

### 每週
- 深度分析
- 趨勢預測
- 策略調整

### 每月
- 大規模回顧
- 架構優化
- 長期規劃

## 整合系統

### 與決策系統整合

```python
# 決策時自動學習
def decide_with_learning(context):
    # 1. 獲取優化後的規則
    rules = get_optimized_rules()
    
    # 2. 使用規則決策
    decision = apply_rules(context, rules)
    
    # 3. 記錄決策
    record_decision(decision)
    
    # 4. 執行並記錄結果
    result = execute(decision)
    record_result(decision.id, result)
    
    # 5. 觸發學習（如果需要）
    if result.needs_review:
        trigger_learning(decision.id)
    
    return decision
```

### 與記憶系統整合

```python
# 定期寫入學習筆記
def write_learning_notes():
    notes = generate_learning_notes()
    
    memory = {
        "date": today,
        "learnings": notes,
        "optimizations": get_recent_optimizations(),
        "metrics": get_current_metrics()
    }
    
    write_to_memory("weekly_learning", memory)
```

## 成效追蹤

### 關鍵指標

| 指標 | 目標 | 當前 |
|------|------|------|
| 決策準確率 | > 85% | ?% |
| 信心度匹配度 | > 80% | ?% |
| 平均決策時間 | < 5s | ?s |
| 自動化成功率 | > 90% | ?% |

### 趨勢圖

```
決策準確率趨勢
100% |    *****
 90% |  *****
 80% |****
 70% |*
     +-----------
     Day 1   Day 7  Day 30
```

## 啟動自動學習

```bash
# 加入每日 cron
0 0 * * * ~/.openclaw/workspace/scripts/self_improve.sh

# 或手動觸發
python3 ~/.openclaw/workspace/scripts/self_improve.py run
```

## 持續進化

系統會自己：
1. **學會更好地決策** - 根據歷史調整
2. **優化信心度** - 讓預測更準
3. **改進回覆質量** - 根據反饋調整
4. **發現新模式** - 找出人類沒注意到的規律
5. **適應用戶** - 學習你的偏好

讓系統變得越來越聰明！🧬
