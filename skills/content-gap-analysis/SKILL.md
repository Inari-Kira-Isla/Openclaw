---
name: content-gap-analysis
description: |
  內容缺口分析系統。當需要分析現有內容、找出擴展方向、規劃內容策略時使用。
  功能：(1) 分析現有內容分佈 (2) 識別缺口 (3) 推薦新主題 (4) 制定擴展計畫。
  適用場景：(1) 內容規劃 (2) 擴展方向 (3) 每日內容生成
metadata:
  {
    "openclaw": { "emoji": "📊", "requires": { "anyTools": ["exec", "read"] } },
  }
---

# Content Gap Analysis

內容缺口分析與擴展規劃系統

## 現狀分析

### 內容分佈

| 類型 | 數量 | 佔比 |
|------|------|------|
| 系統提示詞 | 47 | 47% |
| 提示詞模板 | 21 | 21% |
| 工具設定 | 17 | 17% |
| 工作流 | 14 | 14% |
| 案例分析 | 1 | 1% |

### 熱門主題

- OpenClaw (4)
- API (3)
- n8n (2)
- GitHub Actions (2)
- Claude (2)

## 未來擴展方向

### 1. AI 基礎 (6 個新主題)

| 主題 | 類型 |
|------|------|
| 機器學習基礎 | system_prompt |
| 深度學習原理 | tutorial |
| 神經網路入門 | tutorial |
| NLP 基礎 | tutorial |
| 電腦視覺基礎 | tutorial |
| AI 倫理 | system_prompt |

### 2. AI 應用 (6 個新主題)

| 主題 | 類型 |
|------|------|
| AI 寫作 | prompt_template |
| AI 圖像生成 | tool_setup |
| AI 影片製作 | workflow |
| AI 音頻處理 | tool_setup |
| AI 翻譯 | prompt_template |
| AI 程式開發 | workflow |

### 3. Prompt 工程 (6 個新主題)

| 主題 | 類型 |
|------|------|
| Chain-of-Thought | prompt_template |
| Tree of Thoughts | prompt_template |
| ReAct | prompt_template |
| Few-shot Learning | prompt_template |
| 角色扮演 | system_prompt |
| 情境設計 | prompt_template |

### 4. 工具深度 (6 個新主題)

| 主題 | 類型 |
|------|------|
| ChatGPT 進階 | tool_setup |
| Claude 深度 | system_prompt |
| Midjourney | tool_setup |
| Stable Diffusion | tool_setup |
| ComfyUI | tool_setup |
| Perplexity | tool_setup |

### 5. API 整合 (6 個新主題)

| 主題 | 類型 |
|------|------|
| OpenAI API | tool_setup |
| Anthropic API | tool_setup |
| Google AI API | tool_setup |
| 本地 API 部署 | tool_setup |
| API 代理 | workflow |
| API 閘道 | tool_setup |

### 6. 企業應用 (6 個新主題)

| 主題 | 類型 |
|------|------|
| 客服自動化 | workflow |
| 內部知識庫 | tool_setup |
| 文檔處理 | workflow |
| 數據分析助手 | system_prompt |
| 報告自動化 | workflow |
| 決策支援 | system_prompt |

### 7. 開源專案 (6 個新主題)

| 主題 | 類型 |
|------|------|
| LangChain | tool_setup |
| LlamaIndex | tool_setup |
| AutoGPT | tool_setup |
| BabyAGI | tool_setup |
| MetaGPT | tool_setup |
| ChatDev | tool_setup |

### 8. 硬體與部署 (6 個新主題)

| 主題 | 類型 |
|------|------|
| GPU 選購 | tutorial |
| 雲端 GPU | tool_setup |
| 模型量化 | tool_setup |
| 邊緣部署 | tool_setup |
| 行動裝置部署 | tool_setup |
| 嵌入式 AI | tutorial |

## 使用方式

```bash
# 分析缺口
python3 ~/.openclaw/workspace/aeo-site/scripts/content_gap_analysis.py

# 生成新內容
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type tool_setup --topic "LangChain"
```

## 擴展策略

### 短期 (1-2週)

1. **Prompt 工程** - 最快補充
   - Chain-of-Thought
   - Few-shot Learning
   
2. **熱門工具** - 需求高
   - ChatGPT 進階
   - Claude 深度

### 中期 (1個月)

3. **企業應用** - 商業價值
   - 客服自動化
   - 內部知識庫

4. **開源專案** - 技術深度
   - LangChain
   - LlamaIndex

### 長期 (2-3個月)

5. **AI 基礎** - 長期價值
   - 機器學習基礎
   - 深度學習原理

6. **硬體部署** - 進階主題
   - GPU 選購
   - 模型量化

## 自動化

```bash
# 每日生成新類別
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate \
  --type prompt_template \
  --topic "Chain-of-Thought"
```

## 總結

- **現有**: 100 篇
- **可擴展**: 48 個新主題
- **類別**: 8 大領域
- **優先順序**: Prompt 工程 → 工具 → 企業應用 → 基礎

持續擴展，未來可達 150+ 篇！
