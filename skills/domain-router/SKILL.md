# Domain Router Skill v2

## 功能
根據任務領域自動選擇合適的 Agent，並處理模型切換。

## 領域識別

### 自動識別邏輯
1. 接收任務描述
2. 提取關鍵詞
3. 匹配領域標籤
4. 選擇最佳 Agent

### 領域關鍵詞庫

| 領域 | 關鍵詞 | Agent | 模型 |
|------|--------|-------|------|
| 開發 coding | code, 開發, 程式, debug, 寫 code | code-master | MiniMax |
| 寫作 writing | 文案, 寫作, 文章, 內容, copy | writing-master | MiniMax |
| 設計 design | 設計, UI, UX, 圖形, 介面 | design-master | MiniMax |
| 分析 analysis | 分析, 數據, 統計, 圖表 | analytics-agent | MiniMax |
| 知識 knowledge | 知識, 學習, 理解, 概念 | knowledge-agent | MiniMax |
| 記憶 memory | 記憶, 向量, RAG, 檢索 | memory-agent | MiniMax |
| 治理 governance | 治理, 決策, 政策, 規則 | governance-agent | Claude Sonnet |
| 審查 review | 審查, 裁決, 評估, 判断 | neicheok | Claude Sonnet |
| 質疑 evolution | 質疑, 挑戰, 改進, 優化 | evolution | MiniMax |
| 執行 execution | 執行, 任務, 行動, 完成 | team | MiniMax |
| 學習 learning | 學習, 優化, 成長, 訓練 | slime | MiniMax |
| 創意 creative | 創意, 策略, 策劃, 靈感 | muse-core | MiniMax |

## 路由規則

### 優先級
1. 精確匹配 > 模糊匹配
2. 有上下文 > 無上下文
3. 主模型 > 備用模型

### 上下文傳遞
- 切換時保留最近 5 輪對話
- 傳遞任務背景
- 記錄切換歷史

## Fallback 機制

```
主模型失敗 → 切換備用模型 → 重試 → 失敗則警報
```

| 狀況 | 行動 |
|------|------|
| 主模型超時 | 切換備用 |
| 主模型 rate limit | 排隊等待 30s 後重試 |
| 所有模型失敗 | 記錄錯誤 + 發送警報 |

## 使用方式

直接說出任務，系統會：
1. 識別領域
2. 選擇 Agent
3. 切換並執行
4. 回報結果

---
*更新：2026-03-01 v2*
