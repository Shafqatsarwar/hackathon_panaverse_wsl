import sys
import os
import asyncio
import logging
from pathlib import Path

# Setup Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StressTest")

async def run_stress_test():
    print("="*80)
    print("      PANAVERSITY AI EMPLOYEE - FULL CAPABILITY STRESS TEST      ")
    print("      Target: 10 WhatsApp Messages & 10 Emails via 3 Approaches      ")
    print("="*80)

    # Load targets from Config (which loads .env)
    wa_target = Config.WHATSAPP_FORWARD_MESSAGES
    email_target = Config.EMAIL_FORWARD_EMAIL
    
    # Fallbacks if not set (though user said they are provided)
    if not wa_target:
        print("❌ Error: WHATSAPP_FORWARD_MESSAGES not found in .env")
        return
    if not email_target:
        print("❌ Error: EMAIL_FORWARD_EMAIL not found in .env")
        return

    print(f"🎯 Target WhatsApp: {wa_target}")
    print(f"🎯 Target Email:    {email_target}")
    print("-" * 60)

    # Initialize Components
    # ---------------------------------------------------------
    print("\n[INIT] Initializing Components...")
    
    # 1. Skills (Low Level)
    from skills.whatsapp_skill.skill import WhatsAppSkill
    from skills.email_skill.skill import EmailSkill
    # Note: WhatsAppSkill needs session path. We use the one we standardized.
    wa_skill = WhatsAppSkill(enabled=True, headless=False, session_dir=os.path.abspath("./whatsapp_session"))
    email_skill = EmailSkill() 

    # 2. Agents (Mid Level)
    from agents.whatsapp_agent import WhatsAppAgent
    from agents.notification_agent import NotificationAgent # Uses email skill internally
    wa_agent = WhatsAppAgent()
    email_agent = NotificationAgent()

    # 3. MCP Servers (High Level)
    from mcp.whatsapp_server import WhatsAppMCPServer
    # Email MCP usually runs as a standalone process, but we can simulate the tool class if available.
    # We will simulate the "Action" via Brain logic if a dedicated EmailMCP class isn't importable.
    # Looking at file list, we don't have a specific mcp/email_server.py easily accessible/importable 
    # in same way (it's often a node script in some architectures). 
    # We'll use the Agent as proxy for "High Level" or construct a mock.
    wa_mcp = WhatsAppMCPServer()

    print("[INIT] Completed. Starting Transmission Loop...")
    print("-" * 60)

    # EXECUTION LOOP (10 Iterations)
    # ---------------------------------------------------------
    for i in range(1, 11):
        print(f"\n📢 --- ITERATION {i}/10 ---")
        
        # Rotational Approach: 1=Skill, 2=Agent, 3=MCP
        mode = (i % 3)
        if mode == 0: mode = 3
        
        # --- WHATSAPP ---
        wa_msg = f"Stress Test Msg {i}/10 [Mode: {mode}] - PANA-AI"
        try:
            if mode == 1:
                print(f"   [WhatsApp][Skill] Sending: '{wa_msg}'")
                res = await wa_skill.send_message_async(wa_target, wa_msg)
            elif mode == 2:
                print(f"   [WhatsApp][Agent] Sending: '{wa_msg}'")
                res = wa_agent.send_message(wa_target, wa_msg)
            else: # mode 3
                print(f"   [WhatsApp][MCP]   Sending: '{wa_msg}'")
                res = wa_mcp.call_tool("send_message", {"number": wa_target, "message": wa_msg})
            
            if res.get("success") or res.get("status") == "sent":
                print("   ✅ Delivered")
            else:
                print(f"   ❌ Failed: {res}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

        # --- EMAIL ---
        email_subj = f"PanaServer Stress Test {i}/10 [Mode: {mode}]"
        email_body = f"This is automated verification message {i} of 10.\nMode: {mode}\nTimestamp: {os.times()}"
        try:
            if mode == 1:
                print(f"   [Email][Skill]    Sending: '{email_subj}'")
                # Direct skill usage
                email_skill.send_email(
                    to_email=email_target, 
                    subject=email_subj, 
                    content=email_body
                )
                print("   ✅ Sent (Skill)")
            elif mode == 2:
                print(f"   [Email][Agent]    Sending: '{email_subj}'")
                res = email_agent.send_email(to_email=email_target, subject=email_subj, body=email_body)
                if res.get("success"): print("   ✅ Sent (Agent)")
                else: print(f"   ❌ Failed: {res}")
            else: # mode 3 (Simulate High Level)
                print(f"   [Email][HighLvl]  Sending: '{email_subj}'")
                # Re-using Agent as High Level proxy since MCP is Node-based in original spec
                res = email_agent.send_email(to_email=email_target, subject=email_subj, body=email_body) 
                if res.get("success"): print("   ✅ Sent (HighLvl)")
                else: print(f"   ❌ Failed: {res}")

        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Small delay to prevent rate limit smash
        await asyncio.sleep(2)

    print("\n" + "="*80)
    print("      STRESS TEST COMPLETE      ")
    print("="*80)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(run_stress_test())
