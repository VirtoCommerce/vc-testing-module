# Playwright + Python Project Setup

## Prerequisites

0. Install Cursor AI (recommended IDE)
1. Clone/download project and open with Cursor AI (or PyCharm)

Make sure you have the following installed on your system:

- Python (version 3.7 or later)
- pip (Python package manager)

1. **Create and activate a virtual environment**

   ```sh
   python -m venv .venv
   source venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**

   ```sh
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install pre-commit hooks**

   ```sh
   pre-commit install
   ```

   > **Note:** This step needs to be done manually after installing requirements. Pre-commit hooks (including Black formatter) cannot be installed automatically through requirements.txt as this is a Git security feature.

4. **Install Playwright browsers**

   ```sh
   playwright install
   ```

5. **Verify Playwright installation**
   ```sh
   python -c "import playwright; print(playwright.__version__)"
   ```

## Installing Playwright MCP (Model Context Protocol)

Playwright MCP enables AI assistants and LLMs to interact with web browsers through structured accessibility snapshots. It provides browser automation capabilities without requiring screenshots or vision models.

### What is Playwright MCP?

Playwright MCP is a Model Context Protocol server that provides:
- **Fast and lightweight** browser automation using accessibility trees
- **LLM-friendly** structured data instead of pixel-based input
- **Deterministic tool application** avoiding screenshot-based ambiguity
- Support for multiple browsers (Chrome, Firefox, WebKit)

### Installation Options

#### Option 1: Official Microsoft Playwright MCP

**For VS Code:**
```sh
# Install via VS Code CLI
code --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'

# For VS Code Insiders
code-insiders --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'
```

**For Cursor:**
1. Go to `Cursor Settings` → `MCP` → `Add new MCP Server`
2. Name: "playwright"
3. Command type: `npx @playwright/mcp@latest`

**For Claude Desktop:**
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**For Windsurf:**
Follow Windsurf MCP documentation with this configuration:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

#### Option 2: ExecuteAutomation Playwright MCP

**Installation via npm:**
```sh
npm install -g @executeautomation/playwright-mcp-server
```

**Installation via mcp-get:**
```sh
npx @michaellatman/mcp-get@latest install @executeautomation/playwright-mcp-server
```

**Installation via Smithery (for Claude Desktop):**
```sh
npx @smithery/cli install @executeautomation/playwright-mcp-server --client claude
```

**For VS Code:**
```sh
code --add-mcp '{"name":"playwright","command":"npx","args":["@executeautomation/playwright-mcp-server"]}'
```

**For Claude Desktop:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    }
  }
}
```

### Configuration Options

You can customize Playwright MCP behavior with command-line arguments:

**Run in headless mode:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headless"]
    }
  }
}
```

**Enable vision mode (screenshot-based):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--vision"]
    }
  }
}
```

**Specify browser:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser=firefox"]
    }
  }
}
```

**Run in isolated mode (no persistent profile):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--isolated"]
    }
  }
}
```

### Standalone Server Mode

For headless environments or remote access:

```sh
# Start server on specific port
npx @playwright/mcp@latest --port 8931
```

Then configure client to connect via URL:
```json
{
  "mcpServers": {
    "playwright": {
      "url": "http://localhost:8931/sse"
    }
  }
}
```

### Docker Installation

```json
{
  "mcpServers": {
    "playwright": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--init", "--pull=always", "mcr.microsoft.com/playwright/mcp"]
    }
  }
}
```

### Verification

After installation, restart your AI assistant/IDE completely. The Playwright MCP server should now be available and provide browser automation tools like:
- `browser_navigate` - Navigate to URLs
- `browser_snapshot` - Capture page accessibility tree
- `browser_click` - Click elements
- `browser_type` - Type text into fields
- `browser_screenshot` - Take screenshots
- And many more...

### User Data Directory

Playwright MCP stores browser profiles at:
- **Windows:** `%USERPROFILE%\AppData\Local\ms-playwright\mcp-{channel}-profile`
- **macOS:** `~/Library/Caches/ms-playwright/mcp-{channel}-profile`
- **Linux:** `~/.cache/ms-playwright/mcp-{channel}-profile`

Delete this directory to start with a fresh browser session.

## Running Tests

To execute your Playwright tests with pytest, run:

```sh
# To run functional tests:
pytest -v -s test_graphql/tests
# To run visual tests:
pytest e2e/ -v --headed

# Run a specific test
pytest tests/test_auth.py -k test_user_registration
pytest tests/test_auth.py -k test_user_login

# Run with more detailed output
pytest tests/test_auth.py -v

```

If you want to run Playwright tests in headed mode (with browser UI), use:

```sh
pytest --headed
```

For running tests in a specific browser, specify it as follows:

```sh
pytest --browser=chromium  # or firefox, webkit
```

## Environment Variables

To store authentication tokens and other secrets securely, create a `.env` file:

```ini
TOKEN=your_auth_token_here
```

Then, load environment variables in your test files using:

```python
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
```

## Debugging Tests

- Use `--slowmo` to slow down execution for debugging:
  ```sh
  pytest --headed --slowmo=500  # 500ms delay between steps
  ```
- Run tests in debug mode:
  ```sh
  pytest --headed --debug
  ```

## Generating Tests Automatically

Playwright can generate tests for you by recording actions:

```sh
playwright codegen example.com
```

This opens a browser where you can perform actions, and Playwright generates the corresponding test script.

## Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/en/latest/)

Happy Testing! 🚀
