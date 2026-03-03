# GitHub 監控報告 - 2026-03-03

## 最新 PRs

| # | 標題 | 狀態 | 相關性 |
|---|------|------|--------|
| 32029 | fix(acp): enforce sessions_spawn-only thread creation | OPEN | ✅ ACP 系統相關 |
| 32028 | feat: add Kimi ACP agent adapter | OPEN | ⚪ 其他 Agent |
| 32026 | fix(signal): drop bare emoji reaction | OPEN | ⚪ Signal 整合 |
| 32024 | fix(feishu): improve card text extraction | OPEN | ⚪ 飛書整合 |
| 32022 | fix(launchd): set restrictive umask | OPEN | ⚪ macOS LaunchD |

## 最新 Issues

| # | 標題 | 狀態 | 相關性 |
|---|------|------|--------|
| 32030 | BlueBubbles webhook 405 error | OPEN | ⚪ |
| **32025** | **[Bug] openclaw update fails with node-llama-cpp cmake (macOS)** | **OPEN** | **🔴 高** |
| 32023 | fix(feishu): bot receives '[Interactive Card]' | OPEN | ⚪ |
| 32021 | [Feature] Decouple browser config for Cron | OPEN | 🟡 中 |
| 32019 | Plugin diffs v0.1.1 install fails | OPEN | ⚪ |

## 重點分析

### 🔴 高相關：#32025 node-llama-cpp cmake 安裝失敗

**問題**：macOS 上 `openclaw update` 因 node-llama-cpp 需要 cmake 而失敗

**解決方案**：
```bash
brew install cmake
openclaw update
```

**影響**：若 Joe 需要更新 OpenClaw，需先安裝 cmake

### 🟡 中相關：#32021 動態瀏覽器配置

**功能**：為 Cron jobs 動態分配瀏覽器 profile

**潛在應用**：我們的多組態鈎子可能受益

### ✅ 相關：#32029 ACP sessions_spawn

**變更**：強化 ACP harness 的 thread creation 規範

**影響**：我們的 acp-router skill 需要確保符合新規範

## 行動建議

1. **立即**：若要更新 OpenClaw，先 `brew install cmake`
2. **關注**：#32021 瀏覽器配置優化
3. **檢查**：acp-router skill 是否符合 #32029 新規範

---
*監控時間：2026-03-03 02:20*
