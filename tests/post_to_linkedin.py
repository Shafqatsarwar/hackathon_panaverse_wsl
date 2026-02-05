"""
LinkedIn Post Creator - Simple Version
Since you're already logged in, this will just help you post
"""
import asyncio
import sys
from playwright.async_api import async_playwright

# Project details
GITHUB_URL = "https://github.com/Shafqatsarwar/hackathon_panaverse_wsl"
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

async def post_to_linkedin():
    print("=" * 80)
    print("🚀 LinkedIn Post Creator - Interactive Mode")
    print("=" * 80)
    
    print("\n📄 YOUR POST CONTENT:")
    print("=" * 80)
    print(POST_CONTENT)
    print("=" * 80)
    
    # Try to copy to clipboard
    try:
        import pyperclip
        pyperclip.copy(POST_CONTENT)
        print("\n✅ POST CONTENT COPIED TO CLIPBOARD!")
    except ImportError:
        print("\n⚠️ pyperclip not installed. Installing now...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "pyperclip"], 
                      capture_output=True)
        try:
            import pyperclip
            pyperclip.copy(POST_CONTENT)
            print("✅ POST CONTENT COPIED TO CLIPBOARD!")
        except:
            print("⚠️ Could not copy to clipboard automatically.")
    
    print("\n" + "=" * 80)
    print("📝 INSTRUCTIONS:")
    print("=" * 80)
    print("1. A browser will open to LinkedIn (you're already logged in)")
    print("2. Click the 'Start a post' button")
    print("3. Press Ctrl+V to paste the content (already in clipboard)")
    print("4. Review the post and click 'Post'")
    print("=" * 80)
    
    input("\n👉 Press Enter to open LinkedIn...")
    
    playwright = await async_playwright().start()
    
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="./linkedin_session",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--window-size=1280,900"
        ],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    
    page = context.pages[0] if context.pages else await context.new_page()
    
    print("\n🌐 Opening LinkedIn feed...")
    await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
    await asyncio.sleep(3)
    
    print("\n✅ LinkedIn opened!")
    print("\n" + "=" * 80)
    print("📋 NEXT STEPS:")
    print("=" * 80)
    print("1. Look for the 'Start a post' button at the top of your feed")
    print("2. Click it")
    print("3. Press Ctrl+V to paste the content")
    print("4. Add any images if you want (optional)")
    print("5. Click the 'Post' button")
    print("=" * 80)
    
    print("\n💡 TIP: The post content is in your clipboard - just press Ctrl+V!")
    
    input("\n👉 Press Enter after you've posted (or when you're done)...")
    
    await context.close()
    await playwright.stop()
    
    print("\n" + "=" * 80)
    print("🎉 AWESOME! Your post should now be live!")
    print("=" * 80)
    print(f"\n🔗 GitHub URL shared: {GITHUB_URL}")
    print("\n💡 Next steps:")
    print("   • Check your LinkedIn profile to see the post")
    print("   • Engage with comments to boost visibility")
    print("   • Share in relevant groups")
    print("=" * 80)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(post_to_linkedin())
