# Token 調度管理 Skill

## 目的
防止短時間內大量 API 請求造成 rate limit，確保系統穩定運作。

## 核心機制

### 1. 調度策略
- **時間分片**：將密集任務分散到不同時間區間
- **優先級隊列**：高優先級任務優先處理
- **Token 配額**：每分鐘/每小時限制請求數

### 2. 速率限制規則
| 時間窗口 | 最大請求數 | 冷卻時間 |
|---------|-----------|---------|
| 每分鐘 | 10 請求 | 6 秒 |
| 每 5 分鐘 | 40 請求 | 3 秒 |
| 每小時 | 300 請求 | 1 秒 |

### 3. 錯峰排程
將 cron jobs 分散執行，避免同時觸發：
- `*/10` → `*/12` 或 `*/13`
- `*/15` → `*/15+offset`
- 30m → 25m 或 35m

## 使用方式

### 調度請求
```bash
# 調度任務，自動排隊
token-scheduler schedule --task "任務描述" --priority high|normal|low

# 檢查當前隊列狀態
token-scheduler status

# 緊急：立即執行（繞過排隊）
token-scheduler urgent --task "緊急任務"
```

### 配置示例
```json
{
  "rateLimit": {
    "perMinute": 10,
    "per5Minutes": 40,
    "perHour": 300
  },
  "schedules": {
    "heartbeat": "offset:5",
    "monitoring": "offset:3", 
    "cleanup": "offset:10"
  }
}
```

## 實現狀態
- [x] 速率限制邏輯
- [x] 優先級隊列
- [x] 調度配置
- [ ] 實際排隊執行（需整合 cron）

---
_更新：2026-03-01_
