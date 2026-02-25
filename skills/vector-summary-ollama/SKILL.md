---
name: vector_summary_ollama
description: 本地 Ollama 向量摘要生成。當需要使用本地模型對 Notion 筆記進行向量化摘要時觸發，包括：文本切分、Ollama 摘要生成、向量化、本地儲存。
---

# 向量摘要（Ollama 版本）

## 功能說明

使用本地 Ollama（llama3）生成 Notion 筆記的向量摘要，免費且快速。適合日常批次處理及自動化場景。

## 前置條件

- Ollama 已安裝且正在運行（`ollama serve`）
- llama3 模型已下載（4.7GB）
- Python 3 可用

## 工作流程

### 第一步：文本切分
- 將長文本切分成多段，每段約 250 字
- 以句號、驚嘆號等標點作為切分點
- 過濾低於 20 字的無效片段

### 第二步：Ollama 摘要生成
- 使用 llama3 對每個片段生成 30 字以內的精簡摘要
- 提示詞：「用30字以內摘要核心概念：{片段內容}」

### 第三步：向量化
- 將摘要轉為 128 維向量
- 進行歸一化處理

### 第四步：本地儲存
- 儲存位置：`~/Desktop/vector-db/`
- 檔案格式：`{page_id}.json`

### 第五步：相似度檢索
- 使用餘弦相似度進行比對
- 返回最相關的片段

## 工具指引

```bash
# 確保 Ollama 運行
ollama serve

# 處理最新 Notion 頁面
python scripts/vector_summary_ollama.py

# 處理所有頁面
python scripts/vector_summary_ollama.py --all
```

腳本位置：`scripts/vector_summary_v2.py`

## 與 MiniMax 版本比較

| 項目 | Ollama | MiniMax |
|------|--------|---------|
| 品質 | 中 | 高 |
| 速度 | 快 | 慢 |
| 成本 | 免費 | API 按量計費 |
| 適用 | 日常批次 | 首次高品質處理 |

## 錯誤處理

| 情境 | 處理方式 |
|------|----------|
| Ollama 未啟動 | 自動嘗試執行 `ollama serve`，失敗則提示用戶手動啟動 |
| 模型未下載 | 提示執行 `ollama pull llama3` |
| 文本為空 | 跳過該頁面，記錄到日誌 |
| 向量庫目錄不存在 | 自動建立 `~/Desktop/vector-db/` |
| 摘要品質過低 | 建議切換到 MiniMax 驗證版本 |

## 使用範例

- 「用 Ollama 處理最新的 Notion 筆記」
- 「批次向量化所有未處理的筆記」
- 「用本地模型跑一次向量摘要」

## 護欄

- 不修改 Notion 原始內容，僅生成摘要
- 每段摘要不超過 30 字
- 區塊數量限制 1-11 個
- 向量維度固定 128 維
- 不將本地資料上傳至外部服務
