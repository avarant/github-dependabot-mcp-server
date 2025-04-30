# Github Dependabot alerts MCP server

mcp server for github dependabot alert

## Requirements

-   **uv**: A fast Python package installer and resolver.
-   **Github access token**: You need a personal access token from Github.

## Setup

1.  **Install `uv`:**
    `uv` is used to run the script and manage its dependencies directly from the script header. Follow the official installation instructions for your OS:
    -   **macOS / Linux:**
        -   Using Homebrew (macOS):
            ```bash
            brew install uv
            ```
        -   Or using curl:
            ```bash
            curl -LsSf https://astral.sh/uv/install.sh | sh
            ```
    -   **Windows (PowerShell):**
        ```powershell
        irm https://astral.sh/uv/install.ps1 | iex
        ```
    -   **Other methods:** See the [uv documentation](https://docs.astral.sh/uv/).

2. Clone the project

```bash
git clone git@github.com:avarant/github-dependabot-mcp-server.git
```

3. Update your MCP config

Cursor

edit your `~/.cursor/mcp.json` or your local `.cursor/mcp.json`

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
        "<path to git repo>",
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
