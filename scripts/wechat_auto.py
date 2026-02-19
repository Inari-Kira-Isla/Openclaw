#!/usr/bin/env python3
"""
WeChat 網頁版自動輸入腳本
使用 Playwright 實現自動輸入
"""
import asyncio
import sys
from playwright.async_api import async_playwright

# ===== 設定區 =====
TARGET_CONTACT = "稻荷 協成 日本貨"  # 要發送訊息的聯絡人名稱
MESSAGE = "測試自動發送訊息！Hello from AI 🤖"  # 要發送的訊息
WECHAT_URL = "https://web.wechat.com"
USER_DATA_DIR = "/tmp/wechat-profile"  # 儲存登入狀態
# ==================

async def send_wechat_message(contact: str, message: str):
    async with async_playwright() as p:
        # 使用持久化 profile，保留登入狀態
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  # 設為 True 可背景執行
            args=["--no-sandbox"],
            viewport={"width": 1280, "height": 800},
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print(f"[1/4] 開啟 WeChat 網頁版...")
        await page.goto(WECHAT_URL, wait_until="networkidle")
        
        # 等待登入
        print("[2/4] 等待登入...")
        try:
            await page.wait_for_selector(".contact_item, .chat_item, #search_bar", timeout=60000)
            print("✅ 已登入！")
        except:
            print("⚠️ 請掃描 QR Code 登入，等待中...")
            await page.wait_for_selector(".contact_item, .chat_item, #search_bar", timeout=120000)
            print("✅ 登入成功！")
        
        # 搜尋聯絡人
        print(f"[3/4] 搜尋聯絡人：{contact}")
        try:
            search = page.locator("#search_bar, input[placeholder*='搜'], input[type='text']").first
            await search.click()
            await page.keyboard.type(contact, delay=50)
            await page.wait_for_timeout(1500)
            
            result = page.locator(".contact_item, .search_item").first
            await result.click()
            await page.wait_for_timeout(1000)
            print("✅ 已開啟對話！")
        except Exception as e:
            print(f"❌ 搜尋失敗：{e}")
            await context.close()
            return
        
        # 輸入並發送訊息
        print(f"[4/4] 發送訊息：{message}")
        try:
            input_box = page.locator(".input_area, [contenteditable='true'], textarea").last
            await input_box.click()
            await page.wait_for_timeout(500)
            await input_box.type(message, delay=30)
            await page.wait_for_timeout(500)
            await page.keyboard.press("Enter")
            print("✅ 訊息已發送！")
        except Exception as e:
            print(f"❌ 輸入失敗：{e}")
        
        await page.wait_for_timeout(2000)
        await context.close()
        print("\n✅ 完成！")

if __name__ == "__main__":
    asyncio.run(send_wechat_message(TARGET_CONTACT, MESSAGE))
