"""
WhatsApp Skill Implementation (Playwright Edition) - V3.0 ASYNC REFACTOR
Uses browser automation to send and read messages via WhatsApp Web.
Fully async implementation with proper Windows event loop handling.
"""
import logging
import asyncio
import sys
import os
import time
from typing import Dict, Any, List, Optional
import qrcode
import io
from playwright.async_api import async_playwright, Page, BrowserContext, Playwright

# Configure Logging
logger = logging.getLogger(__name__)

class FileLock:
    """Simple file lock to prevent multiple playwright instances on same dir"""
    def __init__(self, lock_file: str):
        self.lock_file = lock_file
        
    def acquire(self, timeout: int = 60) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not os.path.exists(self.lock_file):
                try:
                    with open(self.lock_file, 'w') as f:
                        f.write(str(os.getpid()))
                    return True
                except:
                    pass
            time.sleep(1)
        return False

    def release(self):
        try:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
        except:
            pass

class WhatsAppSkill:
    """
    Skill to handle WhatsApp interactions using Playwright.
    V3.0: Fully async, no sync wrappers, clean architecture.
    """
    
    def __init__(self, check_interval: int = 60, enabled: bool = True, headless: bool = True, session_dir: str = "./whatsapp_session"):
        self.check_interval = check_interval
        self.enabled = enabled
        self.headless = headless
        self.session_dir = os.path.abspath(session_dir)
        
        # Ensure session directory exists
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir, exist_ok=True)
        
        # Playwright instances (managed per operation)
        self._playwright: Optional[Playwright] = None
        self._lock = FileLock(os.path.join(self.session_dir, "whatsapp.lock"))

    async def _wait_for_login(self, page: Page) -> bool:
        """
        Waits for the user to be logged in. 
        If not logged in, detects QR code and prints it to terminal for headless auth.
        """
        logger.info("WhatsApp Skill: Waiting for login...")
        
        login_selector = '#pane-side, [data-testid="chat-list"], div[aria-label="Chat list"], [data-testid="chat-list-search"], [data-icon="chat"]'
        
        # Multiple QR code selectors for robustness
        qr_selectors = [
            'canvas[aria-label="Scan this QR code"]',
            'canvas[aria-label*="QR"]',
            'div[data-ref]',
            '[data-ref]',
            'canvas[role="img"]'
        ]
        
        try:
            # CRITICAL: First wait for EITHER login OR QR code to appear (up to 60s)
            logger.info("WhatsApp Skill: Waiting for page to fully load (login or QR)...")
            try:
                # Wait for either the chat list OR a canvas element to appear
                await page.wait_for_selector(
                    '#pane-side, canvas, div[data-ref], [data-ref]',
                    timeout=60000
                )
                logger.info("WhatsApp Skill: Page loaded - detected interactive element!")
            except Exception as e:
                logger.warning(f"WhatsApp Skill: Timed out waiting for page elements: {e}")
            
            # Check for "Loading your chats" screen
            try:
                loading_msg = page.get_by_text("Loading your chats")
                if await loading_msg.count() > 0:
                     logger.info("WhatsApp Skill: 'Loading your chats' detected. Waiting...")
                     await loading_msg.wait_for(state="detached", timeout=60000)
            except:
                pass


            # Loop to check for Login OR QR Code
            # User Requested: Single clear 60s attempt (we'll do 3 rounds of 60s just in case)
            for i in range(3): 
                logger.info(f"WhatsApp Skill: Scan attempt {i+1}/3...")
                
                # 1. Check if logged in (Searching for various "Logged In" elements)
                login_indicators = [
                    '#pane-side', 
                    '[data-testid="chat-list"]', 
                    'div[aria-label="Chat list"]', 
                    '[data-testid="chat-list-search"]', 
                    '[data-icon="chat"]',
                    '[data-testid="intro-text"]',
                    'div[data-testid="conversation-panel-messages"]',
                    'span[data-testid="menu"]',
                    '[data-testid="menu-bar-menu"]',
                    'div[role="application"]',
                    '[aria-label="Search input textbox"]',
                    'header[data-testid="chatlist-header"]'
                ]
                
                for selector in login_indicators:
                    if await page.locator(selector).count() > 0:
                        logger.info(f"WhatsApp Skill: ✅ Login detected via {selector}!")
                        return True
                
                # Check for "End-to-end encrypted" text (appears after scan, before chats load)
                try:
                    encrypted_text = page.get_by_text("End-to-end encrypted")
                    if await encrypted_text.count() > 0:
                        logger.info("WhatsApp Skill: ✅ Login detected via 'End-to-end encrypted' message!")
                        # Wait for chats to fully load
                        logger.info("WhatsApp Skill: Waiting 15s for chats to sync...")
                        await asyncio.sleep(15)
                        return True
                except:
                    pass
                
                # 2. Check for QR Code using multiple selectors
                qr_found = False
                data_ref = None
                
                for qr_selector in qr_selectors:
                    try:
                        count = await page.locator(qr_selector).count()
                        logger.info(f"WhatsApp Skill: Checking '{qr_selector}' - found {count} elements")
                        
                        if count > 0:
                            # Try to get data-ref attribute
                            elem = page.locator(qr_selector).first
                            data_ref = await elem.get_attribute("data-ref")
                            
                            if data_ref:
                                logger.info(f"WhatsApp Skill: ✅ QR Code found via '{qr_selector}'!")
                                qr_found = True
                                break
                            else:
                                # If no data-ref, try to screenshot the canvas
                                logger.info(f"WhatsApp Skill: Element found but no data-ref, trying canvas screenshot...")
                                try:
                                    await elem.screenshot(path="whatsapp_qr_canvas.png")
                                    logger.info("WhatsApp Skill: Canvas screenshot saved to whatsapp_qr_canvas.png")
                                    print("\n" + "="*60)
                                    print("       QR CODE DETECTED BUT CANNOT EXTRACT")
                                    print("       Please check whatsapp_qr_canvas.png file")
                                    print("       Or scan from the browser window")
                                    print("="*60 + "\n")
                                except Exception as e:
                                    logger.warning(f"WhatsApp Skill: Canvas screenshot failed: {e}")
                    except Exception as e:
                        logger.debug(f"WhatsApp Skill: Selector '{qr_selector}' check failed: {e}")
                        continue
                
                if qr_found and data_ref:
                    # CLEAR TERMINAL for visibility
                    os.system('clear' if os.name == 'posix' else 'cls')
                    
                    logger.info(f"WhatsApp Skill: 📸 QR Code detected (Attempt {i+1}/3).")
                    
                    qr = qrcode.QRCode(border=1)
                    qr.add_data(data_ref)
                    
                    # Save image
                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save("whatsapp_qr.png")
                    
                    # Print High-Contrast Blocks to Terminal
                    print("\n" + "="*60)
                    print("       ACTION REQUIRED: SCAN THIS QR CODE NOW")
                    print("       TERMINAL CLEARED FOR BETTER VISIBILITY")
                    print("       STABILITY MODE: FIXED FOR 60 SECONDS")
                    print("       TIP: Zoom Out (Ctrl and -) if it looks too big.")
                    print("="*60 + "\n")
                    
                    matrix = qr.get_matrix()
                    for row in matrix:
                        line = "".join(["██" if cell else "  " for cell in row])
                        print(line)
                    
                    print("\n" + "="*60)
                    print(f"       Checking for login every 5 seconds...")
                    print("="*60 + "\n")
                    
                    # ACTIVE POLLING: Check for login every 5 seconds for 60 seconds total
                    for check in range(12):  # 12 checks * 5 seconds = 60 seconds
                        await asyncio.sleep(5)
                        for selector in login_indicators:
                            if await page.locator(selector).count() > 0:
                                logger.info(f"WhatsApp Skill: ✅ Login detected via {selector}!")
                                return True
                        logger.info(f"WhatsApp Skill: Login check {check+1}/12... not yet")
                    continue
                else:
                    logger.warning(f"WhatsApp Skill: No QR code detected on attempt {i+1}. Waiting 30s before retry...")
                    await asyncio.sleep(30)

            logger.warning("WhatsApp Skill: Login check timed out after 3 attempts.")
            return False
            
        except Exception as e:
            logger.warning(f"WhatsApp Skill: Login/QR check failed: {e}")
            return False

    async def _init_browser(self) -> Optional[Page]:
        """Initialize browser and return page, or None if failed"""
        # Try to acquire lock first
        if not self._lock.acquire(timeout=60): # Wait up to 60s for other process to finish
            logger.warning("WhatsApp Skill: Could not acquire lock. Another process is using WhatsApp.")
            return None

        try:
            self._playwright = await async_playwright().start()
            
            self._context = await self._playwright.chromium.launch_persistent_context(
                user_data_dir=self.session_dir,
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = self._context.pages[0] if self._context.pages else await self._context.new_page()
            
            if "web.whatsapp.com" not in page.url:
                logger.info("WhatsApp Skill: Navigating to WhatsApp Web...")
                # Use networkidle to wait for page to FULLY load (not just DOM)
                await page.goto("https://web.whatsapp.com", wait_until="networkidle", timeout=90000)
            
            # CRITICAL: Wait 10 seconds for WhatsApp to render the QR code
            logger.info("WhatsApp Skill: Waiting 10s for page to fully render...")
            await asyncio.sleep(10)
            
            # Take a debug screenshot to see what's on the page
            try:
                await page.screenshot(path="whatsapp_debug.png")
                logger.info("WhatsApp Skill: Debug screenshot saved to whatsapp_debug.png")
            except:
                pass
            
            if not await self._wait_for_login(page):
                await self._cleanup()
                return None
                
            return page
            
        except Exception as e:
            logger.error(f"WhatsApp Skill: Browser init error: {e}")
            await self._cleanup()
            return None

    async def _cleanup(self):
        """Clean up browser resources"""
        try:
            if self._context:
                await self._context.close()
            if self._playwright:
                await self._playwright.stop()
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")
        finally:
            self._context = None
            self._playwright = None
            self._lock.release()

    async def send_message_async(self, number: str, message: str) -> Dict[str, Any]:
        """
        Send a WhatsApp message (async version).
        Supports Phone Number (+123...) OR Name ("Sir Junaid").
        """
        if not self.enabled:
            return {"success": False, "error": "WhatsApp skill is disabled"}
        
        page = await self._init_browser()
        if not page:
            return {"success": False, "error": "Failed to initialize browser or login"}
        
        try:
            is_number = number.replace("+", "").replace("-", "").strip().isdigit()
            
            if is_number:
                # Direct Navigation for Numbers
                clean_number = number.replace("+", "").replace(" ", "").replace("-", "")
                from urllib.parse import quote
                encoded_message = quote(message)
                send_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
                logger.info(f"WhatsApp Skill: Navigating to send message to {clean_number}...")
                await page.goto(send_url)
            else:
                # SMART SEARCH for Names
                logger.info(f"WhatsApp Skill: Searching for contact/group '{number}'...")
                
                # 1. Click Search
                search_selectors = [
                    'div[contenteditable="true"][data-tab="3"]',
                    'div[aria-label="Search"]',
                    'div[title="Search input textbox"]',
                    'button[aria-label="Search or start new chat"]'
                ]
                
                search_box = None
                for sel in search_selectors:
                    if await page.locator(sel).count() > 0:
                        search_box = page.locator(sel).first
                        break
                        
                if not search_box:
                    # Fallback: Just type '/' to focus search usually? Or 'Ctrl+F' logic?
                    # Let's try locating by placeholder text
                    search_box = page.get_by_placeholder("Search", exact=False).first
                
                if search_box:
                    await search_box.click()
                    await page.wait_for_timeout(500)
                    await page.keyboard.type(number)
                    await page.wait_for_timeout(3000) # Wait for results
                    
                    # 2. Select Result (Avoiding Meta AI)
                    logger.info("WhatsApp Skill: analyzing search results...")
                    
                    # Get all rows in the results pane
                    pane = page.locator('#pane-side') # The scrolling list container
                    rows = pane.locator('div[role="row"]')
                    
                    found_contact = False
                    count = await rows.count()
                    
                    for i in range(count):
                        row = rows.nth(i)
                        text = await row.text_content()
                        
                        # SKIP Meta AI or "Ask Meta AI" or "Search for..."
                        if "Meta AI" in text or "Ask Meta AI" in text:
                            continue
                            
                        # If it matches our search largely, click it
                        # Or simply click the first NON-Meta result
                        logger.info(f"WhatsApp Skill: Clicking result: {text[:30]}...")
                        await row.click()
                        found_contact = True
                        break
                        
                    if not found_contact:
                        # Fallback: Try strict title match if fuzzy failed
                        logger.warning("WhatsApp Skill: No valid contact found in results. Trying strict match...")
                        strict_sel = f'span[title="{number}"]'
                        if await page.locator(strict_sel).count() > 0:
                            await page.locator(strict_sel).first.click()
                        else:
                            return {"success": False, "error": f"Contact '{number}' not found (and avoided Meta AI)."}
                else:
                    return {"success": False, "error": "Could not find search box"}

            # Wait for input box to appear (confirming chat open)
            input_selector = 'footer div[contenteditable="true"]'
            start_time = time.time()
            found_input = False
            
            while time.time() - start_time < 30:
                # Check for invalid number popup (only for phone numbers)
                if is_number and await page.locator('div[data-testid="popup-controls-ok"]').is_visible():
                    logger.warning("WhatsApp Skill: Invalid number detected.")
                    await self._cleanup()
                    return {"success": False, "error": "Invalid WhatsApp number."}
                
                if await page.locator(input_selector).is_visible():
                    found_input = True
                    break
                await asyncio.sleep(1)
            
            if not found_input:
                raise TimeoutError("Chat input did not appear in time (Contact not found?).")
            
            # Focus and send
            await page.locator(input_selector).focus()
            
            # If we used search, we still need to type the message
            if not is_number:
                for line in message.split('\n'):
                    await page.keyboard.type(line)
                    await page.keyboard.down("Shift")
                    await page.keyboard.press("Enter")
                    await page.keyboard.up("Shift")
            else:
                # Message is already in box from URL, just needs focus?
                # Sometimes URL navigation pre-fills but doesn't send.
                # Actually, URL param pre-fills it.
                pass
                
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Enter")
            
            logger.info("WhatsApp Skill: Message submitted.")
            await page.wait_for_timeout(3000)
            return {"success": True, "status": "sent"}
            
        except Exception as e:
            logger.error(f"WhatsApp Skill: Send error: {e}")
            try:
                await page.screenshot(path="whatsapp_error.png")
            except:
                pass
            return {"success": False, "error": str(e)}
        finally:
            await self._cleanup()

    async def check_messages_async(
        self, 
        keywords: List[str] = None, 
        check_archived: bool = True, 
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Check WhatsApp messages (async version).
        Robust Archived folder logic using text-based locators.
        """
        if not self.enabled:
            return {"success": False, "error": "WhatsApp skill is disabled", "messages": []}
        
        page = await self._init_browser()
        if not page:
            return {"success": False, "error": "Failed to initialize browser or login", "messages": []}
        
        messages_found = []
        
        try:
            logger.info("WhatsApp Skill: Logged in, starting scan...")
            
            # Helper to parse visible chats
            async def parse_chats():
                # Give it more time to load all chats, especially for large histories
                logger.info("WhatsApp Skill: Waiting for chat rows to load (up to 90s)...")
                try:
                    await page.wait_for_selector('div[role="row"]', timeout=90000)
                except:
                    logger.warning("WhatsApp Skill: Timeout waiting for chat rows. List might be empty or DOM changed.")
                
                # Extra buffer for rendering
                await page.wait_for_timeout(5000) 
                
                rows = await page.locator('div[role="row"]').all()
                results = []
                for row in rows[:limit]:
                    try:
                        # Get Title
                        title_el = row.locator('[dir="auto"][title]')
                        if not await title_el.count():
                            # Sometimes title doesn't have [title] attr, just text
                            title_el = row.locator('div._ak8q span') # Generic class fallback? Risky.
                            if not await title_el.count():
                                continue

                        title = await title_el.first.text_content()
                        
                        # Get Last Message preview
                        preview_el = row.locator('span[dir="auto"]').last
                        preview = await preview_el.text_content() if await preview_el.count() else ""
                        
                        # Check unread badge
                        unread_el = row.locator('[aria-label*="unread message"]')
                        unread_count = await unread_el.text_content() if await unread_el.count() else "0"
                        
                        chat_data = {
                            "title": title,
                            "last_message": preview,
                            "unread": unread_count
                        }

                        # Filter by keyword if provided
                        if keywords:
                            match = False
                            for k in keywords:
                                if k.lower() in title.lower() or k.lower() in preview.lower():
                                    match = True
                                    chat_data['matched_keyword'] = k
                                    break
                            if match:
                                results.append(chat_data)
                        else:
                            results.append(chat_data)
                            
                    except Exception as e:
                        continue  # Skip buggy row
                return results

            # 1. Scroll ID 'pane-side' to trigger lazy loading
            logger.info("WhatsApp Skill: Scrolling chat list to load messages...")
            try:
                # Find the scrollable pane
                pane = page.locator('#pane-side')
                if await pane.count() > 0:
                     # Scroll down a few times
                     for _ in range(3):
                        await pane.evaluate("element => element.scrollTop += 500")
                        await page.wait_for_timeout(1000)
            except Exception as e:
                logger.warning(f"WhatsApp Skill: Scroll failed: {e}")

            # 2. Check Archived (PRIORITY)
            if check_archived:
                logger.info("WhatsApp Skill: Checking Archived folder (PRIORITY)...")
                try:
                    # ROBUST STRATEGY: Look for text "Archived" specifically
                    # This finds the Archived row/button regardless of CSS classes
                    archived_btn = page.get_by_text("Archived", exact=True).first
                    
                    if await archived_btn.is_visible():
                        logger.info("WhatsApp Skill: Found 'Archived' text, clicking...")
                        await archived_btn.click()
                        await page.wait_for_timeout(1000)
                        
                        archived_chats = await parse_chats()
                        for c in archived_chats:
                            c['source'] = 'archived'
                        messages_found.extend(archived_chats)
                        
                        # Go back
                        back_btn = page.locator('[data-icon="back"], button[aria-label="Back"]')
                        if await back_btn.count() > 0:
                            await back_btn.first.click()
                        else:
                            # If back button not found, try reloading to root
                            await page.goto("https://web.whatsapp.com")
                            await page.wait_for_timeout(2000)
                    else:
                        logger.warning("WhatsApp Skill: 'Archived' text not visible.")
                        
                except Exception as e:
                    logger.warning(f"WhatsApp Skill: Archived check failed: {e}")

            # 2. Scan Main Chat List
            logger.info("WhatsApp Skill: Scanning main chat list...")
            main_chats = await parse_chats()
            messages_found.extend(main_chats)
            
            return {"success": True, "messages": messages_found, "count": len(messages_found)}
            
        except Exception as e:
            logger.error(f"WhatsApp Scan Error: {e}")
            return {"success": False, "error": str(e), "messages": []}
        finally:
            await self._cleanup()

    # ========================================
    # SYNC WRAPPERS (for backward compatibility)
    # ========================================
    
    def send_message(self, number: str, message: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for send_message_async.
        Use this from non-async code.
        """
        return self._run_async(self.send_message_async(number, message))
    
    def check_messages(
        self, 
        keywords: List[str] = None, 
        check_archived: bool = True, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for check_messages_async.
        Use this from non-async code.
        """
        return self._run_async(self.check_messages_async(keywords, check_archived, limit))
    
    def _run_async(self, coro):
        """
        Helper to run async code from sync context.
        Handles Windows event loop properly.
        """
        if sys.platform == 'win32':
            # Set Windows-specific event loop policy
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        try:
            # Try to get existing loop
            loop = asyncio.get_running_loop()
            # If we're already in an async context, we can't use asyncio.run()
            # This should not happen with proper architecture, but handle it
            logger.warning("WhatsApp Skill: Called sync method from async context. Use async methods instead!")
            # Create new loop in thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        except RuntimeError:
            # No running loop, we can use asyncio.run()
            return asyncio.run(coro)


if __name__ == '__main__':
    # Test Block
    print('Testing WhatsApp Skill V3.0...')
    skill = WhatsAppSkill(headless=False)
    
    print('Test 1: Sending message...')
    result = skill.send_message('+923244279017', 'Test from WhatsApp Skill V3.0 🚀')
    print(f'Send result: {result}')
    
    print('\nTest 2: Checking messages...')
    msgs = skill.check_messages(keywords=['Test', 'Panaverse'])
    print(f'Found {len(msgs)} messages: {msgs}')
