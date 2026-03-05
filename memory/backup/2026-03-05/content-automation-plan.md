# Content Automation Plan - Lazy Uni Shop

**日期**: 2026-02-20

---

## 計劃名稱

**Content Generation Automation** - Lazy Uni Shop 內容自動化

---

## 目標

建立自動化內容生成流程，生產高質量社交媒體內容

---

## 靈感來源

Joe 既 TikTok UGC 自動化系統：
- Claude Code + Manus
- Clickup 任務管理
- Human in Loop 審核
- 多平台發佈

---

## OpenClaw 版本架構

### 系統組件

| 組件 | 功能 |
|------|------|
| Notion | 題目資料庫 |
| Web Search | 素材搜集 |
| OpenClaw | Thread 生成 |
| Telegram | 審批確認 |
| n8n | 自動化排程 |

### 流程圖

```
Schedule (每4小時)
    ↓
Notion (搵新題目)
    ↓
Web Search (搜素材)
    ↓
OpenClaw (生成 Thread)
    ↓
Telegram (審批)
    ↓
手動發佈 / 自動發佈
```

---

## 檔案清單

| 檔案 | 說明 |
|------|------|
| n8n_workflows/content-generation.json | n8n workflow v1 |
| n8n_workflows/content-generation-v2.json | n8n workflow v2 (完整版) |
| n8n_workflows/content-generation_README.md | 說明文件 |
| scripts/notion_content_db.json | Notion 資料庫結構 |
| scripts/setup_content_gen.sh | 設定腳本 |

---

## 當前狀態

**⚠️ 暫停中** - 優先處理 CarPlay 計劃

### ✅ 已完成
- Thread 生成器 Skill
- Notion Database Schema
- n8n Workflow (v2)
- 設定腳本

### ⏳ 待辦
- 填寫環境變數
- Import workflow 到 n8n
- 設定 credentials

---

## 設定項目

### 1. Notion Database
- 建立 Content Topics Database
- 欄位：Topic, Status, Created, Platform

### 2. Telegram
- 取得 Chat ID
- 設定審批訊息格式

### 3. OpenClaw
- 確認 API Token

### 4. Serper/You.com
- API Key 設定

---

## 功能清單

### Level 1: 基礎
- [x] Thread 生成器 Skill
- [x] 素材搜集 Skill
- [x] Notion 整合

### Level 2: 自動化
- [ ] n8n workflow import
- [ ] Schedule trigger 設定
- [ ] Telegram 審批

### Level 3: 進階
- [ ] AI 圖片生成
- [ ] 多平台自動發佈
- [ ] 成效追蹤

---

## 安全考量

### 素材合法性
- 優先使用 AI 生成圖片
- Unsplash / Pexels 備用
- 避免 Google 圖片

### 內容合規
- 避免抄襲
- 標註來源
- 符合平台規範

---

## 時間線

| 階段 | 時間 | 內容 |
|------|------|------|
| Phase 1 | Day 1-2 | 設定 Notion + Thread 生成器 |
| Phase 2 | Day 3-4 | n8n workflow + Telegram |
| Phase 3 | Day 5-7 | 測試 + 優化 |
| Phase 4 | Week 2 | 加入圖片 + 發佈 |

---

## 預期效果

| 指標 | 目標 |
|------|------|
| 每日產出 | 1-3 篇 Thread |
| 準備時間 | < 30 分鐘 |
| 發佈時間 | < 5 分鐘 |
| 總效率提升 | 80% |

---

## 風險與對策

| 風險 | 對策 |
|------|------|
| 內容質量 | Human Review 把關 |
| 素材侵權 | AI 生成為主 |
| 平台限制 | 多元化發佈 |
| 算法變化 | 持續監測調整 |

---

## 成功關鍵

1. **Human in Loop** - 審批不可或缺
2. **質量 > 數量** - 寧缺毋濫
3. **持續優化** - 根據數據調整
4. **多元化** - 多平台發佈

---

## 下一步行動

- [ ] 匯入 n8n workflow
- [ ] 設定 Notion Database
- [ ] 測試整條流程
- [ ] 開始每日使用

---
