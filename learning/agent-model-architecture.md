# Agent 模型架構規劃

**日期**: 2026-02-19

---

## 當前所有 Agent

| # | Agent ID | 類型 | 模型策略 |
|---|----------|------|----------|
| 0 | main | 核心對話 | MiniMax → 本地 |
| 1 | muse-core | 治理核心 | MiniMax |
| 2 | workflow-orchestrator | 流程協調 | 本地 |
| 3 | skill-creator | 技能創建 | 本地 |
| 4 | mcp-builder | MCP 構建 | 本地 |
| 5 | verification-agent | 驗證代理 | 本地 |
| 6 | memory-agent | 記憶管理 | 本地 |
| 7 | skill-slime-agent | 技能進化 | MiniMax |
| 8 | self-evolve-agent | 自我進化 | MiniMax |
| 9 | analytics-agent | 數據分析 | 本地 |
| 10 | knowledge-agent | 知識管理 | 本地 |
| 11 | governance-agent | 治理裁決 | MiniMax |
| 12 | lifeos-agent | 生活助理 | 本地 |
| 13-20 | alice/bob/carol/dave/eva/georgia/isla | 團隊成員 | 本地 |
| 21 | note-taker | 筆記記錄 | 本地 |
| 22 | statistics-analyzer | 統計分析 | 本地 |
| 23 | code-master | 程式大師 | codellama ⭐ |
| 24 | design-master | 設計大師 | 本地 |
| 25 | writing-master | 寫作大師 | 本地 |
| 26 | evaluator | 評估師 | 本地 |
| 27 | agent-builder | Agent 構建 | 本地 |

---

## 模型分配策略

### 🔴 需要 MiniMax 驗證 (高複雜度)

| Agent | 原因 |
|-------|------|
| muse-core | 複雜決策、策略規劃 |
| skill-slime-agent | 技能進化判斷 |
| self-evolve-agent | 自我優化邏輯 |
| governance-agent | 規則裁決 |

### 🟡 可用本地模型 (中複雜度)

| Agent | 本地模型 | 原因 |
|-------|----------|------|
| workflow-orchestrator | llama3 | 流程邏輯 |
| skill-creator | llama3 | 技能設計 |
| memory-agent | llama3 | 記憶管理 |
| analytics-agent | llama3 | 數據分析 |
| knowledge-agent | llama3 | 知識搜尋 |

### 🟢 建議用專用模型

| Agent | 推薦模型 | 原因 |
|-------|----------|------|
| **code-master** | codellama | 程式碼專家 |
| **mcp-builder** | codellama | API 開發 |

### 🔵 可完全本地化

| Agent | 本地模型 |
|-------|----------|
| lifeos-agent | llama3 |
| alice/bob/... | llama3 |
| note-taker | llama3 |
| design-master | llama3 |
| writing-master | llama3 |

---

## 三階段規劃

### Phase 1: 混合模式 (現在)

```
模型選擇: MiniMax → 驗證 → 反饋記錄
```

| Agent | 初期模型 | 驗證 |
|-------|----------|------|
| 所有 Agent | 本地 | MiniMax |

### Phase 2: 分類優化 (1個月)

```
根據任務類型自動選擇
```

| 任務類型 | 模型 |
|----------|------|
| 程式碼 | codellama |
| 推理分析 | mistral |
| 一般對話 | llama3 |
| 複雜決策 | MiniMax |

### Phase 3: 自我優化 (3個月)

```
根據反饋自動調整
```

| 指標 | 動作 |
|------|------|
| 相似度 > 90% | 降低驗證頻率 |
| 相似度 < 70% | 觸發優化 |
| 新任務類型 | 添加新規則 |

---

## Fallback 機制

### 本地模型 Fallback

```
codellama 失敗 → mistral → llama3 → MiniMax
```

### API Fallback

```
Gemini 失敗 → Claude → MiniMax → 本地
```

---

## 整合到 Agent

### model-dispatcher Agent 職責

```
1. 接收任務
2. 分析任務類型
3. 選擇最適模型
4. 執行並驗證
5. 記錄反饋
6. 定期優化
```

### 與其他 Agent 互動

```
muse-core (調度)
    ↓
model-dispatcher (選模型)
    ↓
執行 Agent (使用本地/MiniMax)
    ↓
驗證結果
    ↓
記錄反饋 → 自我優化
```

---

## 優先順序

### 第一優先 (立即實作)

| Agent | 目標模型 | 原因 |
|-------|----------|------|
| code-master | codellama | 程式專家 |
| mcp-builder | codellama | API 開發 |

### 第二優先 (本週)

| Agent | 目標模型 | 原因 |
|-------|----------|------|
| workflow-orchestrator | 本地 | 日常流程 |
| skill-creator | 本地 | 技能創建 |

### 第三優先 (本月)

| Agent | 目標模型 | 原因 |
|-------|----------|------|
| 所有 Agent | 自動選擇 | 根據任務 |

---

## 檔案位置

- 配置: `config/model-dispatcher.yaml`
- 腳本: `scripts/local_model_optimizer.py`
- 工作流: `workflows/model-dispatcher-workflow.md`
- Skill: `skills/local-model-optimization/`

---
