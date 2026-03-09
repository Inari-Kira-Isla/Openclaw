# 自動化數據收集系統

## 目標
自動收集和分析技能使用數據

## 收集流程

```
1. 觸發條件
   ↓
2. 數據記錄
   ↓
3. 格式驗證
   ↓
4. 數據清理
   ↓
5. 分類存儲
   ↓
6. 統計分析
   ↓
7. 生成報告
```

## 觸發條件

| 觸發類型 | 條件 | 動作 |
|----------|------|------|
| 技能使用 | 每次調用 | 記錄數據 |
| 任務完成 | success=true | 計算經驗值 |
| 低評分 | rating<3 | 標記問題 |
| 定時 | 每天 18:00 | 生成報告 |

## 自動化腳本

### 數據記錄腳本
```python
def record_skill_usage(agent, skill, context, success, rating, duration):
    data = {
        "agent": agent,
        "skill": skill,
        "timestamp": get_timestamp(),
        "context": context,
        "success": success,
        "rating": rating,
        "duration_seconds": duration
    }
    save_to_raw(data)
    validate_and_clean(data)
    return data
```

### 定時報告腳本
```python
def generate_daily_report():
    data = load_cleaned_data()
    stats = calculate_stats(data)
    report = create_report(stats)
    save_report(report)
    return report
```

## 數據流向

```
┌─────────────┐
│  技能使用   │
└──────┬──────┘
       ↓
┌─────────────┐     ┌─────────────┐
│  數據記錄   │────→│  Raw 數據   │
└──────┬──────┘     └─────────────┘
       ↓
┌─────────────┐     ┌─────────────┐
│  格式驗證   │────→│  Cleaned    │
└──────┬──────┘     └─────────────┘
       ↓
┌─────────────┐     ┌─────────────┐
│  統計分析   │────→│  Aggregated │
└──────┬──────┘     └─────────────┘
       ↓
┌─────────────┐     ┌─────────────┐
│  生成報告   │────→│  Reports    │
└─────────────┘     └─────────────┘
```

## 設定

### Cron Job（每天 18:00）
```json
{
  "schedule": "0 18 * * *",
  "task": "generate_daily_report"
}
```

### 質量檢查（每次記錄）
- 必填欄位檢查
- 數值範圍檢查
- 時間格式檢查

## 下一步
1. 部署自動化腳本
2. 設定定時任務
3. 開始收集數據
