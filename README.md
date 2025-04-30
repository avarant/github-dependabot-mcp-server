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

3.  **Update your MCP configuration**:

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
            "GITHUB_PERSONAL_ACCESS_TOKEN": "<your github token>"
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
            "GITHUB_PERSONAL_ACCESS_TOKEN": "<your github token>"
          }
        }
      }
    }
    ```
    **Note:** Replace `<absolute path to github-dependabot-mcp-server directory>` and `<your github token>` with your actual values. Using an absolute path ensures Cursor can find the server regardless of the workspace root.

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
