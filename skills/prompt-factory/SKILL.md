---
name: prompt-factory
description: |
  自動將業務上下文組裝成精確的 coding prompt。當需要將記憶、知識庫、客戶資料轉化為給 coding agent 的任務描述時使用。
  適用場景：(1) 用戶需求轉化為技術任務 (2) 注入歷史上下文到新任務 (3) 跨專案知識傳遞 (4) 確保 coding agent 了解業務背景
metadata:
  {
    "openclaw": { "emoji": "🏭", "requires": { "anyTools": ["memory_search", "read", "exec"] } },
  }
---

# Prompt Factory

自動將業務上下文組裝成精確的 coding prompt。

## 使用方式

```
當你收到一個 coding 任務：
1. 分析任務需要的上下文
2. memory_search 查詢相關歷史
3. 組裝 prompt 模板
4. 返回完整 prompt
```

## Prompt 模板

```markdown
## 任務
{TASK}

## 業務上下文
{CONTEXT}

## 技術約束
{CONSTRAINTS}

## 參考範例
{EXAMPLES}

## 輸出要求
{OUTPUT_REQUIREMENTS}
```

## 上下文來源

### 1. 記憶系統
```javascript
memory_search({ 
  query: "相關關鍵字" 
})
// 提取相關決策、歷史記錄
```

### 2. 知識庫
```javascript
// 查詢本地資料庫（SQLite）或向量庫
// 獲取相關技術文檔
```

### 3. 用戶偏好
```javascript
// 從 USER.md 獲取技術偏好
// 語言: TypeScript > JavaScript
// 框架: React, Node.js
```

## 組裝流程

### Step 1: 分析任務

判斷任務需要哪種上下文：

| 任務類型 | 需要的上下文 |
|----------|-------------|
| 新功能開發 | 產品需求、相關模組 |
| Bug修復 | 問題描述、類似問題 |
| 重構 | 現有架構、依賴關係 |
| 優化效能 | 瓶頸分析、過往優化 |

### Step 2: 查詢上下文

```javascript
// 主要查詢
memory_search({ query: "任務關鍵字" })

// 補充查詢
memory_search({ query: "相關技術棧" })
memory_search({ query: "類似決策" })
```

### Step 3: 模板組裝

```
Context = 記憶摘要 + 技術約束 + 業務目標

Prompt = 任務描述 + Context + 輸出格式
```

## 輸出格式範例

### 功能開發

```markdown
## 任務
開發 {功能名稱}

## 上下文
{從記憶提取的相關背景}

## 技術棧
- 語言: {語言偏好}
- 框架: {框架偏好}
- 相依: {現有依賴}

## 要求
- 符合現有程式碼風格
- 包含單元測試
- 更新相關文檔
```

### Bug修復

```markdown
## 任務
修復 {問題描述}

## 上下文
{問題發生情境}

## 類似問題
{歷史上的修復記錄}

## 要求
- 找出根本原因
- 提供測試用例防止回歸
```

## 組合範例

### 輸入
```
User: "幫我加一個使用者登入功能"
```

### 處理流程
```javascript
// 1. 查詢相關上下文
memory_search({ query: "使用者認證 登入 auth" })
memory_search({ query: "OpenClaw 架構" })

// 2. 組裝 prompt
```

### 輸出

```markdown
## 任務
新增使用者登入功能

## 業務上下文
- 這是 AI 治理系統的一部分
- 需要與現有權限系統整合
- 用戶透過 Telegram 機器人互動

## 技術約束
- 語言: TypeScript
- 現有認證: JWT
- 資料庫: SQLite
- 相關模組: auth/, permissions/

## 要求
1. 實現 email/password 登入
2. 支援 JWT token 發行
3. 與現有 permissions 系統整合
4. 包含單元測試
5. 更新 API 文檔
```

## 最佳實踐

1. **精確而非冗長** - 只包含相關上下文
2. **明確的輸出格式** - 讓 coding agent 知道期望什麼
3. **技術約束清晰** - 語言、框架、規範
4. **包含參考** - 相似問題的解決方案
5. **保持迭代** - 根據反饋優化模板
