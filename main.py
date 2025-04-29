# main.py
import os
from mcp.server.fastmcp import FastMCP
import requests

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

# Create an MCP server
mcp = FastMCP("Github Dependabot alerts")

@mcp.tool()
def get_dependabot_alerts(repo_owner: str, repo_name: str) -> list[dict]:
    """Get Github Dependabot alerts"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dependabot/alerts"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, response.text)
        return []

