#!/bin/bash
# OpenClaw Whisper 轉換腳本

if [ $# -lt 1 ]; then
    echo "用法: ./whisper.sh <輸入檔案> [選項]"
    echo ""
    echo "選項:"
    echo "  --model tiny/base/small/medium/large  (預設: medium)"
    echo "  --language zh/en/ja                    (預設: zh)"
    echo "  --output_format srt/vtt/txt           (預設: srt)"
    echo ""
    echo "範例:"
    echo "  ./whisper.sh meeting.wav"
    echo "  ./whisper.sh meeting.wav --model small --language zh"
    exit 1
fi

INPUT=$1
OUTPUT_DIR="./output"
MODEL="medium"
LANG="zh"
FORMAT="srt"

# 解析參數
shift
while [ $# -gt 0 ]; do
    case "$1" in
        --model) MODEL=$2; shift 2 ;;
        --language) LANG=$2; shift 2 ;;
        --output_format) FORMAT=$2; shift 2 ;;
        *) shift ;;
    esac
done

# 建立輸出目錄
mkdir -p "$OUTPUT_DIR"

# 取得檔名
BASENAME=$(basename "$INPUT" .${INPUT##*.})
OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.$FORMAT"

echo "🎙️  Whisper 轉換"
echo "輸入: $INPUT"
echo "輸出: $OUTPUT_FILE"
echo "模型: $MODEL"
echo "語言: $LANG"
echo ""

# 執行轉換
whisper "$INPUT" \
    --model "$MODEL" \
    --language "$LANG" \
    --output_format "$FORMAT" \
    --output_dir "$OUTPUT_DIR"

echo ""
echo "✅ 完成! 輸出位置: $OUTPUT_FILE"
