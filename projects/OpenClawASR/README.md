# OpenClaw ASR - 本地語音辨識工具

**建立日期**: 2026-02-20

---

## 📦 檔案結構

```
~/OpenClawASR/
├── scripts/
│   ├── transcribe.sh    # 轉換腳本
│   └── batch.sh         # 批次處理
├── models/              # 模型存放
├── output/              # 輸出位置
├── venv/               # Python 環境
└── README.md           # 說明
```

---

## 🎮 使用方式

### 1. 單檔轉換

```bash
cd ~/OpenClawASR
./scripts/transcribe.sh 會議錄音.wav 會議.srt
```

### 2. 批次處理

```bash
./scripts/batch.sh ./meetings/
```

---

## 📝 支援格式

| 輸入 | 輸出 |
|------|------|
| WAV | SRT |
| MP3 | VTT |
| M4A | TXT |
| MP4 | JSON |

---

## ⚙️ 參數說明

| 參數 | 說明 |
|------|------|
| --model | 模型 (tiny/base/small/medium/large) |
| --language | 語言 (zh/en/ja) |
| --output_format | 輸出格式 (srt/vtt/txt/json) |

---

## 🔧 模型選擇

| 模型 | 大小 | 速度 | 品質 |
|------|------|------|------|
| tiny | 39MB | 最快 | 一般 |
| base | 74MB | 快 | 一般 |
| small | 244MB | 中 | 較好 |
| medium | 769MB | 慢 | 好 |
| large | 1550MB | 最慢 | 最好 |

**建議**: medium (769MB)

---

## 📥 首次使用

1. 下載模型 (自動)
2. 執行轉換
3. 取得字幕

---

## ❓ 常見問題

### Q: 需要網路嗎？
A: 首次下載模型需要網路，之後離線可用。

### Q: 需要 GPU 嗎？
A: 不需要，CPU 即可執行。

### Q: 速度如何？
A: medium 模型約 7 分鐘/小時音訊。

---

## 📞 支援

有問題請告訴我！
