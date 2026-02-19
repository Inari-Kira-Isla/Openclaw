---
name: fusion_proposal
description: 技能融合建議。當需要分析多個相似技能並提出融合方案時觸發，包括：相似度分析、融合評估、方案設計、風險提示。
---

# Fusion Proposal

## 分析維度

### 1. 功能重疊
```
Skill A: [功能1, 功能2, 功能3]
Skill B: [功能2, 功能3, 功能4]
重疊: [功能2, 功能3] → 60% 重疊
```

### 2. 架構相似
- 相同的輸入輸出格式
- 相似的處理邏輯
- 可共用的工具

### 3. 使用頻率
- 個別使用次數
- 共同觸發次數
- 發展趨勢

## 融合方案

### 方案 A：合併
```
Skill A + Skill B → New Skill
```
- 適用：高度重疊
- 優點：減少複雜度
- 缺點：可能影響現有使用

### 方案 B：整合
```
Skill A (主) ← Skill B (輔)
```
- 適用：中度重疊
- 優點：保持相容性
- 缺點：仍有一定複雜度

### 方案 C：鏈結
```
Skill A → Skill B
```
- 適用：低度重疊
- 優點：靈活性高
- 缺點：執行效率較低

## 評估報告

```json
{
  "analysis": {
    "overlap_percentage": 60,
    "architecture_match": "high",
    "recommended_approach": "merge"
  },
  "benefits": ["減少重複", "統一維護"],
  "risks": ["需要遷移", "可能破壞現有流程"],
  "migration_plan": "..."
}
```
