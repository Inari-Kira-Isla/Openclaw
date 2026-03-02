---
name: seo-aeo-monitor
description: |
  SEO/AEO 監控鉤子。當需要監控內容質量、持續優化時觸發。
  功能：(1) 定期審計內容質量 (2) 自動修復 SEO 問題 (3) 追蹤優化效果 (4) 學習改進。
  適用場景：(1) 每日質量檢查 (2) 新內容審計 (3) 持續優化
metadata:
  {
    "openclaw": { "emoji": "📊", "requires": { "anyTools": ["exec", "read", "write", "message"] } },
  }
---

# SEO/AEO Monitor

內容質量監控與持續優化系統

## 審計流程

```
┌─────────────────────────────────────────────────────────────┐
│                   📊 SEO/AEO 監控                            │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  1. 內容審計                                               │
│     - 檢查 frontmatter                                     │
│     - 檢查結構                                             │
│     - 檢查關鍵詞                                           │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  2. 問題診斷                                               │
│     - 缺少字段                                             │
│     - 結構問題                                             │
│     - AEO 問題                                             │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 自動修復                                               │
│     - 添加描述                                             │
│     - 添加關鍵詞                                           │
│     - 修復結構                                             │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  4. 學習優化                                               │
│     - 記錄問題                                             │
│     - 分析模式                                             │
│     - 持續改進                                             │
└─────────────────────────────────────────────────────────────┘
```

## 使用方式

### 審計

```bash
# 審計所有內容
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py audit

# 修復問題
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py fix

# 生成報告
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py report
```

### 自動監控

```bash
# 加入每日監控
0 8 * * * python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py audit
```

## 審計標準

### 必需字段

| 字段 | 說明 |
|------|------|
| title | 標題 |
| type | 類型 |
| date | 日期 |
| tags | 標籤 |

### 推薦字段

| 字段 | 說明 |
|------|------|
| description | 描述 |
| keywords | 關鍵詞 |
| author | 作者 |
| category | 分類 |

### AEO 字段

| 字段 | 說明 |
|------|------|
| use_case | 使用場景 |
| difficulty | 難度 |
| related | 相關文章 |

## 持續學習

### 記錄問題

```python
{
  "issues": [
    {"type": "missing_field", "field": "description", "count": 100},
    {"type": "structure", "multiple_h1": 17}
  ]
}
```

### 分析模式

- 哪些字段最常缺少
- 哪些類型問題最多
- 哪些結構需要優化

### 自動改進

- 修復時添加智能建議
- 根據問題類型調整修復策略
- 持續追蹤質量趨勢

## 監控指標

| 指標 | 目標 | 當前 |
|------|------|------|
| 平均分數 | > 85 | 87.4 |
| 優秀文章 | 100% | 100% |
| 問題修復 | 100% | ✅ |

## 自動化

```bash
# 每日自動審計
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py audit

# 發現問題自動修復
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py fix

# 生成趨勢報告
python3 ~/.openclaw/workspace/aeo-site/scripts/seo_audit.py report
```

## 整合閉環

```python
# 每日質量監控流程

# 1. 審計
audit()

# 2. 修復
fix()

# 3. 記錄
record_metrics()

# 4. 學習
learn()

# 5. 優化
optimize()
```

系統會持續監控質量，自動修復問題，並從中學習改進！
