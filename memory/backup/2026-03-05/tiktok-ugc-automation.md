# TikTok UGC 影片自動化工具

**日期**: 2026-02-20
**作者**: Joe

---

## 系統架構

```
Claude Code + Manus
    ↓
Clickup (120 Topics ToDo)
    ↓
Manus Skills (自動化)
    ↓
Webapp (Human in Loop)
    ↓
發佈到 IG Reels, TikTok, YouTube Shorts
```

---

## Manus Skills 流程

### 1. 每日題目搜尋
- 從 Clickup ToDo list 搵未做既新題目

### 2. 相片搜尋 + 視覺檢查
- 基於題目搜尋相片
- 用 LLM 視覺檢查相片會否重複
- (一般搜尋只靠 description，唔會真正睇相)

### 3. 相片處理
- 裁剪成 9:16
- 一個場景放四張

### 4. 內容生成
- Generate Heygen 對白

### 5. 發佈相片
- IG Reels
- TikTok
- Pinterest

### 6. 影片處理
- 發佈到自己既 Webapp
- Webapp = 最後檢查 + 微調 (Human in the Loop)
- 確認後發佈到 IG Reels, TikTok, YouTube Shorts

### 7. 狀態更新
- Clickup ToDo 改為 completed
- 明日重複

---

## 工具選擇

| 工具 | 原因 |
|------|------|
| Clickup | 免費 + Manus 內置 MCP |
| Claude Code | AI 编程 |
| Manus | 自動化 Agent |
| 自建 Webapp | Human in the loop |

---

## SaaS 未來睇法

> 多人討論：未來是否仲需要 SaaS 軟件？

**我相信：**
- 仲需要既
- 但需求會大幅減少

**證據：**
- AppSumo 創辦人分享
- 收入跌咗一半

---

## 啟示

1. **AI Agent 可以取代大部分 SaaS 功能**
2. **但人類審核仍然重要** (Human in the Loop)
3. **自建工具 > 購買 SaaS** (長期)

---
