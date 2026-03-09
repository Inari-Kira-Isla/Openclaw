# 📚 共享知識庫 - Kira & Isla

## 目錄結構

```
shared_knowledge/
├── index.json          # 索引配置
├── status.json         # 同步狀態
├── discussions/       # 討論記錄
│   └── YYYY-MM-DD/
│       └── discussion_*.md
└── knowledge/         # 知識庫
    └── topic_*.md
```

## Agent 角色

| Agent | 功能 |
|-------|------|
| **Kira** | 語音轉文字、截圖傳送、檔案操作、訊息傳送、TTS |
| **Isla** | 網頁瀏覽、資料抓取、Gemini AI、內容生成 |

## 使用方式

1. **寫入知識**：寫入 `shared_knowledge/knowledge/` 或 `discussions/`
2. **更新索引**：更新 `index.json`
3. **更新狀態**：更新 `status.json`

## 同步規則

- 雙方都可讀寫
- 寫入後更新 `status.json` 的 `lastSync` 時間
- 記錄貢獻者

---

*Created: 2026-02-16*
