
import asyncio
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Import Agents and Skills
from agents.main_agent import MainAgent
from skills.whatsapp_skill.skill import WhatsAppSkill
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from src.utils.config import Config

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('autonomous_fte.log')
    ]
)
logger = logging.getLogger("AutonomousFTE")

class AutonomousFTE:
    """
    Autonomous Full-Time Employee (FTE) Runner.
    Polls skills and triggers Main Agent hooks.
    """
    def __init__(self):
        self.main = MainAgent()
        # Initialize Skills directly for polling
        self.whatsapp_skill = WhatsAppSkill(enabled=Config.WHATSAPP_ENABLED, headless=True) # Headless for deploy
        self.gmail_skill = GmailMonitoringSkill(
            Config.GMAIL_CREDENTIALS_PATH, 
            Config.GMAIL_TOKEN_PATH,
            Config.FILTER_KEYWORDS
        )
        self.gmail_authenticated = False
        
        self.running = True

    def initialize(self):
        """Init Main Agent and Skills"""
        self.main.initialize()
        
        # Auth Gmail
        if self.gmail_skill.authenticate():
            self.gmail_authenticated = True
            logger.info("FTE: Gmail Monitoring Active.")
        else:
            logger.warning("FTE: Gmail Monitoring Failed.")

    async def _poll_whatsapp(self):
        """Poll WhatsApp for Panaversity messages"""
        if not self.whatsapp_skill.enabled: return
        
        logger.info("FTE: Checking WhatsApp for updates...")
        
        # Running in thread because Playwright might be blocking or complex
        # Note: WhatsAppSkill V2 handles its own loop logic internally usually, 
        # but calling it from here inside an async loop needs care.
        # check_messages is our V2 method
        
        # Use a list of keywords from Config + 'Panaverse' explicit
        keywords = Config.FILTER_KEYWORDS + ["Panaversity", "Panaverse", "PIAIC"]
        
        # sync wrapper call
        loop = asyncio.get_running_loop()
        msgs = await loop.run_in_executor(None, self.whatsapp_skill.check_messages, keywords)
        
        if msgs and not isinstance(msgs[0], dict) or "error" not in msgs[0]:
            # Found content
            for msg in msgs:
                if "error" in msg: continue
                logger.info(f"FTE: Found WhatsApp Match: {msg.get('title')}")
                # HOOK: Trigger Main Agent
                self.main.process_trigger("whatsapp", msg)

    async def _poll_gmail(self):
        """Poll Gmail for Panaverse emails"""
        if not self.gmail_authenticated: return
        
        logger.info("FTE: Checking Gmail for updates...")
        loop = asyncio.get_running_loop()
        
        # Run blocking gmail check in executor
        emails = await loop.run_in_executor(None, self.gmail_skill.check_emails)
        
        if emails:
            logger.info(f"FTE: Found {len(emails)} relevant emails.")
            for email in emails:
                # HOOK: Trigger Main Agent
                self.main.process_trigger("email", email)

    async def start(self, interval_seconds=120):
        """Start the autonomous event loop"""
        self.initialize()
        logger.info(f"FTE: Started. Polling every {interval_seconds}s...")
        
        # Initial run
        await self._poll_whatsapp()
        await self._poll_gmail()
        
        while self.running:
            logger.info("FTE: Sleeping...")
            await asyncio.sleep(interval_seconds)
            
            # Run Cycle
            await self._poll_whatsapp()
            await self._poll_gmail()

if __name__ == "__main__":
    runner = AutonomousFTE()
    try:
        # Windows Loop Policy (Crucial for Playwright)
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
             
        asyncio.run(runner.start(interval_seconds=60))
    except KeyboardInterrupt:
        logger.info("FTE: Stopping...")
