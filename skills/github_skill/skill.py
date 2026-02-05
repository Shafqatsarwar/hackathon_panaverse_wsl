"""
GitHub Skill Implementation
"""
import logging
import requests
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GitHubSkill:
    """Skill to handle GitHub interactions"""
    
    def __init__(self, token: str, username: str = None):
        self.token = token
        self.username = username
        self.base_url = "https://api.github.com"
        
    def list_repos(self, limit: int = 5) -> Dict[str, Any]:
        """List user repositories"""
        if not self.token or self.token == "your_github_token_here":
            return {"success": False, "error": "GITHUB_TOKEN not configured"}
            
        try:
            headers = {"Authorization": f"token {self.token}", "Accept": "application/vnd.github.v3+json"}
            response = requests.get(f"{self.base_url}/user/repos?sort=updated&per_page={limit}", headers=headers)
            
            if response.status_code == 200:
                repos = [{"name": r["full_name"], "url": r["html_url"], "updated": r["updated_at"]} for r in response.json()]
                return {"success": True, "repos": repos}
            return {"success": False, "error": f"API Error: {response.status_code}"}
        except Exception as e:
            logger.error(f"GitHub Skill Error: {e}")
            return {"success": False, "error": str(e)}
            
    def get_recent_activity(self) -> Dict[str, Any]:
        """Get recent activity summary (mockable logic for agent)"""
        # For simplicity, just listing repos is good enough for "activity" check in phase 5
        return self.list_repos(limit=3)
