#!/bin/bash
# OpenClaw CarPlay 語音通知腳本
# 用於任務完成、即時回覆、自定義語音

# 配置
VOICE_DIR="/Users/ki/.openclaw/workspace/scripts"
VOICE_FILE="$VOICE_DIR/voices.sh"

# 可用的聲音列表
show_voices() {
    say -v "?" | grep -i zh | head -10
}

# 設定聲音
set_voice() {
    local voice="$1"
    echo "VOICE=$voice" > "$VOICE_FILE"
    echo "✅ 聲音已設定為: $voice"
}

# 讀取目前聲音
get_voice() {
    if [ -f "$VOICE_FILE" ]; then
        source "$VOICE_FILE"
        echo "${VOICE:-Meijia}"
    else
        echo "Meijia"
    fi
}

# 任務完成通知
notify_task_complete() {
    local task_name="$1"
    local voice=$(get_voice)
    say -v "$voice" "任務完成，$task_name"
}

# 即時語音回覆
voice_reply() {
    local message="$1"
    local voice=$(get_voice)
    say -v "$voice" "$message"
}

# 根據類型回覆
reply() {
    local type="$1"
    local content="$2"
    local voice=$(get_voice)
    
    case "$type" in
        "task")
            say -v "$voice" "任務完成，$content"
            ;;
        "info")
            say -v "$voice" "$content"
            ;;
        "error")
            say -v "$voice" "發生錯誤，$content"
            ;;
        *)
            say -v "$voice" "$content"
            ;;
    esac
}

# 主程式
case "$1" in
    "notify")
        notify_task_complete "$2"
        ;;
    "reply")
        voice_reply "$2"
        ;;
    "set-voice")
        set_voice "$2"
        ;;
    "get-voice")
        get_voice
        ;;
    "voices")
        show_voices
        ;;
    *)
        echo "用法:"
        echo "  ./carplay_voice.sh notify <任務名稱>"
        echo "  ./carplay_voice.sh reply <訊息>"
        echo "  ./carplay_voice.sh set-voice <聲音>"
        echo "  ./carplay_voice.sh get-voice"
        echo "  ./carplay_voice.sh voices"
        ;;
esac
