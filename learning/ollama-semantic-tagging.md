# 學習更新優化 - Ollama 驅動語義標籤

**來源**: AI 系統架構師建議
**日期**: 2026-02-18
**版本**: v1.3

---

## 🎯 核心理念

> 從 LLM 生成標籤到 Embedding，完全本地運行，0 API 費用

---

## 🛠️ 進階版腳本功能

### 1. 語義注入 (Semantic Injection)

| 傳統方式 | 進階方式 |
|----------|----------|
| 單純切碎文字 | Ollama 生成語義標籤 |
| 無背景資訊 | 每個碎片帶上前缀標籤 |
| 關鍵字匹配 | 語義理解匹配 |

### 2. 標籤生成模板

```
【領域/關鍵字 | 摘要】
例如：
【海膽/成本分析 | 2026年A級馬糞海膽市場價格趨勢】
```

---

## 📋 配置說明

```python
OBSIDIAN_VAULT_PATH = "./MyObsidianVault"  # 筆記路徑
VECTOR_DB_PATH = "./.vectors/athena_brain"  # 向量庫路徑
OLLAMA_MODEL = "llama3"  # 本地 LLM 模型
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

---

## 💡 優勢

| 項目 | 效果 |
|------|------|
| 語義理解 | 搜尋「海膽成本」即使內文沒有，也能匹配 |
| 完全本地 | 0 API 費用，資料不離開 Mac |
| 助理分工 | Athena (SOP)、QI (分析)、DDH (決策) 分類 |

---

## 🔧 需要的環境

1. **Ollama** - 本地 LLM
2. **LangChain** - Python 套件
3. **HuggingFace Embeddings** - 本地向量

---

## 📝 下一步

需要我幫你寫「檢索測試腳本」嗎？

---

*記錄時間: 2026-02-18*
