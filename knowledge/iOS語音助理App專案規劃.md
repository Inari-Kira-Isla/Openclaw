# 📱 iOS 語音助理 App 專案規劃

**版本：** v1.0
**日期：** 2026-02-18
**類型：** 專案規劃
**狀態：** 規劃中

---

## 摘要

開發 iOS App 連接 Apple CarPlay，用語音與 OpenClaw 溝通，實現：
- 車載語音控制
- 上網查資料
- 音樂控制
- 建立工作任務

---

## 一、功能需求

| 功能 | 說明 | 優先級 |
|------|------|--------|
| CarPlay 整合 | 連接車載系統 | 高 |
| 語音啟動 | 語音喚醒 OpenClaw | 高 |
| 自然對話 | 語音溝通互動 | 高 |
| 網路搜尋 | 上網查詢資料 | 中 |
| 音樂控制 | 播放/切換歌曲 | 中 |
| 工作建立 | 建立任務事項 | 中 |

---

## 二、技術架構

### 系統架構圖
```
┌─────────────────┐
│   iOS App       │
├─────────────────┤
│  CarPlay       │ ← 車載系統
│  Speech        │ ← 語音識別
│  MediaPlayer   │ ← 音樂控制
└────────┬────────┘
         │
    ┌────▼────┐
    │ OpenClaw│ ← 雲端 AI
    │  API    │
    └─────────┘
```

### 技術堆疊

| 層面 | 技術 |
|------|------|
| 前端 | Swift, SwiftUI |
| 車載 | CarPlay Framework |
| 語音 | Speech Framework, SiriKit |
| 音樂 | MediaPlayer, Apple Music API |
| 後端 | OpenClaw API |

---

## 三、OpenClaw API 需求

### 需要建立的 API

| API | 功能 |
|-----|------|
| `/voice` | 語音輸入處理 |
| `/task` | 建立任務 |
| `/search` | 網路搜尋 |
| `/music` | 音樂控制 |

### 請求格式
```json
{
  "action": "voice",
  "text": "幫我查天氣",
  "user_id": "xxx"
}
```

---

## 四、實作階段

### Phase 1: 基礎建設
- [ ] 建立 OpenClaw API 接口
- [ ] iOS 專案初始化
- [ ] 基本語音識別

### Phase 2: CarPlay 整合
- [ ] CarPlay Framework 設定
- [ ] 車載介面開發
- [ ] 語音指令映射

### Phase 3: 功能開發
- [ ] 對話系統
- [ ] 網路搜尋
- [ ] 音樂控制

### Phase 4: 優化
- [ ] 效能優化
- [ ] 測試發布

---

## 五、對應現有系統

| 系統 | 可用功能 |
|------|----------|
| lifeos-agent | 日程管理、提醒 |
| knowledge-agent | 知識搜尋 |
| mcp-builder | API 建構 |
| analytics-agent | 使用分析 |

---

## 六、系統建議

### ✅ 可直接應用

- [ ] 建立 OpenClaw API 接口 (mcp-builder)
- [ ] 設計語音指令格式

### 🔄 需要開發

- [ ] iOS App 開發
- [ ] CarPlay Framework 整合
- [ ] Speech Framework 整合

---

## 七、參考資源

**Apple 開發者：**
- CarPlay Framework
- Speech Framework
- SiriKit

**相關專案：**
- OpenClaw API
- Apple Music API

---

*更新：2026-02-18*
*版本：v1.0*
