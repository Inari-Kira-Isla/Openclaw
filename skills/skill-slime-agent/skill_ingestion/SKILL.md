---
name: skill_ingestion
description: 技能攝入與學習。當需要學習外部技能並整合到系統時觸發，包括：技能發現、分析評估、轉換適配、整合測試。
---

# Skill Ingestion

## 攝入流程

```
來源發現 → 技能分析 → 評估價值 → 轉換處理 → 整合測試 → 上線啟用
```

## 來源類型

### 1. ClawHub
```bash
clawhub search <關鍵詞>
clawhub install <skill-name>
```

### 2. GitHub
- 搜尋 MCP Server 專案
- 評估程式碼品質
- 提取技能定義

### 3. 自定義
- 用戶自行開發
- 從參考文檔生成

## 評估維度

### 功能評估
- 是否符合需求
- 功能完整性
- 與現有技能重疊

### 質量評估
- 程式碼品質
- 維護狀態
- 社群支援

### 風險評估
- 安全漏洞
- 依賴風險
- 相容性問題

## 整合處理

### 轉換適配
- 格式轉換為標準結構
- 路徑調整
- 依賴修復

### 配置更新
- 添加到 agents.yml
- 設定權限
- 配置參數

## 測試驗證
```json
{
  "test_status": "passed",
  "functionality": "ok",
  "integration": "ok",
  "security": "ok"
}
```
