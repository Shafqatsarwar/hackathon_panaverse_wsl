import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill

logging.basicConfig(level=logging.INFO)

def test():
    try:
        gmail = GmailMonitoringSkill(
            credentials_path=Config.GMAIL_CREDENTIALS_PATH,
            token_path=Config.GMAIL_TOKEN_PATH,
            keywords=Config.FILTER_KEYWORDS
        )
        success = gmail.authenticate()
        with open("gmail_auth_status.txt", "w") as f:
            f.write(f"AUTHENTICATION: {'SUCCESS' if success else 'FAILED'}")
    except Exception as e:
        with open("gmail_auth_status.txt", "w") as f:
            f.write(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test()
