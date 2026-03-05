# OpenClaw 中控模式 (Manager Mode) 詳解

**日期**: 2026-02-20
**來源**: 系統架構師分享

---

## 什麼是中控模式？

在 OpenClaw 框架中，**中控模式 (Manager Mode)** 是處理複雜、非線性任務的核心。在這種模式下，你不需要手動排列任務順序，而是指派一個具有「大腦」功能的 Manager Agent。它會像專案經理一樣，分析當前任務，並決定由哪位專家 Agent 來執行。

> 適合那種「問題不明確，需要先分析再拆解」的場景。

---

## 實現示例

```python
from openclaw import Agent, Task, Workflow

# 1. 定義管理者 LLM (建議 GPT-4o 或 Claude 3.5)
manager_llm = ChatOpenAI(model="gpt-4o")

# 2. 定義專業 Agent (執行者)
coder = Agent(
    name="資深工程師",
    role="撰寫高品質 Python 代碼",
    goal="開發穩定且高效的腳本",
    backstory="對代碼整潔度有強迫症的工程師"
)

designer = Agent(
    name="UI/UX 設計師",
    role="設計使用者介面",
    goal="提升產品的易用性與美感"
)

# 3. 定義總體任務
main_task = Task(
    description="開發自動分析海鮮價格趨勢的網頁工具",
    expected_output="設計草圖 + 核心代碼"
)

# 4. 配置中控模式
workflow = Workflow(
, designer],
       agents=[coder tasks=[main_task],
    process="manager",  # 啟用中控模式
    manager_llm=manager_llm
)

# 5. 啟動
result = workflow.kickoff()
```

---

## 工作原理

### 1. 任務分發 (Task Routing)
當任務進來時，Manager 會先評估：「這個任務需要什麼？」

### 2. 動態調度
Manager 會依序點名專家 Agent，根據草圖寫代碼。

### 3. 品質把關
Manager 審核輸出，如果不滿意會退回重做，直到符合預期。

---

## 模式比較

| 模式 | 適用場景 | 複雜度 |
|------|----------|--------|
| **Sequential** | 流程固定、A 做完給 B | 低 |
| **Manager** | 跨領域協作、目標模糊 | 高 |

---

## 什麼時候用？

- 任務目標不明確
- 需要跨領域協作
- 執行順序不確定
- 需要品質把關

---

## 與 muse-core 的關係

我們的架構已經是這種模式：

| 元件 | 角色 |
|------|------|
| **muse-core** | Manager |
| **各專業 Agent** | Expert Agents |

---

## 提示

> Manager Agent 本身不需要定義具體的 backstory，但如果你想讓這位經理更有「個性」，可以單獨為它建立 Agent 物件並指派給 manager_agent 參數。

---

## 相關主題

- Long-term Memory (長期記憶)
- Agent 偏好記憶
- 品質把關機制

---
