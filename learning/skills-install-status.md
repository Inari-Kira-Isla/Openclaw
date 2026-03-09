# Skills 安裝狀態

**日期**: 2026-02-18

---

## 安裝結果

| Skill | 狀態 | 原因 |
|-------|------|------|
| **nano-pdf** | ❌ 失敗 | 需 Python 環境 + pip |
| **summarize** | ❌ 失敗 | 僅支援 Apple Silicon (arm64)，iMac 是 Intel |
| **model-usage** | ❓ 未測試 | 需要 codexbar CLI |
| **sherpa-onnx-tts** | ❓ 未測試 | 需要下載 runtime + model (~200MB) |

---

## 環境資訊

- **架構**: x86_64 (Intel)
- **Python**: 3.14.3 (系統)
- **Homebrew**: ✅ 已安裝

---

## 替代方案

### summarize
可用網頁版替代：
- https://summarize.sh

### nano-pdf
可使用線上工具替代：
- https://edit.typedpdf.com/

### sherpa-onnx-tts
可使用其他 TTS：
- OpenClaw 內建 TTS
- macOS say 命令

---

## 建議

1. **summarize** - 使用網頁版或等待支援
2. **nano-pdf** - 使用線上 PDF 編輯器
3. **model-usage** - 可安裝 codexbar 測試
4. **sherpa-onnx-tts** - 可手動下載測試

---

*記錄時間: 2026-02-18*
