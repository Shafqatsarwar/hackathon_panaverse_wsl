import os
import shutil
import asyncio
import sys

# Add root to sys.path
sys.path.append(os.getcwd())

from skills.whatsapp_skill.skill import WhatsAppSkill

async def main():
    print("=== WhatsApp Verification Tool ===")
    session_path = os.path.abspath("./whatsapp_session")
    
    if os.path.exists(session_path):
        print(f"Detected existing session at: {session_path}")
        print("Cleaning up session to resolve database errors...")
        try:
            # Simple retry logic for Windows file locks
            for i in range(3):
                try:
                    shutil.rmtree(session_path)
                    print("Session cleaned successfully.")
                    break
                except Exception as e:
                    if i == 2: raise e
                    print(f"Retrying cleanup ({i+1})...")
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"Error cleaning session: {e}")
            print("Please MANUALY delete the 'whatsapp_session' folder and try again.")
            return

    print("\nLaunching WhatsApp Web...")
    print("ACTION REQUIRED: Scan the QR code with your phone when it appears.")
    
    print("ACTION REQUIRED: Scan the QR code below with your phone!")
    
    # Headless=True to trigger the console QR code print we implemented
    skill = WhatsAppSkill(headless=True, session_dir=session_path)
    
    # Initialize browser - this will open the window and wait for login
    page = await skill._init_browser()
    
    if page:
        print("\n" + "="*40)
        print("SUCCESS: WhatsApp Login Detected!")
        print("="*40)
        print("Saving session... please wait 10 seconds before closing.")
        await asyncio.sleep(10)
        await skill._cleanup()
        print("Verification complete. You can now run the autonomous system.")
    else:
        print("\n" + "!"*40)
        print("FAILURE: Login timed out or browser closed.")
        print("!"*40)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
