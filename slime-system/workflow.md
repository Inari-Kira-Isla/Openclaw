# 史萊姆學習記憶優化系統 - 工作流設計

> 版本：v1.0 | 設計日期：2026-02-27

---

## 1. 系統架構總覽

```
┌─────────────────────────────────────────────────────────────────┐
│                    Slime Learning System                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   輸入模組      │   處理模組      │   輸出/記憶模組              │
│  (Input)        │  (Processor)    │  (Memory/Output)            │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ • 學習事件      │ • 記憶編碼      │ • 長期記憶庫                 │
│ • 互動記錄      │ • 知識圖譜      │ • 提取器                     │
│ • 外部知識      │ • 遺忘曲線     │ • 複習排程                   │
└─────────────────┴─────────────────┴─────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   協調控制器      │
                    │  (Orchestrator)   │
                    └───────────────────┘
```

---

## 2. 任務排程機制

### 2.1 排程類型

| 排程類型 | 觸發條件 | 執行時機 | 優先級 |
|---------|---------|---------|--------|
| **即時任務** | 新學習事件入庫 | 立即執行 | P0 |
| **週期任務** | 時間驅動 | 每日/每週固定時間 | P1 |
| **事件任務** | 特定條件觸發 | 條件滿足時 | P1 |
| **批次任務** | 大量數據累積 | 低峰期執行 | P2 |

### 2.2 排程時間表

```yaml
schedules:
  daily_maintenance:
    time: "02:00"  # 每日凌晨進行記憶整合
    task: memory_consolidation
    
  review_scheduler:
    time: "08:00, 14:00, 20:00"  # 每日三次複習提醒
    task: review_dispatch
    
  garbage_collection:
    time: "03:00"  # 每日清理無用記憶
    task: memory_cleanup
    
  sync_external:
    interval: "6h"  # 每6小時同步外部知識
    task: external_sync
```

### 2.3 優先級队列

```
P0 (Critical): 即時學習反饋、錯誤修正
P1 (High):    定期複習、記憶鞏固
P2 (Normal):  知識整合、模式識別
P3 (Low):     長期優化、效能調校
```

---

## 3. 狀態追蹤流程

### 3.1 任務狀態機

```
┌──────────┐    submit     ┌─────────┐    start     ┌──────────┐
│  PENDING │ ──────────────▶│ RUNNING │ ────────────▶│ COMPLETED│
└──────────┘                └─────────┘              └──────────┘
      │                          │                         │
      │ submit                   │ start                   │ complete
      │ fail         ┌─────────┐ │ fail         ┌────────▼────────┐
      └─────────────▶│ FAILED  │◀┴─────────────▶│                 │
                     └─────────┘                │    CANCELLED    │
                                                └──────────────────┘
```

### 3.2 狀態欄位定義

| 欄位 | 類型 | 說明 |
|-----|------|-----|
| `task_id` | UUID | 唯一識別碼 |
| `task_type` | Enum | 任務類型 |
| `status` | Enum | PENDING/RUNNING/COMPLETED/FAILED/CANCELLED |
| `priority` | Integer | 優先級 (0-3) |
| `created_at` | Timestamp | 創建時間 |
| `started_at` | Timestamp | 開始時間 |
| `completed_at` | Timestamp | 完成時間 |
| `progress` | Float | 進度 (0.0-1.0) |
| `metadata` | JSON | 任務特定資料 |
| `retry_count` | Integer | 重試次數 |

### 3.3 狀態持久化

```python
# 狀態存儲結構
{
    "task_id": "slm_20260227_001",
    "type": "memory_consolidation",
    "status": "RUNNING",
    "progress": 0.45,
    "created_at": "2026-02-27T02:00:00Z",
    "started_at": "2026-02-27T02:00:01Z",
    "metadata": {
        "memory_blocks": 128,
        "processed": 57
    }
}
```

---

## 4. 協調各模組的工作流

### 4.1 主流程：學習輸入 → 記憶編碼 → 長期存儲

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Input     │────▶│  Processor  │────▶│   Memory    │
│   Module    │     │   Module    │     │   Module    │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Event Queue │     │  Task Queue │     │ State Store │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 4.2 詳細工作流步驟

#### 工作流 A：新規學習輸入

```yaml
name: New Learning Input
steps:
  - id: 1
    module: Input
    action: receive_learning_event
    output: raw_event
    
  - id: 2
    module: Processor
    action: encode_memory
    input: raw_event
    output: encoded_memory
    
  - id: 3
    module: Processor
    action: update_knowledge_graph
    input: encoded_memory
    output: graph_update
    
  - id: 4
    module: Memory
    action: store_to_short_term
    input: encoded_memory
    output: stored_ref
    
  - id: 5
    module: Memory
    action: schedule_review
    input: stored_ref
    output: review_task
```

