# 應用分析：TikTok UGC 自動化 → Joe 既業務

**日期**: 2026-02-20

---

## 你現有既資源

| 資源 | 可以點用 |
|------|----------|
| OpenClaw | 自動化樞紐 |
| Claude Code | 編碼搭檔 |
| Manus | 未來可以試 |
| Notion | 內容管理 |
| n8n | 工作流程 |
| MiniMax / Ollama | 本地 AI |

---

## 可以複製既部分

### 1. 題目管理 (Clickup → Notion)

| Joe 做法 | OpenClaw 版本 |
|----------|---------------|
| Clickup ToDo | Notion Database |
| 120 Topics | 內容題目庫 |
| MCP 整合 | n8n Webhook |

### 2. 相片搜尋 + 檢查

| Joe 做法 | OpenClaw 版本 |
|----------|---------------|
| 網圖搜尋 | Web Search |
| LLM 視覺檢查 | 本地 LLM (Ollama) |
| 重複檢測 | 本地模型 |

### 3. Human in Loop

| Joe 做法 | OpenClaw 版本 |
|----------|---------------|
| 自建 Webapp | 簡易審核流程 |
| 最後把關 | Telegram 確認 |

---

## OpenClaw 改編版流程

```
1. 每日題目
   → Notion Database 搵新題目
   
2. 素材搜尋  
   → Web Search 搜尋圖片/資訊
   
3. 視覺檢查
   → Ollama 本地模型檢測
   
4. 內容生成
   → Thread 生成器 (已有！)
   → MiniMax 翻譯/改寫
   
5. Human Review
   → Telegram 發俾 Joe 確認
   
6. 發佈
   → n8n 發佈到社交平台
   
7. 記錄
   → Notion 更新狀態
```

---

## 立即可以做既事

### Level 1: 現有工具整合
- [ ] 將 Thread 生成器接到 Notion
- [ ] 加入 Web Search 素材收集
- [ ] Telegram 審核流程

### Level 2: 自動化
- [ ] n8n 每日自動生成題目
- [ ] 自動發佈到社交平台
- [ ] 成效追蹤

### Level 3: AI Agent 進化
- [ ] 加入 Manus / Claude Code
- [ ] 相片/影片處理
- [ ] 完全自動化 (除左 Human Review)

---

## 具體應用場景

### 場景 1: 財經博主 (Thread)

```
每日：
1. 搜尋財經新聞
2. 生成 Thread
3. 你確認
4. 自動發布
```

### 場景 2: 懶人包

```
每週：
1. 搜尋熱門話題
2. 生成懶人包
3. 你確認
4. 發布
```

### 場景 3: 產品推廣

```
收到新訂單：
1. 自動生成推文
2. 你確認
3. 發布到多平台
```

---

## 技術需求

| 功能 | 工具 |
|------|------|
| 自動化排程 | n8n / Cron |
| AI 生成 | MiniMax / Ollama |
| 搜尋 | Serper / You.com |
| 儲存 | Notion |
| 審核 | Telegram |
| 發布 | 各平台 API |

---

## 下一步

1. 將 Thread 生成器升級
2. 加入素材搜尋
3. 加入 Telegram 審核
4. 測試完整流程

---
