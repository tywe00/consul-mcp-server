# Architecture Overview

## Project Structure

```
my-mcp-server/
│
├── src/my_mcp_server/          # Main package (source code)
│   ├── __init__.py             # Package initialization & exports
│   ├── server.py               # FastMCP server instance (central hub)
│   │
│   ├── tools/                  # Tools (Actions/Computations)
│   │   ├── __init__.py
│   │   └── example_tools.py    # @mcp.tool() decorated functions
│   │
│   ├── resources/              # Resources (Data exposure)
│   │   ├── __init__.py
│   │   └── example_resources.py # @mcp.resource() decorated functions
│   │
│   ├── prompts/                # Prompts (LLM interaction templates)
│   │   ├── __init__.py
│   │   └── example_prompts.py   # @mcp.prompt() decorated functions
│   │
│   └── utils/                  # Shared utilities
│       ├── __init__.py
│       └── helpers.py          # Common helper functions
│
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest configuration & fixtures
│   └── test_*.py               # Test modules
│
├── pyproject.toml              # Project metadata & dependencies
├── fastmcp.json                # FastMCP runtime configuration
├── Makefile                    # Development task automation
└── README.md                   # Documentation
```

## Component Relationships

```
┌─────────────────────────────────────────┐
│         MCP Client (Claude, etc)        │
└──────────────────┬──────────────────────┘
                   │ MCP Protocol
                   │ (stdio/SSE/HTTP)
                   ▼
┌─────────────────────────────────────────┐
│         FastMCP Server Instance         │
│              (server.py)                │
└──────────┬──────────┬──────────┬────────┘
           │          │          │
           ▼          ▼          ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Tools   │ │Resources │ │ Prompts  │
    │ Module   │ │  Module  │ │  Module  │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         └────────────┴────────────┘
                     │
                     ▼
              ┌────────────┐
              │   Utils    │
              │   Module   │
              └────────────┘
```

## Core Concepts

### 1. The Server Instance (`server.py`)

The heart of the application. This module:
- Creates the FastMCP server instance
- Imports all tools, resources, and prompts (registering them)
- Provides the entry point for running the server

```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

# Import modules to register decorated functions
from my_mcp_server.tools import example_tools
from my_mcp_server.resources import example_resources
from my_mcp_server.prompts import example_prompts
```

### 2. Tools (Actions)

Tools are functions that **perform actions** or **computations**. Think of them as:
- POST endpoints in a REST API
- Functions that produce side effects
- Operations that compute and return results

**Characteristics:**
- Decorated with `@mcp.tool()`
- Can be sync or async
- Type hints generate JSON schemas automatically
- Docstrings become tool descriptions

**Example:**
```python
@mcp.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)  # Simplified example
```

**Use cases:**
- Data processing
- API calls
- File operations
- Calculations
- Database queries

### 3. Resources (Data)

Resources **expose data** to LLMs. Think of them as:
- GET endpoints in a REST API
- Read-only data sources
- Context providers

**Characteristics:**
- Decorated with `@mcp.resource("uri://path")`
- Can be static (fixed URI) or dynamic (URI templates)
- Should be read-only (no side effects)
- Used to load information into LLM context

**Static Resource:**
```python
@mcp.resource("config://app")
def get_config() -> str:
    return "configuration data"
```

**Dynamic Resource (Template):**
```python
@mcp.resource("user://{user_id}/profile")
def get_user(user_id: str) -> str:
    return f"Profile data for user {user_id}"
```

**Use cases:**
- Configuration data
- User profiles
- Documentation
- Database records
- File contents

### 4. Prompts (Templates)

Prompts are **reusable interaction templates**. Think of them as:
- Best practices encoded in your server
- Structured conversation starters
- Guidance for how to use your tools

**Characteristics:**
- Decorated with `@mcp.prompt()`
- Return either strings or Message objects
- Can include multiple conversation turns
- Parameters allow customization

**Simple Prompt:**
```python
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n{code}"
```

**Structured Prompt:**
```python
@mcp.prompt()
def debug_help(error: str) -> list[Message]:
    return [
        UserMessage("I have an error"),
        UserMessage(error),
        AssistantMessage("Let me help debug that..."),
    ]
```

