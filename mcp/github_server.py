"""
GitHub MCP Server for Panaversity Student Assistant
Monitors GitHub repositories for coursework
"""
import os
import logging
import requests
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class GitHubMCPServer:
    """MCP Server for GitHub operations"""
    
    def __init__(self):
        self.name = "github"
        self.version = "1.0.0"
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.base_url = "https://api.github.com"
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available GitHub tools"""
        return [
            {
                "name": "list_repos",
                "description": "List user's GitHub repositories",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_recent_commits",
                "description": "Get recent commits from a repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {
                            "type": "string",
                            "description": "Repository name (owner/repo)"
                        },
                        "count": {
                            "type": "number",
                            "description": "Number of commits to fetch",
                            "default": 5
                        }
                    },
                    "required": ["repo"]
                }
            }
        ]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        if not self.token and name != "list_repos": # list_repos might work public/mock? No, needs auth usually for "user's" repos
             # Allow mock/empty response if no token configured for testing
             pass

        if name == "list_repos":
            return self._list_repos()
        elif name == "get_recent_commits":
            return self._get_recent_commits(
                arguments["repo"],
                arguments.get("count", 5)
            )
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def _list_repos(self) -> Dict[str, Any]:
        """List repositories"""
        if not self.token or self.token == "your_github_token_here":
            return {
                "success": False,
                "error": "GITHUB_TOKEN not configured in .env",
                "repos": []
            }
            
        try:
            headers = {"Authorization": f"token {self.token}", "Accept": "application/vnd.github.v3+json"}
            response = requests.get(f"{self.base_url}/user/repos", headers=headers)
            if response.status_code == 200:
                repos = [{"name": r["full_name"], "url": r["html_url"]} for r in response.json()[:5]]
                return {"success": True, "repos": repos}
            return {"success": False, "error": f"GitHub API error: {response.status_code}"}
        except Exception as e:
            logger.error(f"GitHub Error: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_recent_commits(self, repo: str, count: int) -> Dict[str, Any]:
        """Get recent commits"""
        if not self.token or self.token == "your_github_token_here":
             return {"success": False, "error": "GITHUB_TOKEN not configured"}

        try:
            headers = {"Authorization": f"token {self.token}", "Accept": "application/vnd.github.v3+json"}
            url = f"{self.base_url}/repos/{repo}/commits?per_page={count}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                commits = [{"message": c["commit"]["message"], "author": c["commit"]["author"]["name"]} for c in response.json()]
                return {"success": True, "commits": commits}
            return {"success": False, "error": f"GitHub API error: {response.status_code}"}
        except Exception as e:
             return {"success": False, "error": str(e)}

if __name__ == "__main__":
    server = GitHubMCPServer()
    logger.info(f"GitHub MCP Server v{server.version} started")
