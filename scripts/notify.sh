#!/bin/bash
# 任務完成語音通知腳本
# 用法: ./notify.sh "任務類型" "任務內容"

TYPE="$1"
CONTENT="$2"

# 根據任務類型選擇語音
case "$TYPE" in
    "訓練")
        say -v Meijia "訓練完成，$CONTENT"
        ;;
    "知識庫")
        say -v Meijia "知識庫更新完成，$CONTENT"
        ;;
    "系統")
        say -v Meijia "系統任務完成，$CONTENT"
        ;;
    "整理")
        say -v Meijia "資料整理完成，$CONTENT"
        ;;
    *)
        say -v Meijia "任務完成，$CONTENT"
        ;;
esac
