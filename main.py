# main.py
import os
import logging  # Add logging import
from mcp.server.fastmcp import FastMCP
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
if not GITHUB_TOKEN:
    logging.error("GITHUB_TOKEN environment variable not set.") # Log error
    raise ValueError("GITHUB_TOKEN environment variable not set.")

# Create an MCP server
mcp = FastMCP("Github Dependabot alerts")

@mcp.tool()
def get_dependabot_alerts(repo_owner: str, repo_name: str) -> list[dict]:
    """Get Github Dependabot alerts"""
    logging.info(f"Fetching Dependabot alerts for {repo_owner}/{repo_name}") # Log start
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dependabot/alerts"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        logging.info(f"Successfully fetched alerts for {repo_owner}/{repo_name}") # Log success
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}, Response: {response.text}") # Log HTTP errors
        # Decide how to handle: re-raise, return specific error message, or empty list
        return [] # Returning empty list for now
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}") # Log other request errors (network, timeout, etc.)
        return [] # Returning empty list for now
    except Exception as e:
        logging.exception(f"An unexpected error occurred while fetching alerts for {repo_owner}/{repo_name}: {e}") # Log any other unexpected errors
        return [] # Returning empty list for now

