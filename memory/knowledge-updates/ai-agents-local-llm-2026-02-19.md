# 知識庫更新 - AI Agents 與本地 LLM 趨勢 (2026-02-19)

## 來源
- Hugging Face Blog: Upskill - We Got Claude to Build CUDA Kernels
- Hugging Face Blog: Transformers.js v4 Preview

---

## 1. Agent Skills (Upskill)

### 核心概念
- 使用強大模型（Claude Opus 4.5）創建技能（Skills），傳遞給較小的本地模型
- 教師-學生方法：強大模型生成技能和測試用例，較小模型使用技能執行任務

### 效果數據
| 模型 | 基礎準確率 | 使用技能後 | 提升 |
|------|-----------|-----------|------|
| GPT-OSS (開放模型) | 60% | 95% | +35% |
| GLM-4.7-Flash-GGUF:Q4_0 | 40% | 85% | +45% |

### 技能格式 (Agent Skills Specification)
```
skills/
├── SKILL.md        # 主要指令 (~520 tokens)
└── skill_meta.json # 元數據和測試用例
```

### 工作流程
1. 用強大模型完成任務並記錄 trace
2. 從 trace 生成 skill：`upskill generate "任務描述" --from ./trace.md`
3. 評估 skill 在目標模型上的表現：`upskill eval ./skills/my-skill/ --model haiku`
4. 迭代優化直到滿意
5. 部署到本地模型

### 工具
- **upskill**：pip install upskill
- **本地模型評估**：支援 Ollama、llama.cpp 等 OpenAI 兼容端點

### 應用場景
- CUDA kernel 開發
- 複雜程式碼任務
- 領域特定問題
- 成本優化（昂貴模型用於創建技能，便宜模型用於執行）

---

## 2. Transformers.js v4

### 主要更新
- **WebGPU Runtime**：全新 C++ 重寫，與 ONNX Runtime 團隊合作開發
- **跨平台支援**：瀏覽器、Node.js、Bun、Deno
- **離線支持**：本地緩存 WASM 文件，無需網路連接

### 新架構支援
- **Mamba**：狀態空間模型（State-Space Models）
- **MLA**：多頭潛在注意力（Multi-head Latent Attention）
- **MoE**：混合專家（Mixture of Experts）
- 新模型：GPT-OSS, Chatterbox, GraniteMoeHybrid, LFM2-MoE, HunYuanDenseV1, Apertus, Olmo3, FalconH1, Youtu-LLM

### 效能數據
- **GPT-OSS 20B (q4f16)**：在 M4 Pro Max 上達 ~60 tokens/s
- **BERT 嵌入模型**：使用 MultiHeadAttention 運算子，達 ~4x 加速

### 構建優化
- **esbuild 取代 Webpack**：構建時間 2s → 200ms（10x 提升）
- **Bundle 大小**：平均減少 10%，transformers.web.js 減少 53%

### 獨立套件
- **@huggingface/tokenizers**：獨立分詞庫，8.8kB gzipped，零依賴

---

## 3. 行業趨勢總結

### 模型分工
- 昂貴模型（SOTA）用於：創建技能、解決複雜問題
- 便宜/本地模型用於：執行常見任務

### 瀏覽器 AI
- WebGPU 推動瀏覾器端本地 AI 應用
- 離線支援增強隱私和可靠性

### 開源生態
- DeepSeek 以來的開源 AI 生態系統持續成長
- 本地部署成本持續下降

---

## 4. 系統建議

### 短期（1-2 週）
- [ ] 評估現有 skill-creator 技能與 Upskill 概念的整合
- [ ] 測試本地模型 + skill system 的可行性

### 中期（1 個月）
- [ ] 建立 OpenClaw 專用的 Agent Skills 庫
- [ ] 探索 Transformers.js v4 的離線應用場景

### 長期（季度）
- [ ] 研究本地 LLM + Agent Skills 的自動化工作流
- [ ] 追蹤 WebGPU 技術在瀏覽器 AI 的發展

---

_Last Updated: 2026-02-19_
