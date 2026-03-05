# 🦞 Lobster AI 系統設計

## 核心目標
- 記住犯過的錯，不再重蹈覆轍
- 記住做得好的工作流程，持續優化

---

## 系統架構

```
lobster/
├── memory.py          # 記憶系統 (Associate Learning)
│   ├── error_log      # 錯誤記錄
│   └── success_log    # 成功經驗
├── brain.py           # 決策網絡
├── notifier.py        # 自動通知/驗證
├── notion_sync.py     # Notion 資料庫同步
└── main.py            # 實驗入口
```

---

## 記憶數據結構

### 錯誤記錄 (Error Log)
```json
{
  "id": "err_001",
  "action": "move_forward",
  "state": "near_cliff",
  "outcome": "fell",
  "severity": "critical",
  "timestamp": "2026-02-28T09:00:00Z",
  "lesson": "don't move forward near cliff",
  "fix_count": 0
}
```

### 成功記錄 (Success Log)
```json
{
  "id": "suc_001",
  "workflow": "hunt_food",
  "steps": ["detect_food", "approach", "grab", "eat"],
  "outcome": "success",
  "efficiency": 0.85,
  "timestamp": "2026-02-28T09:10:00Z"
}
```

---

## 自動化流程

1. **感知** → 讀取當前狀態
2. **決策** → 查詢記憶，避開錯誤參考成功
3. **執行** → 採取行動
4. **記錄** → 自動存儲結果到記憶庫
5. **驗證** → 定時檢查錯誤是否重複
6. **同步** → 自動寫入 Notion

---

## Notion 資料庫

### Error Database
| 欄位 | 類型 |
|------|------|
| Action | Text |
| State | Text |
| Outcome | Select |
| Severity | Select |
| Lesson | Text |
| Fix Count | Number |

### Success Database  
| 欄位 | 類型 |
|------|------|
| Workflow | Text |
| Steps | Multi-select |
| Outcome | Select |
| Efficiency | Number |

---

## 下一步

1. ✅ 設計完成
2. 🔧 開始寫 memory.py
3. 🔧 寫 brain.py
4. 🔧 整合 Notion
5. 🧪 測試

確認請回覆 ✅ 開始寫 code
