import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    print("Test: Launching Headless Chromium...")
    try:
        async with async_playwright() as p:
            print("Playwright start...")
            browser = await p.chromium.launch(headless=True)
            print("Browser launched successfully!")
            page = await browser.new_page()
            await page.goto('http://example.com')
            print(f"Page title: {await page.title()}")
            await browser.close()
            print("Browser closed.")
            print("✅ TEST PASSED: System libraries are PRESENT.")
            return True
            
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main())
