---
name: memory_deepener
description: 工作後記憶深化。進行記憶提煉、連結、衝突檢測和權重調整。
---

# 工作後記憶深化 (Memory Deepener)

## 功能說明

工作完成後進行記憶深化處理：
- 歸納 (Summarize)
- 連結 (Linking)
- 衝突檢測 (Conflict Resolution)
- 權重調整 (Weighting)

## 輸入

| 欄位 | 類型 | 說明 |
|------|------|------|
| task_result | string | 任務結果 |
| temp_thoughts | array | 工作中暫存的思考 |
| context | object | 任務上下文 |

## 輸出

| 欄位 | 類型 | 說明 |
|------|------|------|
| summary | string | 提煉的經驗規則 |
| linked_memories | array | 關聯的舊記憶 |
| conflict_flags | array | 衝突標記 |
| importance_score | number | 重要性分數 |

## 四步工作流

### Step 1: 歸納 (Summarize)

```
輸入：對話/任務內容
↓
LLM 提煉：這次學到了什麼新的業務邏輯？
↓
輸出：一條「經驗規則」
```

**範例**：
```
原始：用户询问如何设定 Facebook Webhook
提煉：Facebook Webhook 需要公开 URL，本地 n8n 需用 ngrok 或 cloud 版
標籤：#技術筆記 #Facebook #Webhook
```

### Step 2: 連結 (Linking)

```
提煉結果
↓
搜尋現有向量庫
- 相似記憶？
- 相關專案？
↓
建立關聯
```

**範例**：
```
新記憶：n8n Facebook 整合設定
關聯舊記憶：n8n Telegram 整合
→ 建立連結：屬於同一工作流系統
```

### Step 3: 衝突檢測 (Conflict Resolution)

```
新記憶 vs 舊記憶
↓
檢測衝突
↓
輸出：更新/矛盾/待確認
```

**處理方式**：
| 狀態 | 動作 |
|------|------|
| 衝突 | 標記「記憶更新」，保留新舊雙方 |
| 矛盾 | 標記「資料矛盾」，提示需要驗證 |
| 一致 | 正常儲存 |

### Step 4: 權重調整 (Weighting)

```
計算重要性分數
↓
調整 metadata
```

**權重因素**：
| 因素 | 權重 |
|------|------|
| 驗證正確 | +10 |
| 被引用次數 | +5/次 |
| 時間新舊 | +1/年 |
| 決策相關 | +15 |

---

## 輸出格式

```json
{
  "summary": "經驗規則",
  "tags": ["標籤1", "標籤2"],
  "linked_memories": ["相關記憶ID"],
  "conflict_flags": [],
  "importance_score": 8.5,
  "metadata": {
    "task_type": "學習",
    "created_at": "2026-02-18",
    "last_verified": "2026-02-18"
  }
}
```

---

## 使用時機

- 每次任務完成後
- 重要學習筆記
- 技術難題解決
- 決策記錄

---

*此技能用於記憶深化處理*
