# Fastlane Snapshot 自動化截圖整合

**日期**: 2026-02-18
**來源**: Joe 分享

---

## 🎯 目標

將 Fastlane Snapshot 整合到 OpenClaw 自動化流程

---

## 📸 Fastlane Snapshot

### 功能

| 特性 | 說明 |
|------|------|
| 自動化截圖 | 多語言、多設備同時截圖 |
| 後台執行 | 電腦自動截圖，你可以做其他事 |
| 網頁生成 | 產生 HTML 總覽頁面 |
| App Store 上傳 | 可直接整合 deliver 上傳 |

### 數量計算

```
20 語言 × 6 設備 × 5 截圖 = 600 張
```

---

## 🛠️ 整合方式

### 1. 安裝 Fastlane

```bash
sudo gem install fastlane
```

### 2. 初始化

```bash
fastlane snapshot init
```

### 3. 設定

在 `Snapfile` 設定設備和語言：

```ruby
devices([
  "iPhone 14 Pro",
  "iPhone 14 Pro Max",
  "iPad Pro (12.9-inch) (第 2 代)"
])

languages([
  "zh-Hant",  # 繁體中文
  "en-US"      # 英文
])
```

### 4. 執行

```bash
fastlane snapshot
```

---

## 🔄 OpenClaw 整合流程

```
1. 啟動 iOS Simulator
   ↓
2. 執行 fastlane snapshot
   ↓
3. 截圖產生完成
   ↓
4. 上傳到指定位置
   ↓
5. 通知 (Slack/Telegram)
```

---

## 📦 n8n Workflow

```
iOS Simulator 啟動
    ↓
Fastlane Snapshot 執行
    ↓
截圖產出資料夾
    ↓
上傳雲端 (Google Drive/S3)
    ↓
通知團隊
```

---

## 💡 應用場景

| 場景 | 說明 |
|------|------|
| App Store 更新 | 自動產生新截圖 |
| 多語言測試 | 同時測試所有語言 |
| QA 驗證 | 產生 HTML 給 QA 團隊 |
| 行銷素材 | 給行銷團隊使用 |

---

## ⚠️ 前置需求

1. Xcode 安裝
2. UI Test Target 建立
3. Simulator 可用

---

## 📝 下一步

1. 在專案建立 Snapfile
2. 設定語言和設備
3. 測試執行

---

*記錄時間: 2026-02-18*
