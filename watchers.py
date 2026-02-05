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
            
        # Initialize WhatsApp Skill
        # Initialize WhatsApp Skill
        self.whatsapp_enabled = self.config.WHATSAPP_ENABLED
        if self.whatsapp_enabled:
            from skills.whatsapp_skill.skill import WhatsAppSkill
            session_path = "./whatsapp_session" # Use relative to root, same as verify script
            logger.info(f"WhatsApp Session Path: {os.path.abspath(session_path)}")
            
            self.whatsapp_skill = WhatsAppSkill(
                enabled=True,
                headless=True, 
                session_dir=session_path
            )

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
        """Check for new relevant WhatsApp messages"""
        logger.info("Checking WhatsApp...")
        try:
            # Check for specific keywords
            result = self.whatsapp_skill.check_messages(
                keywords=self.config.FILTER_KEYWORDS,
                check_archived=True,
                limit=10
            )
            
            if result.get("success") and result.get("messages"):
                messages = result["messages"]
                logger.info(f"Found {len(messages)} relevant WhatsApp messages.")
                
                for msg in messages:
                    # Create unique ID based on timestamp and title
                    msg_id = f"{msg.get('title')}_{int(datetime.now().timestamp())}"
                    safe_id = "".join([c for c in msg_id if c.isalnum() or c in "_-"])
                    
                    file_name = f"WHATSAPP_{safe_id}.md"
                    file_path = self.needs_action_path / file_name
                    
                    content = f"""---
type: whatsapp
source: whatsapp_web
status: pending
timestamp: {datetime.now().isoformat()}
sender: {msg.get('title')}
matched_keyword: {msg.get('matched_keyword', 'manual')}
---

# Message Snippet
{msg.get('last_message')}

# Details
Title: {msg.get('title')}
Unread Count: {msg.get('unread')}
Source: {msg.get('source', 'main_list')}
"""
                    if not file_path.exists():
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        logger.info(f"Created WhatsApp task: {file_name}")
                        
        except Exception as e:
            logger.error(f"WhatsApp check failed: {e}")

if __name__ == "__main__":
    watchers = WatcherSystem()
    watchers.run()
