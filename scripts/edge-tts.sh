#!/bin/bash
# Edge TTS Script - 免費文字轉語音
# 使用 Microsoft Edge 的免費 TTS 服務

VENV="/Users/ki/.openclaw/workspace/venv"

tts() {
    local TEXT="$1"
    local OUTPUT="${2:-output.mp3}"
    
    if [ -z "$TEXT" ]; then
        echo "用法: $0 <文字> [輸出檔案]"
        echo "範例: $0 '你好' hello.mp3"
        return
    fi
    
    # 使用 edge-tts
    source "$VENV/bin/activate"
    
    # 列出可用聲音
    if [ "$TEXT" = "--voices" ]; then
        edge-tts --list-voices | grep -i zh
        return
    fi
    
    # 轉換
    echo "🔊 轉換中: $TEXT"
    edge-tts -t "$TEXT" -w "$OUTPUT" 2>/dev/null
    
    if [ -f "$OUTPUT" ]; then
        echo "✅ 完成: $OUTPUT"
        # 播放
        afplay "$OUTPUT" 2>/dev/null &
    else
        echo "❌ 轉換失敗"
    fi
}

# 主程式
case "$1" in
    --voices)
        source "$VENV/bin/activate"
        edge-tts --list-voices | grep -i zh
        ;;
    -t|--text)
        tts "$2" "$3"
        ;;
    *)
        tts "$1" "$2"
        ;;
esac
