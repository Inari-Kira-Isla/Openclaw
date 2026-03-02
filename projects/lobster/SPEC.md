# Lobster System - 錯誤與成功學習系統

## 概述

**名稱**: Lobster (龍蝦)
**目的**: 記錄犯過的錯 + 做得好的工作流程，自動偵測並預防重複犯錯
**願景**: 龍蝦每次蛻殼都會變強 🦞

---

## 功能定義

### 1. 偵測模組 (Detector)

| 來源 | 偵測方式 | 嚴重程度 |
|------|----------|----------|
| Cron Jobs | 監控 error log | 高/中/低 |
| API 調用 | 攔截 4xx/5xx 響應 | 高 |
| OpenClaw Sessions | 分析失敗對話 | 中 |
| 手動匯報 | User 輸入 | 自定義 |

### 2. 記錄模組 (Recorder)

**Notion 資料庫結構**:
```
- 類型: 錯誤 / 成功
- 標籤: [系統, 自動化, 決策, 代碼, 其他]
- 描述: What happened?
- 原因: Why it happened?
- 解決方案: How to fix?
- 預防措施: How to prevent?
- 發生時間: Date
- 發生次數: Count
- 狀態: Open / Resolved / Monitoring
```

### 3. 回顧模組 (Review Engine)

- **每日回顧**: 早安簡報包含今日提醒
- **行動前檢查**: 執行關鍵操作前檢索相關歷史錯誤
- **每週總結**: 統計錯誤趨勢

### 4. 成功模組 (Success Recorder)

- 記錄做得好的流程
- 萃取最佳實踐 (Best Practices)
- 可複用的工作流模板

---

## 技術架構

```
┌─────────────────────────────────────────┐
│           Lobster System               │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │Detector │→→│ Recorder│→→│ Notion  │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│       ↓                                  │
│  ┌─────────┐  ┌─────────┐              │
│  │ Review  │←←│ Success │              │
│  │ Engine  │  │ Module  │              │
│  └─────────┘  └─────────┘              │
└─────────────────────────────────────────┘
```

**技術棧**:
- Language: TypeScript
- Runtime: Node.js
- Storage: Notion API
- Trigger: OpenClaw Cron / Heartbeat
- Integration: OpenClaw Skills

---

## API 設計

### 記錄錯誤
```typescript
recordError({
  source: 'cron' | 'api' | 'session' | 'manual',
  severity: 'high' | 'medium' | 'low',
  title: string,
  description: string,
  cause?: string,
  solution?: string,
  tags: string[]
})
```

### 記錄成功
```typescript
recordSuccess({
  title: string,
  workflow: string,
  tags: string[],
  lessons: string[]
})
```

### 檢索預防
```typescript
checkBeforeAction({
  action: string,
  context: string
}): Promise<Prevention[]>
```

---

## 驗收標準

- [ ] 能自動偵測 Cron error 並記錄
- [ ] 能手動輸入錯誤/成功記錄
- [ ] Notion 資料庫正確建立
- [ ] 行動前檢索功能正常
- [ ] 每日回顧簡報包含錯誤趨勢

---

## 待辦

- [ ] 建立 Notion 資料庫 template
- [ ] 實作 Detector 模組
- [ ] 實作 Recorder 模組
- [ ] 實作 Review Engine
- [ ] 實作 Success Module
- [ ] 整合 OpenClaw Cron

---

*Created: 2026-02-28*
