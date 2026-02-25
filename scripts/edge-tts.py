#!/usr/bin/env python3
# Edge TTS - 免費文字轉語音
# 使用 Microsoft Edge 的免費 TTS 服務

import argparse
import asyncio
import edge_tts
import sys
import os

VOICES = {
    'zh-TW': 'zh-TW-HsiaoYuNeural',
    'zh-CN': 'zh-CN-XiaoxiaoNeural',
    'en': 'en-US-JennyNeural',
}

async def speak(text, output, voice):
    """轉換文字為語音"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output)
        print(f"✅ 已保存: {output}")
        
        # 播放
        os.system(f"afplay '{output}' &")
        return True
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

async def list_voices():
    """列出所有可用聲音"""
    voices = await edge_tts.list_voices()
    for v in voices:
        if v['ShortName'].startswith('zh'):
            print(f"{v['ShortName']}: {v['FriendlyName']}")

def main():
    parser = argparse.ArgumentParser(description='Edge TTS - 免費文字轉語音')
    parser.add_argument('text', nargs='?', help='要轉換的文字')
    parser.add_argument('-o', '--output', default='output.mp3', help='輸出檔案')
    parser.add_argument('-v', '--voice', default='zh-TW', help='語言: zh-TW, zh-CN, en')
    parser.add_argument('--list', action='store_true', help='列出可用聲音')
    
    args = parser.parse_args()
    
    if args.list:
        asyncio.run(list_voices())
        return
    
    if not args.text:
        print("用法: edge-tts.py <文字> [-o output.mp3] [-v zh-TW]")
        print("範例: edge-tts.py '你好' -o hello.mp3 -v zh-TW")
        print("")
        print("可用語言:")
        for k, v in VOICES.items():
            print(f"  {k}: {v}")
        sys.exit(1)
    
    voice = VOICES.get(args.voice, VOICES['zh-TW'])
    asyncio.run(speak(args.text, args.output, voice))

if __name__ == '__main__':
    main()
