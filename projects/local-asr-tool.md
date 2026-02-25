# 本地語音辨識工具 - 離線 + 會議字幕

**建立日期**: 2026-02-20
**目標**: 離線語音辨識 + 會議字幕生成

---

## 📋 需求

| # | 需求 | 說明 |
|---|------|------|
| 1 | 離線語音辨識 | 不用網路，電腦可直接執行 |
| 2 | 會議字幕生成 | 輸入音訊 → 輸出 SRT 字幕 |

---

## 🛠️ 技術方案

### Whisper (本地)

| 項目 | 內容 |
|------|------|
| 模型 | faster-whisper |
| 輸出 | SRT, VTT, TXT |
| 語言 | 中文/英文/日文 |
| 速度 | CPU ~7分/小時 |

---

## 📝 實施計劃

### Phase 1: 環境搭建
- [ ] 安裝 faster-whisper
- [ ] 下載模型 (medium)
- [ ] 測試基本功能

### Phase 2: 會議字幕
- [ ] 建立轉換腳本
- [ ] 輸出 SRT 格式
- [ ] 時間軸對齊

### Phase 3: 優化
- [ ] 參數優化
- [ ] 批次處理
- [ ] 錯誤處理

---

## 🎯 使用方式

### 單檔處理
```bash
# 轉換音訊為字幕
./transcribe.sh input.wav output.srt
```

### 會議資料夾
```bash
# 批次處理
./transcribe_folder.sh ./meetings/
```

---

## 📦 輸出格式

### SRT 範例
```
1
00:00:00,000 --> 00:00:05,000
大家好，今天我們來討論...

2
00:00:05,000 --> 00:00:10,000
第一個議題是...
```

---

## 🔧 腳本規劃

### transcribe.sh
```bash
#!/bin/bash
# 會議字幕生成腳本

INPUT=$1
OUTPUT=$2

# 使用 faster-whisper
python -m faster_whisper \
  --model medium \
  --language zh \
  --output_format srt \
  -o "$OUTPUT" "$INPUT"
```

---

## ❓ 請提供測試素材

1. 有會議錄音檔嗎？
2. 或先用測試檔案？

---
