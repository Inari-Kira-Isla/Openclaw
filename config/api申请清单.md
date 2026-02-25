# 有用 API 申請清單

**建立日期**: 2026-02-19
**目的**: 優化 OpenClaw 系統

---

## 🎯 高優先級

### 1. Brave Search API (Web Search)
| 項目 | 內容 |
|------|------|
| **官網** | https://brave.com/search/api/ |
| **免費額度** | 2,000 次/月 |
| **用途** | Web Search 備用 |
| **狀態** | ❌ 未申請 |

### 2. Serper API (Google Search)
| 項目 | 內容 |
|------|------|
| **官網** | https://serper.dev/ |
| **免費額度** | 2,500 次/月 |
| **用途** | Google 搜尋結果 |
| **狀態** | ❌ 未申請 |

---

## 📋 中優先級

### 3. Tavily AI (AI Search)
| 項目 | 內容 |
|------|------|
| **官網** | https://tavily.com/ |
| **免費額度** | 1,000 次/月 |
| **用途** | AI 優化搜尋 |
| **特點** | 為 LLM 優化 |

### 4. Jina AI (Summarization)
| 項目 | 內容 |
|------|------|
| **官網** | https://jina.ai/ |
| **免費額度** | 免費開源 |
| **用途** | 文章摘要/擷取 |
| **狀態** | 可考慮 |

---

## 🔧 系統優化用

### 5. GitHub API
| 項目 | 內容 |
|------|------|
| **官網** | https://github.com/features/actions |
| **免費額度** | 免費 |
| **用途** | 監控 OpenClaw 更新 |
| **狀態** | ✅ 可用 |

### 6. npm Registry API
| 項目 | 內容 |
|------|------|
| **官網** | https://registry.npmjs.org/ |
| **免費額度** | 免費 |
| **用途** | 檢查 npm 套件更新 |

---

## 📊 建議申請順序

| 順序 | API | 理由 |
|------|-----|------|
| 1 | **Serper** | Google 結果，備用搜尋 |
| 2 | **Tavily** | AI 優化搜尋 |
| 3 | **Brave** | Web Search 備用 |

---

## 🎯 立即行動

### 申請 Serper (最快)
1. 前往 https://serper.dev/
2. 用 GitHub 登入
3. 取得 API Key
4. 設定到 config

---

## 📝 API Key 記錄格式

```yaml
# config/api-keys.yaml
serper_api_key: "your-key"
tavily_api_key: "your-key"
brave_api_key: "your-key"
you_api_key: "ydc-sk-..."
```

---