**Use cases:**
- Code review templates
- Analysis workflows
- Debugging guides
- Documentation generation

### 5. Utils (Helpers)

Shared functionality used across tools, resources, and prompts.

**Characteristics:**
- Pure functions (no decorators)
- Common utilities
- Business logic
- Validation helpers

## Data Flow

### Request Flow (Tool Execution)

```
1. Claude/Client sends tool call request
   ↓
2. FastMCP receives request via transport (stdio/SSE)
   ↓
3. FastMCP routes to correct tool function
   ↓
4. Tool function executes (may use utils)
   ↓
5. Return value serialized
   ↓
6. FastMCP sends response back to client
```

### Request Flow (Resource Access)

```
1. Claude/Client requests resource by URI
   ↓
2. FastMCP matches URI pattern
   ↓
3. Extracts parameters from URI
   ↓
4. Calls resource function with parameters
   ↓
5. Returns resource content to client
```

### Request Flow (Prompt Invocation)

```
1. User selects prompt in client UI
   ↓
2. Client requests prompt definition
   ↓
3. FastMCP returns prompt messages
   ↓
4. Client inserts messages into conversation
```

## Extension Points

### Adding New Functionality

1. **New Tool**: Create function in `tools/`, decorate with `@mcp.tool()`
2. **New Resource**: Create function in `resources/`, decorate with `@mcp.resource()`
3. **New Prompt**: Create function in `prompts/`, decorate with `@mcp.prompt()`
4. **New Utility**: Create function in `utils/` (no decorator)

### Best Practices

1. **Separation of Concerns**: Keep tools, resources, prompts in separate modules
2. **Type Hints**: Always use type hints for automatic schema generation
3. **Docstrings**: Write clear docstrings - they become user-facing descriptions
4. **Error Handling**: Use try-catch and return meaningful error messages
5. **Testing**: Write tests for all tools and resources
6. **Async**: Use async functions for I/O-bound operations

## Configuration

### Development vs Production

**Development:**
- Use stdio transport (default)
- Enable debug logging
- Use MCP Inspector for testing
- Use `uv run` for easy execution

**Production:**
- Consider SSE transport for web integration
- Implement proper authentication
- Add rate limiting
- Enable structured logging
- Use `uv.lock` for reproducible deployments

### Environment Variables

Use `.env` file for configuration:
- API keys
- Database URLs
- Feature flags
- Logging levels

uv automatically loads `.env` files when using `uv run`.

## Testing Strategy

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test with FastMCP client
3. **End-to-End**: Test with MCP Inspector

```python
# Unit test example
def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5

# Integration test example
@pytest.mark.asyncio
async def test_tool_via_mcp():
    from fastmcp import Client
    async with Client(mcp) as client:
        result = await client.call_tool("add_numbers", {"a": 2, "b": 3})
        assert result == 5
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=my_mcp_server

# Run specific test file
uv run pytest tests/test_tools.py

# Run with verbose output
uv run pytest -v
```

## Deployment Options

1. **Local Development**: Run via Python directly
2. **Claude Desktop**: Configure in `claude_desktop_config.json`
3. **Cursor/VSCode**: Use MCP extension
4. **FastMCP Cloud**: Deploy to cloud (requires configuration)
5. **Custom**: Any MCP-compatible client

## Security Considerations

1. **Input Validation**: Validate all tool inputs
2. **Path Traversal**: Prevent directory traversal in file operations
3. **Command Injection**: Sanitize inputs for shell commands
4. **Rate Limiting**: Implement rate limits for expensive operations
5. **Authentication**: Add auth if exposing sensitive data

## Performance Tips

1. **Async I/O**: Use async functions for I/O operations
2. **Caching**: Cache expensive computations
3. **Lazy Loading**: Load resources on demand
4. **Connection Pooling**: Reuse database connections
5. **Batch Operations**: Group multiple operations when possible

## Monitoring and Debugging

1. **Logging**: Use Python logging module
2. **MCP Inspector**: Visual debugging tool
3. **Error Messages**: Return clear, actionable errors
4. **Metrics**: Track tool usage and performance
5. **Health Checks**: Implement health check endpoints
