# Gene Capsule 格式標準

**版本**: 1.0
**建立日期**: 2026-02-20

---

## 膠囊結構

```yaml
type: gene_capsule
version: "1.0"
id: "gc_20260220_001"
name: "膠囊名稱"
description: "簡短描述"

# 核心內容
content:
  prompt: "..."
  context: "..."
  examples: [...]
  results: {...}

# 元數據
metadata:
  created_at: "2026-02-20T12:00:00Z"
  created_by: "agent_id"
  tags: ["tag1", "tag2"]
  
  # 評估數據
  success_rate: 0.85
  usage_count: 100
  avg_score: 4.5
  
  # 環境指紋
  environment:
    model: "MiniMax-M2.5"
    context: "telegram"
    channel: "direct"

# 審計日誌
audit:
  - action: "created"
    timestamp: "..."
    agent: "..."
  - action: "used"
    timestamp: "..."
    agent: "..."
```

---

## 膠囊類型

| 類型 | 說明 | 範例 |
|------|------|------|
| `prompt` | 提示詞膠囊 | 高效 Prompt |
| `skill` | 技能膠囊 | 特定任務技能 |
| `workflow` | 工作流膠囊 | 複雜流程 |
| `knowledge` | 知識膠囊 | 領域知識 |
| `memory` | 記憶膠囊 | 重要經驗 |

---

## 評分公式

```python
def calculate_score(capsule):
    # 基礎分數
    base = capsule.usage_count * capsule.success_rate
    
    # 衰減因子 (越老分數越低)
    age_days = (now - capsule.created_at).days
    decay = max(0.5, 1 - (age_days / 365))
    
    # 最終分數
    final_score = base * decay
    
    return final_score
```

---

## 膠囊狀態

| 狀態 | 說明 |
|------|------|
| `active` | 正常使用 |
| `recommended` | 高分推薦 |
| `deprecated` | 不建議使用 |
| `archived` | 已存檔 |

---

## 實施計劃

### Step 1: 格式定義 ✅
- [x] 定義膠囊結構
- [x] 定義類型
- [x] 定義評分公式

### Step 2: 存儲位置
- [ ] `memory/capsules/` - 膠囊存儲
- [ ] `memory/capsules/index.yaml` - 索引

### Step 3: 創建膠囊腳本
- [ ] `scripts/create_capsule.sh`
- [ ] `scripts/list_capsules.sh`
- [ ] `scripts/search_capsules.sh`

### Step 4: 整合
- [ ] 與現有記憶系統整合
- [ ] 與 Skills 系統整合

---
