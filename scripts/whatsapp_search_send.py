"""
Script to search for a contact by name and send a message.
Useful when phone number is unknown.
"""
import asyncio
import logging
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONTACT_NAME = "Sir Junaid Sb PIAIC UMT"
MESSAGE = """Hello Sir Junaid, this is the Panaversity Student Assistant (Agentic AI). 

We are facing a technical blocker with our Playwright integration for WhatsApp. 
The issue: We cannot programmatically detect the 'Archived' folder button to read archived messages, even though it is visible in the UI. Our selectors (aria-label, title) are failing.

We would appreciate any guidance on how to robustly access the Archived folder using Playwright in the latest WhatsApp Web UI.

Repo: https://github.com/Shafqatsarwar/hackathon_panaverse.git
Thank you!"""

async def send_via_search():
    logger.info(f"Attempting to send message to '{CONTACT_NAME}'...")
    
    async with async_playwright() as p:
        user_data_dir = "./whatsapp_session"
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://web.whatsapp.com")
        
        # Wait for login
        try:
            await page.wait_for_selector('[data-testid="chat-list"], #pane-side', timeout=30000)
            logger.info("Login verified.")
        except:
            logger.error("Login failed or timed out.")
            await context.close()
            return

        # Click Search Box
        logger.info("Looking for search box...")
        search_selectors = [
            'div[contenteditable="true"][data-tab="3"]',
            'div[aria-label="Search"]',
            'div[title="Search input textbox"]'
        ]
        
        search_box = None
        for sel in search_selectors:
            if await page.locator(sel).count() > 0:
                search_box = page.locator(sel).first
                break
                
        if not search_box:
            logger.error("Could not find search box.")
            await context.close()
            return
            
        await search_box.click()
        await page.keyboard.type(CONTACT_NAME)
        await asyncio.sleep(2)
        
        # Wait for results and click first one
        # Results are usually in a list. We define a generic waiter.
        logger.info("Selecting contact...")
        try:
            # Locate the contact item that matches the text
            # We look for a span with the title
            contact_selector = f'span[title="{CONTACT_NAME}"]'
            await page.wait_for_selector(contact_selector, timeout=5000)
            await page.locator(contact_selector).first.click()
            logger.info("Contact selected.")
            
            # Wait for chat pane to open (look for footer input)
            input_selector = 'footer div[contenteditable="true"]'
            await page.wait_for_selector(input_selector, timeout=10000)
            
            # Type and Send
            await page.locator(input_selector).focus()
            
            # Type message (handle newlines)
            for line in MESSAGE.split('\n'):
                await page.keyboard.type(line)
                await page.keyboard.down("Shift")
                await page.keyboard.press("Enter")
                await page.keyboard.up("Shift")
                
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Enter")
            logger.info("Message SENT!")
            
            await page.wait_for_timeout(3000) # Wait for sync
            
        except Exception as e:
            logger.error(f"Failed to select contact or send: {e}")
            await page.screenshot(path="search_send_fail.png")
            
        await context.close()

if __name__ == "__main__":
    asyncio.run(send_via_search())
