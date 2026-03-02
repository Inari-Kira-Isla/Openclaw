---
name: auto-decide-hook
description: |
  自動決策鉤子。當需要決定下一步行動、但沒有明確指示時觸發。
  功能：(1) 評估當前狀態 (2) 基於規則自動決定 (3) 複雜決策調用 Claude CLI (4) 執行並回報。
  適用場景：(1) 完成任務後詢問下一步 (2) 需要在多個選項中選擇 (3) 系統提案後需要確認
metadata:
  {
    "openclaw": { "emoji": "🎯", "requires": { "anyTools": ["exec", "sessions_spawn", "memory_search"] } },
  }
---

# Auto-Decide Hook

自動決定下一步行動的鉤子

## 觸發條件

當聽到以下關鍵詞時觸發：
- "下一步"
- "接下來"
- "要做什麼"
- "what's next"
- "what to do next"
- **無回覆** (沉默一段時間後)

## 決策流程

```
┌─────────────────────────────────────────────────────┐
│                  觸發鉤子                            │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  1. 評估當前狀態                                    │
│     - 最近完成什麼                                   │
│     - 有哪些待辦                                      │
│     - 用戶偏好                                        │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. 規則匹配                                        │
│     - 有明確規則 → 執行規則                          │
│     - 無明確規則 → 進入決策                          │
└──────────────────────┬──────────────────────────────┘
                       ▼
        ┌──────────────┴──────────────┐
        ▼                                 ▼
┌───────────────────┐        ┌───────────────────┐
│  簡單決策          │        │  複雜決策          │
│  (基於規則)        │        │  (需要推理)        │
│  立即執行          │        │  spawn Claude     │
└───────────────────┘        └───────────────────┘
```

## 決策規則

### 簡單情況 (直接決定)

| 狀態 | 決定 |
|------|------|
| 網站已完成 | 預覽網站 |
| 內容生成完成 | 顯示統計 |
| 任務失敗 | 嘗試修復 |
| 用戶問"下一步" | 給出選項 |

### 複雜情況 (需要 Claude)

| 狀態 | 動作 |
|------|------|
| 多個方向都可以 | spawn Claude 評估 |
| 需要新技術評估 | spawn Claude 研究 |
| 策略性決策 | spawn Claude 分析 |

## 使用方式

### 基本觸發

```javascript
// 當用戶說"下一步"
if (message.includes("下一步") || message.includes("接下來")) {
  // 觸發 auto-decide hook
  await autoDecide(context);
}
```

### 手動觸發

```javascript
// 明確呼叫
autoDecide({
  context: currentProject,
  options: ["選項A", "選項B", "選項C"],
  constraints: ["時間限制", "資源限制"]
})
```

## Claude 決策 Prompt

```python
# 當需要 Claude 幫助時
prompt = """
## 上下文
{context}

## 選項
{options}

## 限制
{constraints}

## 任務
評估每個選項的優缺點，給出最終建議。

## 輸出格式
```
推薦: [選項]
理由: [原因]
風險: [需要注意的風險]
```
"""
```

## 實作範例

### 完整流程

```javascript
async function autoDecide(context) {
  // 1. 評估狀態
  const state = await assessState(context);
  
  // 2. 檢查規則
  const rule = findMatchingRule(state);
  if (rule) {
    // 直接執行
    return await executeRule(rule);
  }
  
  // 3. 檢查複雜度
  if (isComplex(state)) {
    // 需要 Claude 幫忙
    return await spawnClaude(state);
  }
  
  // 4. 簡單決策
  return makeSimpleDecision(state);
}

async function spawnClaude(state) {
  const prompt = buildPrompt(state);
  
  // 調用 Claude CLI
  const result = exec({
    command: `claude -p "${prompt}"`,
    pty: true,
    timeout: 60
  });
  
  // 解析建議
  const decision = parseDecision(result);
  
  // 執行
  return await execute(decision);
}
```

## 整合鉤子

### 安裝鉤子

```bash
python3 ~/.openclaw/workspace/scripts/decision_hook.py install
```

### 觸發測試

```bash
python3 ~/.openclaw/workspace/scripts/decision_hook.py trigger "下一步要做什麼"
```

### 監聽模式

```bash
python3 ~/.openclaw/workspace/scripts/decision_hook.py watch
```

### OpenClaw Hook 配置

```javascript
// hooks.json
{
  "hooks": [
    {
      "name": "auto-decide",
      "trigger": {
        "pattern": "(下一步|接下來|what's next|what to do)"
      },
      "action": "autoDecide",
      "priority": 10
    }
  ]
}
```

### 在 OpenClaw 中使用

```javascript
// 當聽到關鍵詞
if (message.includes("下一步") || message.includes("接下來")) {
  // 觸發決策鉤子
  exec("python3 ~/.openclaw/workspace/scripts/decision_hook.py trigger '下一步'");
}
```

## 範例情境

### 情境 1: 完成網站建設

```
User: 網站建好了，下一步？
→ Hook 觸發
→ 評估: 網站完成，沒有下一步指示
→ 決定: 預覽網站 + 問是否部署
→ 回覆: "已完成！要預覽嗎？或直接部署？"
```

### 情境 2: 多個功能完成

```
User: 功能都做完了，然後？
→ Hook 觸發  
→ 評估: 有 3 個已完成功能
→ 決定: 展示統計 + 問要測試哪個
→ 回覆: "3 個功能完成！要測試還是部署？"
```

### 情境 3: 複雜技術選擇

```
User: 接下來要做什麼？
→ Hook 觸發
→ 評估: 多個方向都可走，需要技術評估
→ 動作: spawn Claude 評估
→ 回覆: "我建議先做 X，因為..."
```

## 最佳實踐

1. **不要每次都問** - 自動決定常見路徑
2. **提供選項** - 讓用戶知道你可以做什麼
3. **複雜時求助** - 不確定時調用 Claude
4. **記錄決策** - 存到 memory 供未來參考
5. **持續優化** - 根據反饋改進規則
