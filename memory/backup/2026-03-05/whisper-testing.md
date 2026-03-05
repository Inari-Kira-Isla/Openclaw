# Whisper 測試計劃

**日期**: 2026-02-20
**狀態**: 已安裝，待測試

---

## 📦 安裝狀態

| 項目 | 狀態 |
|------|------|
| whisper CLI | ✅ 已安裝 |
| 模型 | ⏳ 首次使用時下載 |

---

## 🧪 測試方式

### 方式 1: 命令列

```bash
# 基本轉換
whisper 錄音.wav --model medium --language zh

# 指定輸出
whisper 錄音.wav --model medium --language zh --output_format srt
```

### 方式 2: 腳本

```bash
~/OpenClawASR/scripts/whisper.sh 錄音.wav
```

---

## 📋 需要素材

| 類型 | 說明 |
|------|------|
| 會議錄音 | MP3/WAV/M4A |
| 訪談 | 單人/多人 |
| 演講 | 長時間音訊 |

---

## 🎯 測試目標

1. [ ] 測試基本轉換
2. [ ] 測試輸出 SRT 字幕
3. [ ] 測試準確度
4. [ ] 測試速度

---

## 📝 待辦

- [ ] 提供測試素材
- [ ] 執行第一次測試
- [ ] 記錄結果
- [ ] 優化腳本

---
