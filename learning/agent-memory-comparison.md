# AI Agent 記憶機制比較：OpenClaw vs ZeroClaw vs OpenViking

**日期**: 2026-02-19
**來源**: Joe 分享

---

## 總覽

| 系統 | 類型 | 儲存方式 | 搜尋方式 |
|------|------|----------|----------|
| OpenClaw | Agent 框架 | Markdown 檔案 | BM25 + 向量混合 |
| ZeroClaw | Agent 框架 | SQLite | FTS5 + 向量 |
| OpenViking | 記憶服務 | 虛擬檔案系統 | 階層式檢索 |

---

## OpenClaw 記憶機制

### 核心理念
- **檔案優先，搜尋其次**
- Markdown 檔案是唯一的真相來源
- 人類可直接閱讀，可 Git 版本控制

### 搜尋機制
- **BM25** + **向量語意搜尋** 混合
- **時間衰減**（半衰期 30 天）
- **MMR** 多樣性重排序
- Embedding 支援：本地 GGUF、OpenAI、Gemini、Voyage
- **fallback**：全部掛了退回純關鍵字

### 寫入機制
- **Pre-compilation flush**：session 快觸發壓縮前，偷偷跑 agentic turn 寫入重要記憶
- **File watcher**：偵測檔案變動自動重新索引

---

## ZeroClaw 記憶機制

### 核心理念
- **零依賴，全部自幹**
- Rust 寫的，全部塞進 SQLite

### 搜尋機制
- FTS5 關鍵字搜尋 + 向量搜尋
- **問題**：向量是暴力掃描，量大會卡
- 預設 embedding provider 是 none

### 寫入機制
- 每 12 小時 Hygiene 清理
- 7 天日記歸檔
- 30 天直接刪除
- **靈魂備份**：匯出 MEMORY_SNAPSHOT.md

---

## OpenViking 記憶機制

### 核心理念
- **Context Database**
- 字節跳動/火山引擎團隊出品
- 虛擬檔案系統 (viking:// URIs)

### 搜尋機制
- **階層式檢索**：向量搜尋找目錄 → 遞迴往下鑽
- **L0/L1/L2 三層載入**：
  - L0：摘要 (~100 tokens)
  - L1：概覽 (~2000 tokens)
  - L2：完整內容

### 寫入機制
- Session 結束時用 LLM 萃取
- 6 類記憶：個人檔案、偏好、實體、事件、案例、模式
- CREATE/MERGE/SKIP 決策
- **缺點**：每次存記憶要叫好幾次 LLM

---

## 程式碼發現

### OpenClaw
- ✅ 所有官方功能 100% 驗證
- 🔎 藏了沒寫在文件裡的功能：中英文雙語查詢擴展、原子性索引重建

### ZeroClaw
- ⚠️ 有些功能寫了但沒接上
- Markdown chunker 存在但沒使用
- reindex 函式標了 #[allow(dead_code)]
- README 說預設 openai，但其實是 none

### OpenViking
- ⚠️ Dedup 只有三種決策（無 UPDATE）
- Rerank client 是 None + TODO

---

## OpenViking 整合計畫

### 現況
- OpenClaw 的 MemorySearchManager 介面乾淨
- 目前只支援內建 SQLite 和實驗性 QMD

### 挑戰
1. 設定檔要支援多後端
2. 需要 MemoryMultiplexManager
3. 結果合併要處理去重 + 分數正規化

### Joe 的計畫
- 已經動手整合 OpenViking
- 換成本地 embedding 模型 (nomic-embed-text)
- 等用一段時間後分享心得

---

## 對我們的意義

### 我們的現有系統
- ✅ Markdown 檔案當真相來源
- ✅ BM25 + 向量混合搜尋
- ✅ 時間衰減
- ✅ Pre-compaction flush

### 可以優化的地方
- 考慮整合 OpenViking
- 改進 LLM 萃取的頻率
- 優化向量搜尋效能

---

## 相關檔案

- `skills/memory-agent/` - 我們的記憶系統
- `config/vector-db.yaml` - 向量配置

---
