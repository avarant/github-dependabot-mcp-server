# main.py
import os
import logging  # Add logging import
import keyring # Import keyring
from mcp.server.fastmcp import FastMCP
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Attempt to get GitHub token from keyring first
GITHUB_TOKEN = None
SERVICE_NAME = "github_mcp_server" # Define a service name for keyring
USERNAME = "personal_access_token" # Define a username/key for keyring

try:
    GITHUB_TOKEN = keyring.get_password(SERVICE_NAME, USERNAME)
    if GITHUB_TOKEN:
        logging.info("Successfully retrieved GitHub token from keyring.")
    else:
        logging.info("No GitHub token found in keyring, trying environment variable.")
except Exception as e:
    logging.warning(f"Could not retrieve token from keyring: {e}. Trying environment variable.") # Log keyring access issues

# Fallback to environment variable if not found in keyring
if not GITHUB_TOKEN:
    GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if GITHUB_TOKEN:
        logging.info("Successfully retrieved GitHub token from environment variable.")
        # Optionally store the token in keyring for future use
        try:
            keyring.set_password(SERVICE_NAME, USERNAME, GITHUB_TOKEN)
            logging.info("Stored GitHub token from environment variable into keyring.")
        except Exception as e:
            logging.warning(f"Could not store token from environment variable into keyring: {e}")
    else:
        logging.error("GITHUB_PERSONAL_ACCESS_TOKEN not found in keyring or environment variables.") # Log error
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not found in keyring or environment variables.")

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

