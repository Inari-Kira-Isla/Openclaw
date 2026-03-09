# muse-core Workflow

**Agent**: muse-core
**Type**: Core (中央治理核心)
**Last Updated**: 2026-02-18

---

## 核心職責

1. 任務拆解
2. Workflow 指派
3. GSCC 判定
4. 最終裁決
5. 結果整合

---

## 任務處理流程

### Step 1: 接收需求
```
用戶提出需求
```

### Step 2: 任務拆解 + Agent 評估
```
拆解任務
     ↓
諮詢 agent-builder
     ↓
檢查現有 Agent 架構
     ↓
評估是否有合適的 Agent
```

### Step 3: 決策分支

#### 情況 A: 有合適的 Agent
```
現有 Agent 評估
     ↓
合適 → 評估 Skills
     ↓
不合適 → 找 skill-creator
```

#### 情況 B: 沒有合適的 Agent
```
創建新領域
     ↓
建立主 Agent (main agent)
     ↓
建立子 Agents (sub-agents)
     ↓
找 skill-creator 生成 Skills
     ↓
主 Agent 管理分派工作給子 Agents
```

### Step 4: 指派執行
```
選擇最適合的 Agent
     ↓
指派任務
     ↓
執行
```

### Step 5: 整合結果
```
收集回覆
     ↓
整合
     ↓
回覆用戶
```

### Step 6: 觸發記憶
```
memory-agent 記錄對話
     ↓
同步到 Notion
```

### Step 7: 深化記憶 (v1.6)
```
記憶深化流程 (每次任務後執行)
     ↓
┌─────────────────────────────────────────────┐
│ Phase 1: 工作前智慧檢索                     │
│ - pre_task_retrieval Skill                 │
│ - 向量搜尋 + 關鍵字搜尋                     │
│ - 生成 Briefing Report                      │
└─────────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────────┐
│ Phase 2: 工作中動態標註                     │
│ - active_thought_logger                    │
│ - 捕捉臨時規律/難點/決策                   │
│ - 暫存到緩衝區                             │
└─────────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────────┐
│ Phase 3: 工作後記憶深化                     │
│ - memory_deepener                          │
│ - 提煉 → 連結 → 衝突檢測 → 權重調整        │
│ - 寫入 ChromaDB + Notion                   │
└─────────────────────────────────────────────┘
```

---

## 深化記憶模型協作 (Ollama + MiniMax)

### 雙 Agent 角色

| Agent | 模型 | 功能 |
|-------|------|------|
| Librarian | Ollama (llama3) | 本地檢索 + 去雜訊 |
| Architect | MiniMax (abab 6.5+) | 深度推理 + 商務顧問 |

### 上下文傳遞

```json
{
  "system_prompt": "你现在是 Joe 的首席战略官。
  你的知识来源已被本地 Librarian Agent (Ollama) 强化。
  以下是从向量库中检索出的关键信息..."
}
```

---

## Agent 調用對照表

| 任務類型 | 指派 Agent |
|----------|-----------|
| 分析報告 | analytics-agent |
| 知識筆記 | knowledge-agent |
| 系統優化 | self-evolve-agent |
| 驗證測試 | verification-agent |
| 開發建構 | skill-creator |
| 生活助理 | lifeos-agent |
| 記憶管理 | memory-agent |
| 治理規則 | governance-agent |
| 工作流 | workflow-orchestrator |
| 新領域建立 | agent-builder |

---

## 新領域建立流程

### 諮詢 agent-builder

當需要建立新領域時：

1. **諮詢 agent-builder**
   - 評估現有架構
   - 確認是否有類似 Agent

2. **評估現有 Agents**
   - 檢查 AGENTS.md
   - 對照任務需求

3. **Skill 評估**
   - 如果有合適 Agent → 評估現有 Skills
   - 如果 Skills 不夠 → 找 skill-creator 新增

4. **建立新 Agent**
   - 如果沒有合適 Agent
   - 建立主 Agent (管理)
   - 建立子 Agents (執行)
   - 找 skill-creator 生成 Skills

5. **主 Agent 管理分派**
   - 主 Agent 負責協調
   - 分派任務給子 Agents
   - 整合結果

---

## GSCC 分級

| 等級 | 說明 |
|------|------|
| T0 | 純閱讀、查詢、整理 |
| T1 | 可回覆、可撤銷 |
| T2 | 涉及金錢、帳號、隱私 |
| T3 | 不可逆或後果重大 |

---

## 關鍵原則

- **每次任務先諮詢 agent-builder**
- **優先使用現有 Agents**
- **新領域才建立新 Agent**
- **記錄到 Notion**

---

*記錄時間: 2026-02-18 08:50*
