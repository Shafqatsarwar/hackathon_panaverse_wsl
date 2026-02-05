"""
Watchers: The Senses of the AI
Monitors external inputs and creates tasks in data/vault/Needs_Action
"""
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from src.utils.config import Config
from agents.email_agent import EmailAgent

import os # Added os import

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Watchers")

class WatcherSystem:
    def __init__(self):
        self.config = Config
        self.vault_path = Path("data/vault")
        self.inbox_path = self.vault_path / "Inbox"
        self.needs_action_path = self.vault_path / "Needs_Action"
        
        # Ensure directories exist
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        self.needs_action_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Agents/Sensors
        self.email_agent = EmailAgent(
            credentials_path=self.config.GMAIL_CREDENTIALS_PATH,
            token_path=self.config.GMAIL_TOKEN_PATH,
            filter_keywords=self.config.FILTER_KEYWORDS
        )
        self.email_ready = False
        try:
            if self.email_agent.authenticate():
                self.email_ready = True
        except Exception as e:
            logger.error(f"Email Watcher failed to init: {e}")
            
        # Initialize WhatsApp Skill (Baileys - No Browser!)
        self.whatsapp_enabled = self.config.WHATSAPP_ENABLED
        self.whatsapp_skill = None
        if self.whatsapp_enabled:
            from skills.whatsapp_baileys.skill import WhatsAppBaileysSkill
            self.whatsapp_skill = WhatsAppBaileysSkill(
                base_url=self.config.WHATSAPP_BAILEYS_URL
            )
            logger.info(f"WhatsApp Baileys initialized: {self.config.WHATSAPP_BAILEYS_URL}")

    def run(self):
        logger.info("Starting Watcher System...")
        time.sleep(2) # Give user time to read logs
        
        last_email_check = 0
        last_whatsapp_check = 0
        last_odoo_check = 0
        
        while True:
            try:
                current_time = time.time()
                
                # Check WhatsApp Interval
                if self.whatsapp_enabled:
                    if (current_time - last_whatsapp_check) >= (self.config.WHATSAPP_CHECK_INTERVAL * 60):
                        self.check_whatsapp()
                        last_whatsapp_check = time.time()
                
                # Check Email Interval (convert minutes to seconds)
                # if (current_time - last_email_check) >= (self.config.EMAIL_CHECK_INTERVAL * 60):
                #     self.check_email()
                #     last_email_check = time.time()
                
                # Check Odoo (Every 15 mins default or same as email)
                # if (current_time - last_odoo_check) >= (15 * 60):
                #     self.check_odoo()
                #     last_odoo_check = time.time()
                
            except Exception as e:
                logger.error(f"Watcher Loop Error: {e}")
            
            # Sleep for 1 minute before next iteration check
            time.sleep(60)

    def check_email(self):
        if not self.email_ready:
            return

        logger.info("Checking emails...")
        # Mark as read so we don't process them again in the next loop
        emails = self.email_agent.check_emails(mark_read=True)
        for email in emails:
            # Create a task in Needs_Action
            file_name = f"EMAIL_{int(datetime.now().timestamp())}_{email.get('id', 'unknown')}.md"
            file_path = self.needs_action_path / file_name
            
            content = f"""---
type: email
source: gmail
status: pending
priority: {email.get('priority', 'medium')}
timestamp: {datetime.now().isoformat()}
sender: {email.get('sender')}
subject: {email.get('subject')}
---

# Email Content
{email.get('snippet')}

# Raw Body
{email.get('body', 'No body content')}
"""
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"Created task: {file_name}")

    def check_odoo(self):
        """Check Odoo for new tasks (Mock functionality to demonstrate flow)"""
        # For now, we assume Odoo is reactive (tools used by Brain), 
        # but we could poll for 'Assigned' tasks here.
        pass

    def check_whatsapp(self):
        """Check WhatsApp connection status using Baileys"""
        logger.info("Checking WhatsApp (Baileys)...")
        try:
            if not self.whatsapp_skill:
                logger.warning("WhatsApp skill not initialized")
                return
                
            # Check connection status
            status = self.whatsapp_skill.get_status()
            if status.get("connected"):
                logger.info("✅ WhatsApp Baileys connected")
                
                # Get recent chats
                chats = self.whatsapp_skill.get_chats(limit=10)
                chat_list = chats.get("chats", [])
                
                if chat_list:
                    logger.info(f"Found {len(chat_list)} recent chats")
                    
                    # Filter for keywords
                    keywords = [k.lower() for k in self.config.FILTER_KEYWORDS]
                    for chat in chat_list:
                        chat_name = chat.get("name", "").lower()
                        # Check if chat name contains any keyword
                        matched = any(kw in chat_name for kw in keywords)
                        
                        if matched:
                            msg_id = f"{chat.get('name', 'unknown')}_{int(datetime.now().timestamp())}"
                            safe_id = "".join([c for c in msg_id if c.isalnum() or c in "_-"])
                            
                            file_name = f"WHATSAPP_{safe_id}.md"
                            file_path = self.needs_action_path / file_name
                            
                            content = f"""---
type: whatsapp
source: baileys
status: pending
timestamp: {datetime.now().isoformat()}
sender: {chat.get('name')}
---

# WhatsApp Chat
Name: {chat.get('name')}
ID: {chat.get('id')}
"""
                            if not file_path.exists():
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write(content)
                                logger.info(f"Created WhatsApp task: {file_name}")
            else:
                logger.warning("⚠️ WhatsApp not connected - check QR code")
                        
        except Exception as e:
            logger.error(f"WhatsApp check failed: {e}")

if __name__ == "__main__":
    watchers = WatcherSystem()
    watchers.run()
