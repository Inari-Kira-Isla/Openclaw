# 本地模型優化方案

**日期**: 2026-02-19

---

## 問題

本地模型逾時問題：
- 載入時間過長 (30-60秒)
- 8GB RAM 不足
- 模型切換頻繁

---

## 解決方案

### 1. 模型選擇優化

| 策略 | 模型 | 記憶體 |
|------|------|--------|
| 快速 | deepseek-coder:1.3b | 776MB |
| 平衡 | mistral | 4.4GB |
| 質量 | llama3 | 4.7GB |

### 2. 預熱機制

```bash
# 開機自動預熱
ollama serve &
```

### 3. 品質閾值

```
IF 回應時間 > 30秒
    THEN 切換到 MiniMax
```

### 4. 混合架構

```
日常任務 → 本地模型
複雜任務 → MiniMax
```

---

## 設定開機自動啟動

```bash
# macOS LaunchAgent
launchctl load ~/Library/LaunchAgents/com.ollama.ollama.plist
```

---

## 監控腳本

```bash
# 檢查狀態
curl http://localhost:11434/api/tags
```

---