#### 工作流 B：記憶提取與複習

```yaml
name: Memory Retrieval & Review
steps:
  - id: 1
    module: Scheduler
    action: trigger_review
    condition: time_based
    output: review_queue
    
  - id: 2
    module: Memory
    action: retrieve_memories
    input: review_queue
    output: memory_items
    
  - id: 3
    module: Processor
    action: calculate_retrieval_strength
    input: memory_items
    output: retrieval_probs
    
  - id: 4
    module: Output
    action: present_review_content
    input: retrieval_probs
    output: review_session
    
  - id: 5
    module: Input
    action: receive_feedback
    input: review_session
    output: feedback_data
    
  - id: 6
    module: Processor
    action: update_memory_strength
    input: feedback_data
    output: updated_memories
```

#### 工作流 C：記憶整合（夜間批次）

```yaml
name: Memory Consolidation (Nightly)
steps:
  - id: 1
    module: Scheduler
    action: nightly_trigger
    time: "02:00"
    
  - id: 2
    module: Memory
    action: collect_short_term_memories
    output: candidate_memories
    
  - id: 3
    module: Processor
    action: pattern_detection
    input: candidate_memories
    output: patterns
    
  - id: 4
    module: Processor
    action: merge_similar_memories
    input: patterns
    output: merged_memories
    
  - id: 5
    module: Memory
    action: transfer_to_long_term
    input: merged_memories
    output: long_term_refs
    
  - id: 6
    module: Memory
    action: prune_weak_memories
    input: all_memories
    output: cleanup_report
```

### 4.3 跨模組協調機制

```python
class Orchestrator:
    """工作流協調器"""
    
    def __init__(self):
        self.modules = {
            'input': InputModule(),
            'processor': ProcessorModule(),
            'memory': MemoryModule(),
            'output': OutputModule()
        }
        self.task_queue = TaskQueue()
        self.state_store = StateStore()
    
    async def execute_workflow(self, workflow_name: str, params: dict) -> dict:
        """執行指定工作流"""
        
        # 1. 加載工作流定義
        workflow = self.load_workflow(workflow_name)
        
        # 2. 創建任務並追蹤狀態
        task_id = await self.create_task(workflow_name, params)
        
        # 3. 逐步執行每個步驟
        context = {'params': params, 'task_id': task_id}
        
        for step in workflow.steps:
            # 檢查前置條件
            if not self.check_prerequisites(step, context):
                await self.handle_failure(task_id, "Prerequisites not met")
                break
            
            # 執行步驟
            result = await self.execute_step(step, context)
            
            # 更新上下文
            context[step.output] = result
            
            # 更新任務進度
            await self.update_progress(task_id, step.id, len(workflow.steps))
        
        # 4. 完成任務
        await self.complete_task(task_id, context)
        
        return context
```

---

## 5. 錯誤處理與重試

### 5.1 重試策略

| 錯誤類型 | 重試次數 | 間隔時間 | 備用動作 |
|---------|---------|---------|---------|
| 網路錯誤 | 3 | 2^n 秒 | 進入離線模式 |
| 記憶體不足 | 2 | 10 秒 | 釋放緩衝 |
| 處理失敗 | 3 | 5^n 秒 | 降級處理 |
| 外部服務 | 5 | 指數回退 | 使用快取 |

### 5.2 熔斷機制

```
連續失敗閾值: 5 次
熔斷恢復時間: 60 秒
降級模式: 僅寫入短期記憶，延遲處理
```

---

## 6. 監控與指標

### 6.1 關鍵指標

- **任務吞吐量**: 每分鐘處理任務數
- **平均延遲**: 任務提交到完成的時間
- **成功率**: 成功完成任務 / 總任務數
- **記憶效率**: 提取正確率 / 遺忘率
- **系統健康**: CPU、記憶體、磁碟使用率

### 6.2 日誌級別

```
DEBUG: 詳細執行步驟
INFO:  正常工作流程
WARN:  可恢復的錯誤
ERROR: 需要關注的錯誤
CRITICAL: 系統級故障
```

---

## 7. 配置文件

```yaml
# config/workflow.yaml
workflow:
  max_concurrent_tasks: 10
  task_timeout_seconds: 300
  retry_max: 3
  
scheduler:
  timezone: "Asia/Macau"
  enable_nightly_batch: true
  
monitoring:
  log_level: "INFO"
  metrics_interval: 60
```

---

*設計完成 - 可根據實際需求調整參數與流程細節*
