"""
LinkedIn Login Helper
Opens a browser window for you to log in to LinkedIn manually.
The session will be saved for future use.
"""
import asyncio
import sys
from playwright.async_api import async_playwright

async def linkedin_login():
    """Open LinkedIn in a browser for manual login"""
    print("🔐 LinkedIn Login Helper")
    print("=" * 50)
    print("\nOpening LinkedIn in your browser...")
    print("Please log in manually and then close the browser window.")
    print("\nYour session will be saved in: ./linkedin_session")
    print("=" * 50)
    
    playwright = await async_playwright().start()
    
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="./linkedin_session",
        headless=False,  # Show browser
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--window-size=1280,800"
        ],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    page = context.pages[0] if context.pages else await context.new_page()
    
    # Navigate to LinkedIn
    await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
    
    print("\n✅ Browser opened!")
    print("\n📝 Instructions:")
    print("1. Log in to LinkedIn if you're not already logged in")
    print("2. Wait for the feed to load completely")
    print("3. Close this browser window when done")
    print("\nWaiting for you to close the browser...")
    
    # Wait for user to close the browser
    try:
        await page.wait_for_event("close", timeout=300000)  # 5 minutes timeout
    except:
        pass
    
    await context.close()
    await playwright.stop()
    
    print("\n✅ Session saved successfully!")
    print("You can now use LinkedIn features in the chatbot.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(linkedin_login())
