"""
Main Orchestrator Agent - Coordinates Email and Notification Agents
"""
import logging
import schedule
import time
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from src.utils.config import Config
from agents.email_agent import EmailAgent
from agents.notification_agent import NotificationAgent
from agents.whatsapp_agent import WhatsAppAgent
from agents.linkedin_agent import LinkedInAgent
from agents.github_agent import GitHubAgent
from agents.odoo_agent import OdooAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('panaversity_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MainAgent:
    """Main orchestrator coordinating all sub-agents"""
    
    def __init__(self):
        self.config = Config
        self.email_agent = None
        self.email_agent = None
        self.email_agent_ready = False
        self.notification_agent = None
        self.whatsapp_agent = None
        self.linkedin_agent = None
        self.github_agent = None
        self.odoo_agent = None
        self.running = False
        self.chat_history_dir = Path("History/chat_history")
        self.chat_history_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate configuration
        errors = self.config.validate()
        if errors:
            logger.error("Configuration errors:")
            for error in errors:
                logger.error(f"  - {error}")
            raise ValueError("Invalid configuration")
    
    def initialize(self):
        """Initialize all agents"""
        logger.info("Main Agent: Initializing Panaversity Student Assistant...")
        
        self.config.print_config()
        
        # Initialize Email Agent
        self.email_agent = EmailAgent(
            credentials_path=self.config.GMAIL_CREDENTIALS_PATH,
            token_path=self.config.GMAIL_TOKEN_PATH,
            filter_keywords=self.config.FILTER_KEYWORDS
        )
        
        
        try:
            if self.email_agent.authenticate():
                self.email_agent_ready = True
                logger.info("Main Agent: Email Agent initialized and authenticated")
            else:
                logger.error("Main Agent: Email authentication failed (Auth flow returned False)")
        except Exception as e:
            logger.error(f"Main Agent: Email authentication failed: {e}")
            logger.info("Main Agent: Continuing without Email Monitoring...")
        
        logger.info("Main Agent: Email Agent initialization step complete")
        
        # Initialize Notification Agent
        self.notification_agent = NotificationAgent(
            smtp_server=self.config.SMTP_SERVER,
            smtp_port=self.config.SMTP_PORT,
            smtp_username=self.config.SMTP_USERNAME,
            smtp_password=self.config.SMTP_PASSWORD
        )
        
        logger.info("Main Agent: Notification Agent initialized")
        
        # Initialize WhatsApp Agent
        if self.config.WHATSAPP_ENABLED:
            self.whatsapp_agent = WhatsAppAgent()
            logger.info("Main Agent: WhatsApp Agent initialized")
        else:
            logger.info("Main Agent: WhatsApp Agent disabled (skipping initialization)")
            
        # Initialize LinkedIn Agent
        if self.config.LINKEDIN_ENABLED:
            self.linkedin_agent = LinkedInAgent()
            logger.info("Main Agent: LinkedIn Agent initialized")
        else:
            logger.info("Main Agent: LinkedIn Agent disabled (skipping initialization)")

        # Initialize GitHub Agent (Active if token present)
        self.github_agent = GitHubAgent()
        if self.github_agent.enabled:
             logger.info("Main Agent: GitHub Agent initialized")
        else:
             logger.info("Main Agent: GitHub Agent disabled (no token)")

        # Initialize Odoo Agent
        self.odoo_agent = OdooAgent()
        if self.odoo_agent.enabled:
            logger.info("Main Agent: Odoo Agent initialized")
        else:
            logger.info("Main Agent: Odoo Agent disabled (missing config)")

        logger.info("Main Agent: Initialization complete!")
    
    def check_emails(self):
        """Execute email check task"""
        logger.info("=" * 60)
        logger.info("Main Agent: Running email check task...")
        
        try:
            if not self.email_agent_ready:
                # Skip log spam if we know it's down
                return

            # Get relevant emails from Email Agent
            relevant_emails = self.email_agent.check_emails()
            
            if not relevant_emails:
                logger.info("Main Agent: No new relevant emails")
                self._log_to_chat_history("email_check", {
                    "status": "completed",
                    "emails_found": 0
                })
                return
            
            logger.info(f"Main Agent: Processing {len(relevant_emails)} email(s)")
            
            # Send notifications via Notification Agent
            for email in relevant_emails:
                safe_subject = email['subject'].encode('ascii', 'ignore').decode('ascii')
                logger.info(f"Main Agent: Processing '{safe_subject}'")
                
                success = self.notification_agent.send_email_alert(
                    admin_email=self.config.ADMIN_EMAIL,
                    email_data=email
                )
                
                if success:
                    logger.info(f"[OK] Notification sent for: {email['subject']}")
                else:
                    logger.error(f"[FAIL] Failed to send notification for: {email['subject']}")
                
                # Send WhatsApp Alert
                if self.whatsapp_agent:
                    wa_message = f"📧 New Important Email: {email['subject']}\nFrom: {email.get('sender', 'Unknown')}"
                    wa_result = self.whatsapp_agent.send_alert(wa_message)
                    if wa_result.get("success"):
                        logger.info(f"[OK] WhatsApp alert sent for: {email['subject']}")
                    else:
                        logger.error(f"[FAIL] Failed to send WhatsApp alert: {wa_result.get('error')}")
                
                # Create Odoo Lead
                if self.odoo_agent and self.odoo_agent.enabled:
                    odoo_result = self.odoo_agent.create_lead_from_email(email)
                    if odoo_result.get("success"):
                        logger.info(f"[OK] Created Odoo Lead ID: {odoo_result.get('id')}")
                    else:
                        logger.error(f"[FAIL] Failed to create Odoo Lead: {odoo_result.get('error')}")

            # Log to chat history
            self._log_to_chat_history("email_check", {
                "status": "completed",
                "emails_found": len(relevant_emails),
                "emails": [{"subject": e['subject'], "priority": e.get('priority')} for e in relevant_emails]
            })
        
        except Exception as e:
            logger.error(f"Main Agent: Error during email check: {str(e)}")
            self._log_to_chat_history("email_check", {
                "status": "error",
                "error": str(e)
            })
        
        logger.info("Main Agent: Email check task complete")
        logger.info("=" * 60)
    
    def _log_to_chat_history(self, task_name: str, data: Dict[str, Any]):
        """Log task execution to chat history"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "task": task_name,
            "data": data
        }
        
        # Create daily log file
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.chat_history_dir / f"{date_str}.json"
        
        # Append to log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def schedule_tasks(self):
        """Schedule periodic tasks"""
        logger.info("Main Agent: Scheduling periodic tasks...")
        
        schedule.every(self.config.EMAIL_CHECK_INTERVAL).minutes.do(self.check_emails)
        logger.info(f"Main Agent: Email checks scheduled every {self.config.EMAIL_CHECK_INTERVAL} minutes")
    
    def start(self):
        """Start the assistant in background mode"""
        logger.info("Main Agent: Starting Panaversity Student Assistant...")
        
        self.initialize()
        self.schedule_tasks()
        
        # Run initial check
        logger.info("Main Agent: Running initial email check...")
        self.check_emails()
        
        # Start scheduled loop
        self.running = True
        logger.info("Main Agent: Assistant is now running. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Main Agent: Stopping assistant...")
            self.running = False
    
    def run_manual_check(self):
        """Run a single manual email check"""
        logger.info("Main Agent: Running manual email check...")
        self.initialize()
        self.check_emails()
        logger.info("Main Agent: Manual check complete!")
    
    def status(self):
        """Show current status"""
        logger.info("Main Agent: Status Report")
        logger.info("=" * 50)
        logger.info(f"Running: {self.running}")
        
        if self.email_agent:
            email_status = self.email_agent.get_status()
            logger.info(f"Email Agent: {email_status}")
        
        if self.notification_agent:
            notif_status = self.notification_agent.get_status()
            logger.info(f"Notification Agent: {notif_status}")
            
        if self.whatsapp_agent:
            wa_status = self.whatsapp_agent.get_status()
            logger.info(f"WhatsApp Agent: {wa_status}")
            
        if self.linkedin_agent:
            li_status = self.linkedin_agent.get_status()
            logger.info(f"LinkedIn Agent: {li_status}")
            
        if self.github_agent:
            gh_status = self.github_agent.get_status()
            logger.info(f"GitHub Agent: {gh_status}")
        
        logger.info("=" * 50)
    
    def get_status(self):
        """Get status as dictionary for API consumption"""
        return {
            "agent": "MainAgent",
            "running": self.running,
            "email_agent": self.email_agent.get_status() if self.email_agent_ready else "auth_failed",
            "notification_agent": self.notification_agent.get_status() if self.notification_agent else "not_initialized",
            "whatsapp_agent": self.whatsapp_agent.get_status() if self.whatsapp_agent else "disabled",
            "linkedin_agent": self.linkedin_agent.get_status() if self.linkedin_agent else "disabled",
            "github_agent": self.github_agent.get_status() if self.github_agent else "disabled",
            "odoo_agent": self.odoo_agent.get_status() if self.odoo_agent else "disabled",
            "config": {
                "email_check_interval": self.config.EMAIL_CHECK_INTERVAL,
                "filter_keywords": self.config.FILTER_KEYWORDS,
                "whatsapp_enabled": self.config.WHATSAPP_ENABLED,
                "linkedin_enabled": self.config.LINKEDIN_ENABLED
            }
        }

    def process_trigger(self, source: str, event_data: Dict[str, Any]):
        """
        Hook: Process external triggers (like WhatsApp 'Panaverse' message).
        Used by the Autonomous Runner.
        """
        logger.info(f"Main Agent: Trigger received from {source}!")
        
        # Log Trigger
        self._log_to_chat_history("trigger_received", {"source": source, "data": event_data})
        
        # Logic: If trigger is from WhatsApp/Email about Panaverse -> Run Analysis or Actions
        trigger_summary = f"Trigger from {source}: {json.dumps(event_data)}"
        
        # 1. Notify Admin via WhatsApp (if urgency high)
        if self.whatsapp_agent:
            self.whatsapp_agent.send_alert(f"🔔 System Trigger: {trigger_summary[:100]}...")

        # 2. Sync to Odoo if it's a message/lead
        if source == "whatsapp" or source == "linkedin":
            if self.odoo_agent and self.odoo_agent.enabled:
                sender = event_data.get('sender', 'Unknown')
                content = event_data.get('last_message') or event_data.get('content') or ""
                self.odoo_agent.create_lead_from_email({
                    "subject": f"Trigger from {source}: {sender}",
                    "sender": sender,
                    "body": content
                })  # Reusing email method for now or add generic create_lead
        
        logger.info("Main Agent: Trigger processing complete.")
