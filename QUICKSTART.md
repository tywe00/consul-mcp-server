# FastMCP Quick Start Guide

This guide will get you up and running with your FastMCP server in 5 minutes.

## 0. Install uv (if needed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 1. Setup (1 minute)

```bash
# Sync dependencies (uv creates venv automatically)
uv sync --all-extras
```

## 2. Test the Server (1 minute)

```bash
# Run the server
uv run python -m my_mcp_server.server

# Or use make
make run
```

The server is now running and listening for MCP connections via stdio.

## 3. Test with MCP Inspector (2 minutes)

The MCP Inspector provides a web UI to test your server:

```bash
# Install and run inspector
npx @modelcontextprotocol/inspector uv run python -m my_mcp_server.server

# Or use make
make inspector
```

Open http://localhost:5173 in your browser. You'll see:
- **Tools**: Try `add_numbers` with parameters `{"a": 5, "b": 3}`
- **Resources**: Try `config://app` or `user://123/profile`
- **Prompts**: Try `analyze_code` with some sample code

## 4. Modify the Server (1 minute)

### Add a new tool:

Edit `src/my_mcp_server/tools/example_tools.py`:

```python
@mcp.tool()
def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y
```

Restart the server and test your new tool in the Inspector!

## 5. Next Steps

### Integrate with Claude Desktop

1. Edit your Claude Desktop config:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add your server:
```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/your/project",
        "python",
        "-m",
        "my_mcp_server.server"
      ]
    }
  }
}
```

3. Restart Claude Desktop

4. Start a new chat and your tools will be available!

### Development Tips

- **Run tests**: `uv run pytest` or `make test`
- **Format code**: `make format`
- **Type check**: `make type-check`
- **See all commands**: `make help`
- **Add dependencies**: `uv add package-name`
- **Add dev dependencies**: `uv add --dev package-name`

### Common Patterns

**Async tools** (for I/O operations):
```python
@mcp.tool()
async def fetch_data(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

**Dynamic resources** (with parameters):
```python
@mcp.resource("api://{endpoint}/data")
def get_api_data(endpoint: str) -> str:
    return f"Data from {endpoint}"
```

**Structured prompts** (multi-message):
```python
from fastmcp.prompts.base import UserMessage, AssistantMessage

@mcp.prompt()
def guided_analysis(topic: str) -> list:
    return [
        UserMessage(f"Let's analyze: {topic}"),
        AssistantMessage("I'll help you analyze that..."),
    ]
```

## Troubleshooting

**Import errors**: Make sure you ran `uv sync --all-extras`

**Server won't start**: Check that dependencies are synced with `uv sync`

**Changes not reflected**: Restart the server after code changes

**Inspector connection fails**: Make sure no other process is using port 5173

**uv not found**: Install uv first with the command from step 0

## Learn More

- [Full README](README.md) - Complete documentation
- [FastMCP Docs](https://gofastmcp.com/) - Official documentation
- [MCP Spec](https://modelcontextprotocol.io/) - Protocol specification
- [Examples](tests/) - Check out the test files for more examples

Happy coding! 🚀
