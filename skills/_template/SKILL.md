# Skill 模板

**用途**: 建立新 Skill 的標準範本

---

## 模板結構

```yaml
name: skill_name
description: 技能描述
version: 1.0.0
author: OpenClaw

# 參數定義
parameters:
  - name: param_name
    type: string
    required: false
    default: "default_value"
    description: 參數說明

# 輸出格式
output_format: |
  ## 標題
  - 項目1: {value1}
  - 項目2: {value2}

# 錯誤處理
error_handling: |
  - 404: 回報網頁不存在
  - timeout: 回報超時
  - error: 回報錯誤訊息

# 使用範例
examples:
  - "獲取最新趨勢"
  - "分析數據"

# 模型建議
model: sonnet-4.5  # 設計時使用
production_model: gpt-4o  # 生產環境使用
```

---

## 錯誤處理範本

```markdown
## 錯誤處理

### 網路錯誤
- 404: 回報「網頁不存在，請檢查網址」
- timeout: 回報「連線逾時，請稍後重試」

### 資料錯誤
- empty: 回報「無資料」
- invalid: 回報「資料格式錯誤」

### 系統錯誤
- error: 回報「發生錯誤: {error_message}」
```

---

## 輸出格式範本

```markdown
## 輸出格式

### 摘要 ({count} 項目)
| # | 主題 | 來源 | 價值 |
|---|------|------|------|
| 1 | {title} | {source} | {rating} |

### 詳細
{content}
```

---

## 參數化範本

```yaml
parameters:
  - name: topic
    type: string
    required: true
    description: 要搜尋的主題
  
  - name: limit
    type: number
    default: 5
    description: 結果數量上限
  
  - name: source
    type: string
    default: "all"
    description: 來源 (github/hackernews/etc)
```

---

## 設計原則

1. **精準設計** - 避免過多雜訊
2. **明確定義** - 參數/輸出/錯誤
3. **容錯機制** - 處理各種錯誤情況
4. **迭代優化** - 設計→測試→修改

---
