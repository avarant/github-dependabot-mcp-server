# Github Dependabot MCP server

Fetches Github Dependabot alerts for a specified repository.

## Requirements

-   **uv**: A fast Python package installer and resolver. Used to run the script and manage dependencies.
-   **Github Personal Access Token**: Required for authenticating with the Github API. Ensure it has the necessary permissions (e.g., `repo`, `security_events`).

## Setup

1.  **Install `uv`**:
    Follow the official installation instructions for your OS:
    -   **macOS / Linux**:
        -   Using Homebrew (macOS):
            ```bash
            brew install uv
            ```
        -   Or using curl:
            ```bash
            curl -LsSf https://astral.sh/uv/install.sh | sh
            ```
    -   **Windows (PowerShell)**:
        ```powershell
        irm https://astral.sh/uv/install.ps1 | iex
        ```
    -   **Other methods**: See the [uv documentation](https://docs.astral.sh/uv/).

2.  **Clone the repository**:
    ```bash
    git clone git@github.com:avarant/github-dependabot-mcp-server.git
    cd github-dependabot-mcp-server
    ```

3.  **Set up Github Authentication**:

    First, you need to generate a Github Personal Access Token (PAT) if you don't already have one:
    1.  Go to your Github Settings -> Developer settings -> Personal access tokens -> Tokens (classic).
    2.  Click "Generate new token" (or "Generate new token (classic)").
    3.  Give your token a descriptive name (e.g., "MCP Dependabot Server").
    4.  Set an expiration date.
    5.  Select the necessary scopes:
        *   `repo` (Full control of private repositories) - needed for accessing repository data.
        *   `security_events` (Read security events) - needed for reading Dependabot alerts.
    6.  Click "Generate token" and copy the generated token immediately. You won't be able to see it again.

    Once you have your token, this server requires it to authenticate with the Github API. There are two ways to provide it:

    *   **Option 1: Using macOS Keychain (Recommended on macOS)**:
        The script will automatically attempt to read the token from your macOS Keychain using the `keyring` library.

        *   **Via Command Line:**
            Run the following command in your terminal, replacing `<your token>` with your actual Github token:
            ```bash
            # Make sure you are in the project's virtual environment if you have one active
            # Or install keyring globally if needed: pip install keyring
            keyring set github_mcp_server personal_access_token
            # It will prompt you to enter the token securely.
            ```
            Alternatively, using the Python module:
            ```bash
            python -m keyring set github_mcp_server personal_access_token
            ```

        *   **Via Keychain Access UI:**
            1.  Open "Keychain Access" (Applications -> Utilities).
            2.  Select the `login` keychain and the `Passwords` category.
            3.  Click the `+` button to add a new item.
            4.  Enter the following details:
                *   **Keychain Item Name:** `personal_access_token`
                *   **Account Name:** `github_mcp_server`
                *   **Password:** Paste your Github token.
            5.  Click "Add".

    *   **Option 2: Using Environment Variable:**
        If the token is not found in the Keychain, the script will fall back to using the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable. If you use this method, the script will attempt to store the token in your Keychain for future use (if `keyring` is functional).

4.  **Update your MCP configuration**:

    Edit your global `~/.cursor/mcp.json` or create a local `.cursor/mcp.json` file within your project:

    ```json
    {
      "mcpServers": {
        "github": {
          "command": "docker",
          "args": [
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "mcp/github"
          ],
          "env": {
            // Optional: Set if NOT using Keychain, or as a fallback.
            // "GITHUB_PERSONAL_ACCESS_TOKEN": "<your github token>"
          }
        },
        "github-dependabot": {
          "command": "uv",
          "args": [
            "--directory",
            "<absolute path to github-dependabot-mcp-server directory>",
            "run",
            "mcp",
            "run",
            "main.py"
          ],
          "env": {
            // Optional: Set if NOT using Keychain, or as a fallback.
            // "GITHUB_PERSONAL_ACCESS_TOKEN": "<your github token>"
          }
        }
      }
    }
    ```
    **Note:** Replace `<absolute path to github-dependabot-mcp-server directory>` with your actual path.

## Tools Provided

This MCP server provides the following tool:

-   **`get_dependabot_alerts(repo_owner: str, repo_name: str)`**:
    -   Fetches Dependabot alerts for the specified repository.
    -   `repo_owner`: The owner of the repository (username or organization).
    -   `repo_name`: The name of the repository.
    -   Returns a list of alert objects from the Github API.

## Usage Example

example prompt

```
Fetch all dependabot alerts for https://github.com/avarant/github-dependabot-mcp-server
```
