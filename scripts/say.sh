#!/bin/bash
# Gemini TTS 語音腳本
# 用於 Antigravity IDE 中讓 Gemini 說話

# 檢查是否有輸入參數
if [ $# -eq 0 ]; then
    echo "Usage: $0 <text_to_say>"
    exit 1
fi

# 合併所有參數為單一字串
TEXT="$*"

# 臨時檔案
TMP_FILE="/tmp/google_tts_$$.mp3"

# 直接使用 Mac 內建聲音 (更穩定)
say -v Mei-jia "$TEXT"
