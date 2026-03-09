#!/bin/bash
# OpenClaw CarPlay 語音腳本
# 功能：任務完成通知、即時回覆、自定義語音

VOICE_FILE="/tmp/carplay_voice.cfg"
DEFAULT_VOICE="Meijia"

# 讀取聲音設定
get_voice() {
    if [ -f "$VOICE_FILE" ]; then
        cat "$VOICE_FILE"
    else
        echo "$DEFAULT_VOICE"
    fi
}

# 設定聲音
set_voice() {
    echo "$1" > "$VOICE_FILE"
    echo "✅ 聲音設定為: $1"
}

# 顯示可用聲音
list_voices() {
    say -v "?" 2>/dev/null | grep -i "zh" | head -15
}

# 任務完成通知
notify() {
    local voice=$(get_voice)
    say -v "$voice" "任務完成，$1"
}

# 即時回覆
reply() {
    local voice=$(get_voice)
    say -v "$voice" "$1"
}

# 錯誤回覆
error() {
    local voice=$(get_voice)
    say -v "$voice" "發生錯誤，$1"
}

# 主程式
case "$1" in
    notify)
        notify "$2"
        ;;
    reply)
        reply "$2"
        ;;
    error)
        error "$2"
        ;;
    set-voice)
        set_voice "$2"
        ;;
    get-voice)
        get_voice
        ;;
    voices)
        list_voices
        ;;
    *)
        echo "📖 OpenClaw CarPlay 語音指令"
        echo ""
        echo "用法:"
        echo "  carplay.sh notify <任務名稱>     # 任務完成通知"
        echo "  carplay.sh reply <訊息>         # 即時回覆"
        echo "  carplay.sh error <錯誤訊息>      # 錯誤回覆"
        echo "  carplay.sh set-voice <聲音>      # 設定聲音"
        echo "  carplay.sh get-voice            # 查詢目前聲音"
        echo "  carplay.sh voices               # 顯示可用聲音"
        echo ""
        echo "範例:"
        echo "  carplay.sh notify '訓練完成'"
        echo "  carplay.sh reply '天氣晴朗'"
        echo "  carplay.sh set-voice Meijia"
        ;;
esac
