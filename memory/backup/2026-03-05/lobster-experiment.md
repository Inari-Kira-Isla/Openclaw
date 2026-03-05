# 🦞 龍蝦自進化神經元實驗框架

## 1️⃣ 小範圍測試 (Toy Environment)

### 測試場景
- 簡化網格世界 (5x5 grid)
- 3 種action: 前/後/轉向
- 隨機生成障礙物和食物

### 基準對比
| 版本 | 描述 |
|------|------|
| Baseline | 固定策略，無學習 |
| v1 | 加入神經元，無訓練 |
| v2 | 關聯學習後 |
| v3 | 多代演化後 |

---

## 2️⃣ 效能指標追蹤

### 主要指標
```
- 生存率 (survival_rate): 存活回合數 / 總回合
- 成功率 (success_rate): 達成目標次數 / 總嘗試
- 平均回報 (avg_reward): 每回合累積獎勵
- 學習曲線 (learning_curve): 回報隨訓練世代的變化
```

### 次要指標
```
- 決策多樣性 (action_entropy): 避免策略僵化
- 記住坑數 (trap_count): 成功避開過去失敗的次數
- 進化穩定性 (evo_stability): 連續世代表現波動
```

---

## 3️⃣ 成功指標閾值

| 指標 | 最低目標 | 優秀標準 |
|------|---------|---------|
| success_rate | > 60% | > 85% |
| avg_reward | +0.5 | +1.5 |
| action_entropy | > 1.0 | > 1.5 |
| trap avoidance | > 50% | > 80% |

---

## 4️⃣ 實驗記錄模板

```json
{
  "generation": 1,
  "environment": "grid_5x5",
  "population": 10,
  "results": {
    "survival_rate": 0.75,
    "success_rate": 0.60,
    "avg_reward": 0.8,
    "action_entropy": 1.2
  },
  "evolution": {
    "new_neurons": 3,
    "pruned_connections": 5,
    "best_strategy": "avoid-then-seek"
  },
  "lessons_learned": [
    "avoid dead ends",
    "hug wall when lost"
  ]
}
```

---

## 🚀 下一步

1. **環境搭建** - 選擇測試框架 (Python/Gym)
2. **神經元實現** - 關聯學習演算法
3. **執行實驗** - 跑 10+ 世代
4. **分析結果** - 對比 Baseline

需要我開始寫程式碼實現嗎？
