---
name: sync_review
description: 間隔複習管理。查看今天待複習項目、標記已複習、手動觸發同步。
---

# Sync & Review — 複習管理

## 操作步驟

1. 用 `knowledge_hub_db.get_due_reviews()` 取得待複習列表
2. 逐一顯示知識卡片（標題、分類、內容、階段）
3. 使用者確認複習後，用 `mark_reviewed()` 推進複習階段
4. 推送變更到 Google Sheets

## 複習間隔

| 階段 | 間隔 | 說明 |
|------|------|------|
| Stage 0 → 1 | 1 天 | 首次複習 |
| Stage 1 → 2 | 7 天 | 短期鞏固 |
| Stage 2 → 3 | 30 天 | 長期記憶 |
| Stage 3 | 完成 | 不再提醒 |

## 工具指引

- **knowledge_hub_db.py**
  - `get_due_reviews()` — 取得今日待複習
  - `mark_reviewed(learning_id, confidence)` — 推進階段
  - `pull_from_sheets()` — 強制同步
  - `push_to_sheets(tab_name)` — 推送變更

## 使用範例

- 「今天要複習什麼」
- 「標記 L-042 已複習」
- 「同步 Knowledge Hub」
- 「所有待複習項目」
