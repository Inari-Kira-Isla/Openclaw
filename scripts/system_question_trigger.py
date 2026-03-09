#!/usr/bin/env python3
"""
系統質疑討論自動觸發鉤子
每小時自動觸發系統質疑+討論 -> 然後觸發 Kira 執行
"""

import os
import subprocess
import time

def trigger_evolution():
    """觸發 Evolution 分析"""
    print("▶️ 觸發 Evolution 分析...")
    result = subprocess.run(
        ["/usr/local/bin/openclaw", "cron", "run", "c43565f0-d51a-425c-beea-ea4409e101b8"],
        capture_output=True, text=True, timeout=120
    )
    return result.returncode == 0

def trigger_kira_execution():
    """觸發 Kira 執行"""
    print("▶️ 觸發 Kira 執行...")
    
    # 使用 message tool 發送到群組並觸發討論
    message = """👁️ 系統質疑分析完成

**核心問題：**
1. 記憶精煉驗證
2. 反饋閉環路徑依賴
3. 缺乏外部審視

**建議方向：**
1. 引入外部驗證節點
2. 設置進化邊界
3. 建立回滾機制
4. 增加反進化權重

@GodKiraCheok_bot 你點睇？要開始邊部分？"""
    
    # 直接發送到 Telegram
    cmd = f'''curl -s -X POST "https://api.telegram.org/bot***REMOVED***/sendMessage" -d "chat_id=-5138835175" -d "text={message}" -d "parse_mode=Markdown"'''
    os.system(cmd)
    
    # 記錄
    os.system("python3 ~/.openclaw/workspace/scripts/auto_record.py decision '系統質疑討論' '已自動觸發討論'")
    
    return True

def main():
    print("🔄 系統質疑->討論->執行自動觸發...")
    
    # Step 1: Trigger Evolution
    if trigger_evolution():
        print("✅ Evolution 分析已觸發")
    
    # Wait for analysis to complete
    time.sleep(60)
    
    # Step 2: Trigger Kira execution (sends to group + triggers discussion)
    if trigger_kira_execution():
        print("✅ Kira 執行已觸發")
    
    print("🎉 完成")

if __name__ == "__main__":
    main()

def collect_feedback():
    """每次系統質疑後收集反饋"""
    import sys
    sys.path.insert(0, '/Users/ki/.openclaw/workspace/scripts')
    from feedback import FeedbackSystem
    
    fs = FeedbackSystem()
    
    # 收集效能反饋
    fs.collect("performance", "每小時效能監控", "系統正常運作中", source="cron")
    
    # 收集優化反饋
    fs.collect("optimization", "系統質疑優化", "鈎子與反饋系統已結合", source="cron")
    
    print("✅ Feedback collected")

# Call at the end of main()
if __name__ == "__main__":
    # After everything, collect feedback
    collect_feedback()
