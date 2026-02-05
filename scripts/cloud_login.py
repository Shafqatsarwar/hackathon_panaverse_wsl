"""
Cloud Login Helper
Run this on your Cloud VM to log into WhatsApp.
Since there is no screen, it saves 'qr_code.png' which you can download and scan.
"""
import sys
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

async def cloud_login():
    print("=" * 60)
    print("CLOUD LOGIN HELPER")
    print("=" * 60)
    
    session_dir = "./whatsapp_session"
    print(f"Session Dir: {session_dir}")
    
    async with async_playwright() as p:
        print("Launching Headless Browser...")
        # Note: Headless must be True on cloud
        context = await p.chromium.launch_persistent_context(
            session_dir,
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("Navigating to WhatsApp Web...")
        await page.goto("https://web.whatsapp.com")
        
        print("Waiting for load...")
        await asyncio.sleep(5)
        
        # Loop for 60 seconds, taking snapshots
        for i in range(12):
            screenshot_path = "qr_code.png"
            await page.screenshot(path=screenshot_path)
            print(f"[{i*5}s] Snapshot saved to {screenshot_path}. Download and scan if QR is visible.")
            
            # Check for login
            try:
                await page.wait_for_selector(
                    '[data-testid="chat-list"], #pane-side', 
                    timeout=5000
                )
                print("\n✅ SUCCESS: Logged in!")
                break
            except:
                pass
                
        await context.close()
        print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(cloud_login())
