"""
LinkedIn Auto-Poster - Fully Automated
Logs in once, then automatically posts your content
"""
import asyncio
import sys
import os
from playwright.async_api import async_playwright
from datetime import datetime

# LinkedIn credentials from .env
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "excellencelinks@gmail.com")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "nokia3310")

# Project details
GITHUB_URL = "https://github.com/Shafqatsarwar/hackathon_panaverse"
PROJECT_NAME = "Panaversity Student Assistant"

# Vibrant, modern LinkedIn post
POST_CONTENT = f"""🚀 Excited to share my latest AI project: {PROJECT_NAME}! 

🤖 An intelligent assistant powered by Google Gemini that automates student workflows:

✨ Key Features:
• 📧 Smart Gmail monitoring with AI-powered filtering
• 💬 WhatsApp integration for instant notifications
• 🔗 LinkedIn automation for networking
• 📊 Odoo CRM integration for lead management
• 🌐 Real-time web search capabilities
• 🧠 Autonomous task execution with AI agents

🛠️ Tech Stack:
• Google Gemini 2.5 Flash AI
• Python + FastAPI backend
• Next.js 15 frontend with glassmorphism UI
• Playwright for browser automation
• MCP (Model Context Protocol) architecture

💡 This project demonstrates the power of AI agents working together to create a seamless, automated workflow for students and professionals.

🔗 Check out the code on GitHub: {GITHUB_URL}

#AI #MachineLearning #Automation #Python #GoogleGemini #WebDevelopment #OpenSource #Innovation #Panaversity #PIAIC

Built with ❤️ for the Panaversity community!"""

async def auto_post_to_linkedin():
    print("=" * 80)
    print("🚀 LinkedIn Auto-Poster")
    print("=" * 80)
    print(f"\n📧 Email: {LINKEDIN_EMAIL}")
    print(f"🔗 GitHub: {GITHUB_URL}")
    print("\n" + "=" * 80)
    
    playwright = await async_playwright().start()
    
    browser = await playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars"
        ]
    )
    
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    
    page = await context.new_page()
    
    try:
        # Step 1: Go to LinkedIn
        print("\n🌐 Opening LinkedIn...")
        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        # Step 2: Login
        print("🔐 Logging in...")
        
        # Fill email
        email_input = page.locator('input[name="session_key"], input[id="username"]')
        await email_input.fill(LINKEDIN_EMAIL)
        await asyncio.sleep(1)
        
        # Fill password
        password_input = page.locator('input[name="session_password"], input[id="password"]')
        await password_input.fill(LINKEDIN_PASSWORD)
        await asyncio.sleep(1)
        
        # Click sign in
        sign_in_button = page.locator('button[type="submit"]')
        await sign_in_button.click()
        
        print("⏳ Waiting for login to complete...")
        await asyncio.sleep(5)
        
        # Check if we need verification
        current_url = page.url
        if "checkpoint" in current_url or "challenge" in current_url:
            print("\n⚠️ VERIFICATION REQUIRED!")
            print("Please complete the verification in the browser window.")
            print("This might include:")
            print("  - Email verification code")
            print("  - Phone verification")
            print("  - CAPTCHA")
            input("\n👉 Press Enter after you've completed verification...")
            await asyncio.sleep(2)
        
        # Wait for feed to load
        print("⏳ Waiting for feed to load...")
        try:
            await page.wait_for_selector('#global-nav', timeout=15000)
            print("✅ Successfully logged in!")
        except:
            print("⚠️ Login may have failed. Checking...")
            if "feed" not in page.url:
                print("❌ Not on feed page. Please check the browser.")
                input("👉 Press Enter if you're logged in and on the feed...")
        
        # Navigate to feed
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Step 3: Start a post
        print("\n📝 Starting a new post...")
        
        # Try to find and click "Start a post" button
        start_post_selectors = [
            'button.share-box-feed-entry__trigger',
            'button[aria-label*="Start a post"]',
            '.share-box-feed-entry__trigger',
            'button:has-text("Start a post")'
        ]
        
        clicked = False
        for selector in start_post_selectors:
            try:
                button = page.locator(selector).first
                if await button.count() > 0:
                    await button.click()
                    print(f"✅ Clicked 'Start a post' button")
                    clicked = True
                    break
            except:
                continue
        
        if not clicked:
            print("⚠️ Could not find 'Start a post' button automatically.")
            print("Please click it manually in the browser.")
            input("👉 Press Enter after clicking 'Start a post'...")
        
        await asyncio.sleep(2)
        
        # Step 4: Fill in the post content
        print("⌨️ Typing post content...")
        
        # Find the editor
        editor_selectors = [
            '.ql-editor',
            'div[role="textbox"]',
            'div[contenteditable="true"]',
            '.share-creation-state__text-editor'
        ]
        
        editor_found = False
        for selector in editor_selectors:
            try:
                editor = page.locator(selector).first
                if await editor.count() > 0:
                    await editor.click()
                    await asyncio.sleep(1)
                    
                    # Type the content
                    await editor.fill(POST_CONTENT)
                    print("✅ Post content entered!")
                    editor_found = True
                    break
            except Exception as e:
                continue
        
        if not editor_found:
            print("⚠️ Could not find post editor automatically.")
            print("\n📋 Here's your post content to paste manually:")
            print("-" * 80)
            print(POST_CONTENT)
            print("-" * 80)
            
            # Try to copy to clipboard
            try:
                import pyperclip
                pyperclip.copy(POST_CONTENT)
                print("\n✅ Content copied to clipboard! Press Ctrl+V to paste.")
            except:
                pass
            
            input("\n👉 Press Enter after pasting the content...")
        
        await asyncio.sleep(2)
        
        # Step 5: Post it
        print("\n🚀 Looking for 'Post' button...")
        
        post_button_selectors = [
            'button.share-actions__primary-action',
            'button[aria-label*="Post"]',
            'button:has-text("Post")',
            '.share-actions__primary-action'
        ]
        
        post_clicked = False
        for selector in post_button_selectors:
            try:
                button = page.locator(selector).first
                if await button.count() > 0:
                    print(f"✅ Found 'Post' button!")
                    print("\n⏸️ REVIEW YOUR POST")
                    print("Please review the post in the browser window.")
                    print("Make any edits if needed.")
                    
                    response = input("\n👉 Type 'yes' to post, or 'no' to cancel: ")
                    
                    if response.lower() == 'yes':
                        await button.click()
                        print("✅ Post button clicked!")
                        post_clicked = True
                        await asyncio.sleep(3)
                    else:
                        print("❌ Post cancelled by user.")
                    break
            except:
                continue
        
        if not post_clicked:
            print("\n⚠️ Could not find 'Post' button automatically.")
            print("Please click the 'Post' button manually in the browser.")
            input("👉 Press Enter after posting...")
        
        print("\n" + "=" * 80)
        print("🎉 SUCCESS!")
        print("=" * 80)
        print("\n✅ Your post should now be live on LinkedIn!")
        print(f"🔗 GitHub URL shared: {GITHUB_URL}")
        print("\n💡 Next steps:")
        print("   • Check your LinkedIn profile")
        print("   • Engage with comments")
        print("   • Share in relevant groups")
        print("=" * 80)
        
        input("\n👉 Press Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📋 Here's your post content:")
        print(POST_CONTENT)
        input("\nPress Enter to close...")
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(auto_post_to_linkedin())
