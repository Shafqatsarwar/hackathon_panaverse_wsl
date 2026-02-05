"""
GitHub Agent
"""
import logging
from typing import Dict, Any
from skills.github_skill.skill import GitHubSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class GitHubAgent:
    """Agent for GitHub interaction"""
    
    def __init__(self):
        self.skill = GitHubSkill(
            token=Config.GITHUB_TOKEN,
            username=Config.GITHUB_USERNAME
        )
        self.enabled = bool(Config.GITHUB_TOKEN and Config.GITHUB_TOKEN != "your_github_token_here")
        
    def check_updates(self) -> Dict[str, Any]:
        """Check for updates"""
        if not self.enabled:
            return {"success": False, "error": "Disabled"}
        return self.skill.list_repos()
        
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "GitHubAgent",
            "enabled": self.enabled
        }
