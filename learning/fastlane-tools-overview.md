# Fastlane 自動化工具總整理

**日期**: 2026-02-18
**來源**: Fastlane Docs

---

## 🎯 可應用在系統的工具

### 1. Testing (測試)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **scan** | 自動執行測試 | ✅ 整合 CI/CD |
| **swiftlint** | Swift 程式碼驗證 | ✅ 程式碼品質 |
| **slather** | 程式碼覆蓋率報告 | ✅ 品質監控 |
| **xcov** | 程式碼覆蓋率美觀報告 | ✅ 測試報告 |
| **oclint** | 程式碼分析 | ✅ 錯誤偵測 |
| **sonar** | SonarQube 分析 | ✅ 程式碼品質 |

### 2. Building (建置)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **gym** | 建置 iOS/macOS App | ✅ 自動化建置 |
| **xcodebuild** | 命令列建置 | ✅ 自動化建置 |
| **cocoapods** | 套件管理 | ✅ 依賴管理 |
| **carthage** | 套件管理 | ✅ 依賴管理 |
| **clear_derived_data** | 清除暫存資料 | ✅ 空間清理 |
| **xcodes** | Xcode 版本切換 | ✅ 多版本管理 |

### 3. Screenshots (截圖)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **snapshot** | 自動化截圖 | ✅ UI 測試 |
| **frameit** | 加上手機框架 | ✅ 素材製作 |
| **screengrab** | Android 截圖 | (Android) |

### 4. Project (專案管理)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **increment_build_number** | 自動遞增 build | ✅ 版本控制 |
| **increment_version_number** | 自動遞增版本 | ✅ 版本控制 |
| **get_version_number** | 取得版本號 | ✅ 版本查詢 |
| **set_info_plist_value** | 設定 Info.plist | ✅ 自動化設定 |

### 5. Code Signing (代碼簽署)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **match** | 自動化證書管理 | ✅ 安全證書 |
| **sigh** | Apple 證書管理 | ✅ 證書申請 |
| **cert** | SSL 證書管理 | ✅ 證書處理 |

### 6. Push (推播)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **pem** | SSL 證書管理 | ✅ 推播設定 |
| **pilot** | TestFlight 管理 | ✅ 測試發布 |

### 7. Beta (測試版)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **testfairy** | Beta 測試平台 | ✅ 測試發布 |
| **fabric** | Beta 發布 | ✅ 測試發布 |

### 8. Notifications (通知)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **slack** | Slack 通知 | ✅ 團隊通知 |
| **mailgun** | Email 通知 | ✅ 郵件通知 |

### 9. Source Control (版本控制)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **git_add** | Git 新增檔案 | ✅ 自動化 Git |
| **git_commit** | Git 提交 | ✅ 自動化 commit |
| **push_to_git_remote** | 推送到遠端 | ✅ 自動化 push |

### 10. Deliver (發布)

| 工具 | 功能 | 系統應用 |
|------|------|----------|
| **deliver** | App Store 發布 | ✅ 自動化發布 |
| **upload_to_app_store** | 上傳 App Store | ✅ 發布流程 |

---

## 🔧 系統自動化應用場景

### 可立即應用

| 場景 | 工具 | 說明 |
|------|------|------|
| **自動化測試** | scan, swiftlint | 定期跑測試+驗證碼 |
| **Slack 通知** | slack | 建置/測試完成通知 |
| **版本管理** | increment_build_number | 自動遞增版本 |
| **空間清理** | clear_derived_data | 定時清除暫存 |
| **Git 自動化** | git_commit, push | 自動提交發布 |

### 需要 iOS/macOS 專案

| 場景 | 工具 | 說明 |
|------|------|------|
| **自動化截圖** | snapshot | UI 測試截圖 |
| **自動化建置** | gym, xcodebuild | CI/CD 建置 |
| **App Store 發布** | deliver | 自動化發布 |

---

## 📋 常用指令

```bash
# 列出所有 actions
fastlane actions

# 查看特定 action
fastlane action [action_name]

# 執行 lane
fastlane [lane_name]
```

---

## 💡 建議應用

1. **先測試** - 用 scan + swiftlint
2. **通知** - 整合 slack
3. **自動化** - git_commit + push
4. **清理** - clear_derived_data

---

*記錄時間: 2026-02-18*
