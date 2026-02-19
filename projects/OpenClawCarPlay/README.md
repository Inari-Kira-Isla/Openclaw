# OpenClaw CarPlay iOS App

iOS 語音助理 App，連接 Apple CarPlay，用語音與 OpenClaw 溝通。

## 功能

- 🔊 語音控制 - 語音喚醒 OpenClaw
- 🚗 CarPlay 整合 - 車載系統無縫連接
- 🎵 音樂控制 - 播放/切換歌曲
- 📋 任務管理 - 建立/查看任務
- 📅 日程查詢 - 查詢今日行程
- 🔍 網路搜尋 - 上網查詢資料

## 專案結構

```
OpenClawCarPlay/
├── Sources/
│   ├── App/
│   │   └── OpenClawCarPlayApp.swift       # App Entry Point
│   ├── Views/
│   │   └── ContentView.swift               # Main UI
│   ├── Services/
│   │   ├── Speech/
│   │   │   └── VoiceManager.swift          # 語音識別
│   │   ├── Music/
│   │   │   └── MusicManager.swift          # 音樂控制
│   │   └── API/
│   │       └── OpenClawService.swift       # OpenClaw API
│   └── CarPlay/
│       └── CarPlayManager.swift             # CarPlay 整合
├── API/
│   └── openclaw-api-server.js               # OpenClaw API Server
└── project.yml                               # 專案配置
```

## 安裝

### 1. 安裝 dependencies

```bash
cd OpenClawCarPlay
```

### 2. 設定 Xcode

```bash
# 使用 XcodeGen
xcodegen generate
```

### 3. 開啟專案

```bash
open OpenClawCarPlay.xcodeproj
```

### 4. 設定 Capabilities

在 Xcode 中開啟：
- CarPlay Audio
- Speech Recognition
- Music Library Access

### 5. 安裝 OpenClaw API Server

```bash
cd API
npm install express cors
node openclaw-api-server.js
```

## 使用

### 權限

首次使用需要授權：
- 麥克風權限
- 語音識別權限
- 音樂庫權限

### 語音指令

| 指令 | 功能 |
|------|------|
| "幫我查天氣" | 網路搜尋 |
| "播放音樂" | 播放音樂 |
| "新增任務" | 建立任務 |
| "今天行程" | 查詢日程 |

## OpenClaw API

### Endpoints

| Method | Endpoint | 功能 |
|--------|----------|------|
| GET | `/api/ping` | 檢查連接 |
| POST | `/api/voice` | 語音訊息 |
| POST | `/api/search` | 網路搜尋 |
| POST | `/api/music` | 音樂控制 |
| POST | `/api/task` | 任務管理 |
| POST | `/api/schedule` | 日程查詢 |

### Request Format

```json
{
  "action": "voice",
  "text": "幫我查天氣",
  "userID": "carplay-ios"
}
```

### Response Format

```json
{
  "success": true,
  "message": "今天天氣晴朗"
}
```

## 技術堆疊

- Swift 5.9
- SwiftUI
- CarPlay Framework
- Speech Framework
- MediaPlayer Framework
- Express.js (API Server)

## License

MIT
