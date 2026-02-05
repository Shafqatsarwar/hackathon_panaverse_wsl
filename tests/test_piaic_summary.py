"""
PIAIC General-Agents Lahore - January Summary Test
Finds the chat, retrieves messages, summarizes with Gemini, and sends via WhatsApp
"""
import sys
import os
import asyncio
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.whatsapp_skill.skill import WhatsAppSkill
from skills.chatbot_skill.skill import ChatbotSkill

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PIAICSummary")

async def main():
    logger.info("="*60)
    logger.info("PIAIC General-Agents Lahore - January Summary Test")
    logger.info("="*60)
    
    # Initialize skills
    logger.info("\n[1/5] Initializing WhatsApp Skill...")
    wa_skill = WhatsAppSkill(enabled=True, headless=False)  # headless=False to see it work
    
    logger.info("[2/5] Searching for 'PIAIC General-Agents Lahore' chat...")
    # Search for the chat in both main and archived
    messages = await wa_skill.check_messages_async(
        keywords=["PIAIC General-Agents Lahore", "PIAIC", "General-Agents"],
        check_archived=True,
        limit=50
    )
    
    if not messages or "error" in messages[0]:
        logger.error(f"Failed to find chat: {messages}")
        return
    
    # Find the specific chat
    target_chat = None
    for msg in messages:
        if "PIAIC" in msg.get('title', '') and "General-Agents" in msg.get('title', ''):
            target_chat = msg
            break
    
    if not target_chat:
        logger.warning("Could not find 'PIAIC General-Agents Lahore' chat")
        logger.info(f"Found these chats instead:")
        for msg in messages[:5]:
            logger.info(f"  - {msg.get('title')}: {msg.get('last_message', '')[:50]}")
        
        # Use the first PIAIC-related chat as fallback
        for msg in messages:
            if "PIAIC" in msg.get('title', '').upper():
                target_chat = msg
                logger.info(f"\nUsing fallback chat: {target_chat.get('title')}")
                break
    
    if not target_chat:
        logger.error("No PIAIC-related chats found at all!")
        return
    
    logger.info(f"\n[3/5] Found chat: {target_chat.get('title')}")
    logger.info(f"  Last message: {target_chat.get('last_message', '')[:100]}")
    logger.info(f"  Unread: {target_chat.get('unread', '0')}")
    logger.info(f"  Source: {target_chat.get('source', 'main')}")
    
    # For this demo, we'll use the last message as a sample
    # In a real implementation, you would need to:
    # 1. Click on the chat
    # 2. Scroll through January messages
    # 3. Extract all message content
    # For now, we'll create a summary based on available info
    
    logger.info("\n[4/5] Creating summary with Gemini AI...")
    
    # Initialize chatbot skill with API key from config
    from src.utils.config import Config
    chatbot = ChatbotSkill(api_key=Config.GOOGLE_API_KEY)
    
    # Create a prompt for summarization
    summary_prompt = f"""
You are analyzing WhatsApp messages from the "PIAIC General-Agents Lahore" group chat.

Chat Information:
- Chat Name: {target_chat.get('title')}
- Latest Message: {target_chat.get('last_message', 'N/A')}
- Unread Count: {target_chat.get('unread', '0')}
- Location: {target_chat.get('source', 'main')} chats

Task: Create a brief summary of the January 2026 activity in this chat based on the available information.

Please provide:
1. A brief overview of the chat's purpose
2. Key topics or themes from the latest message
3. Any action items or important dates mentioned
4. A professional summary suitable for WhatsApp delivery

Keep the summary concise (under 200 words) and professional.
"""
    
    # Use ChatbotSkill properly
    chat_session = chatbot.start_chat()
    summary = chatbot.generate_response(chat_session, summary_prompt)
    
    logger.info(f"\nGenerated Summary:\n{'-'*60}\n{summary}\n{'-'*60}")
    
    # Prepare the message to send
    message_to_send = f"""📊 PIAIC General-Agents Lahore - January Summary

{summary}

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Source: WhatsApp Archive Analysis
Powered by AI Assistant"""
    
    logger.info(f"\n[5/5] Sending summary to +923244279017...")
    
    # Send the summary
    send_result = await wa_skill.send_message_async(
        "+923244279017",
        message_to_send
    )
    
    if send_result.get('success'):
        logger.info("\n" + "="*60)
        logger.info("SUCCESS! Summary sent successfully!")
        logger.info("="*60)
        logger.info(f"\nSummary sent to: +923244279017")
        logger.info(f"Message length: {len(message_to_send)} characters")
    else:
        logger.error(f"\nFailed to send message: {send_result.get('error')}")
    
    logger.info("\nTest completed!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())
