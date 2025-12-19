# FastMCP Examples

Practical examples showing common patterns and use cases.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Working with Files](#working-with-files)
- [API Integration](#api-integration)
- [Database Operations](#database-operations)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)

## Basic Examples

### Simple Calculator Tool

```python
from my_mcp_server.server import mcp

@mcp.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression safely.
    
    Args:
        expression: Mathematical expression (e.g., "2 + 2", "3.5 * 4")
    
    Returns:
        Result of the calculation
    """
    try:
        # Use ast.literal_eval for safety instead of eval
        import ast
        import operator
        
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }
        
        def eval_expr(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            else:
                raise ValueError("Unsupported operation")
        
        return eval_expr(ast.parse(expression, mode='eval').body)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")
```

### String Manipulation Tool

```python
from typing import Literal

@mcp.tool()
def transform_text(
    text: str,
    operation: Literal["uppercase", "lowercase", "title", "reverse"]
) -> str:
    """Transform text using various operations.
    
    Args:
        text: Text to transform
        operation: Type of transformation to apply
    
    Returns:
        Transformed text
    """
    operations = {
        "uppercase": text.upper,
        "lowercase": text.lower,
        "title": text.title,
        "reverse": lambda: text[::-1],
    }
    
    return operations[operation]()
```

## Working with Files

### Safe File Reader Tool

```python
import os
from pathlib import Path

@mcp.tool()
def read_file(filepath: str, max_size_mb: float = 5.0) -> str:
    """Read a file safely with size limits.
    
    Args:
        filepath: Path to the file
        max_size_mb: Maximum file size in MB (default: 5MB)
    
    Returns:
        File contents
    """
    path = Path(filepath).resolve()
    
    # Security: Ensure path is within allowed directory
    allowed_dir = Path("/allowed/directory").resolve()
    if not str(path).startswith(str(allowed_dir)):
        raise ValueError("Access denied: File outside allowed directory")
    
    # Check file size
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(f"File too large: {size_mb:.2f}MB (max: {max_size_mb}MB)")
    
    # Read file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return f"[Binary file: {path.name}]"
```

### File Listing Resource

```python
@mcp.resource("files://{directory}/list")
def list_directory(directory: str) -> str:
    """List files in a directory.
    
    Args:
        directory: Directory path
    
    Returns:
        Formatted list of files
    """
    path = Path(directory).resolve()
    
    if not path.is_dir():
        return f"Not a directory: {directory}"
    
    files = []
    for item in sorted(path.iterdir()):
        size = item.stat().st_size
        type_str = "DIR" if item.is_dir() else "FILE"
        files.append(f"{type_str:4} {size:>10} {item.name}")
    
    return "\n".join(files)
```

## API Integration

### REST API Client Tool

```python
import httpx
from typing import Optional, Dict, Any

@mcp.tool()
async def api_request(
    url: str,
    method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
    timeout: float = 10.0
) -> str:
    """Make HTTP API requests.
    
    Args:
        url: API endpoint URL
        method: HTTP method
        headers: Optional request headers
        body: Optional request body (for POST/PUT)
        timeout: Request timeout in seconds
    
    Returns:
        Response body as string
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=body
            )
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"HTTP Error: {str(e)}"
```

### API Data Resource

```python
@mcp.resource("api://{service}/{endpoint}")
async def fetch_api_data(service: str, endpoint: str) -> str:
    """Fetch data from configured API services.
    
    Args:
        service: Service name (e.g., 'github', 'weather')
        endpoint: API endpoint path
    
    Returns:
        API response data
    """
    base_urls = {
        "github": "https://api.github.com",
        "weather": "https://api.weather.com",
    }
    
    base_url = base_urls.get(service)
    if not base_url:
        return f"Unknown service: {service}"
    
    url = f"{base_url}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

## Database Operations

### Database Query Tool (SQLite Example)

```python
import sqlite3
from typing import List, Dict, Any

@mcp.tool()
def query_database(
    query: str,
    params: Optional[List[Any]] = None
) -> List[Dict[str, Any]]:
    """Execute a SQL query safely.
    
    Args:
        query: SQL query (use ? for parameters)
        params: Query parameters
    
    Returns:
        Query results as list of dictionaries
    """
    # Only allow SELECT queries for safety
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
```

### Database Schema Resource

```python
@mcp.resource("db://{table}/schema")
def get_table_schema(table: str) -> str:
    """Get database table schema.
    
    Args:
        table: Table name
    
    Returns:
        Table schema information
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        # Get table info
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        schema = f"Table: {table}\n\nColumns:\n"
        for col in columns:
            schema += f"  {col[1]:20} {col[2]:10} {'NOT NULL' if col[3] else ''}\n"
        
        return schema
    finally:
        conn.close()
```

## Error Handling

### Tool with Comprehensive Error Handling

```python
from typing import Union

@mcp.tool()
def process_data(data: str, operation: str) -> Union[str, Dict[str, str]]:
    """Process data with comprehensive error handling.
    
    Args:
        data: Data to process
        operation: Operation to perform
    
    Returns:
        Processed result or error details
    """
    try:
        # Validate inputs
        if not data:
            raise ValueError("Data cannot be empty")
        
        if operation not in ["encode", "decode", "hash"]:
            raise ValueError(f"Unknown operation: {operation}")
        
        # Perform operation
        if operation == "encode":
            import base64
            result = base64.b64encode(data.encode()).decode()
        elif operation == "decode":
            import base64
            result = base64.b64decode(data).decode()
        elif operation == "hash":
            import hashlib
            result = hashlib.sha256(data.encode()).hexdigest()
        
        return result
        
    except ValueError as e:
        return {
            "error": "ValidationError",
            "message": str(e),
            "code": "INVALID_INPUT"
        }
    except Exception as e:
        return {
            "error": "ProcessingError",
            "message": str(e),
            "code": "PROCESSING_FAILED"
        }
```

## Advanced Patterns

### Stateful Tool with Context

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Session:
    """Session state storage."""
    history: List[str]
    context: Dict[str, Any]

# Simple in-memory storage (use Redis/database in production)
sessions: Dict[str, Session] = {}

@mcp.tool()
def chat_with_context(
    session_id: str,
    message: str,
    clear: bool = False
) -> Dict[str, Any]:
    """Chat tool that maintains conversation history.
    
    Args:
        session_id: Unique session identifier
        message: User message
        clear: Clear session history
    
    Returns:
        Response with conversation context
    """
    if clear:
        sessions[session_id] = Session(history=[], context={})
        return {"status": "Session cleared"}
    
    if session_id not in sessions:
        sessions[session_id] = Session(history=[], context={})
    
    session = sessions[session_id]
    session.history.append(message)
    
    # Process with context
    context_summary = f"Previous messages: {len(session.history)}"
    response = f"Processed: {message}"
    
    return {
        "response": response,
        "context": context_summary,
        "history_length": len(session.history)
    }
```

### Batch Processing Tool

```python
from typing import List
import asyncio

@mcp.tool()
async def batch_process(
    items: List[str],
    operation: str,
    batch_size: int = 10
) -> Dict[str, Any]:
    """Process items in batches for efficiency.
    
    Args:
        items: List of items to process
        operation: Operation to perform
        batch_size: Size of each batch
    
    Returns:
        Processing results
    """
    results = []
    errors = []
    
    # Process in batches
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        # Process batch concurrently
        tasks = [process_item(item, operation) for item in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for item, result in zip(batch, batch_results):
            if isinstance(result, Exception):
                errors.append({"item": item, "error": str(result)})
            else:
                results.append(result)
    
    return {
        "processed": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }

async def process_item(item: str, operation: str):
    """Process a single item."""
    await asyncio.sleep(0.1)  # Simulate processing
    return f"{operation}({item})"
```

### Resource with Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache for 5 minutes
@lru_cache(maxsize=100)
def _cached_fetch(key: str, timestamp: str) -> str:
    """Internal cached fetch function."""
    # Expensive operation here
    return f"Data for {key} at {timestamp}"

@mcp.resource("cached://{key}")
def cached_resource(key: str) -> str:
    """Resource with time-based caching.
    
    Args:
        key: Resource key
    
    Returns:
        Cached or fresh resource data
    """
    # Round to 5-minute intervals for caching
    now = datetime.now()
    cache_timestamp = now.replace(
        minute=now.minute // 5 * 5,
        second=0,
        microsecond=0
    ).isoformat()
    
    return _cached_fetch(key, cache_timestamp)
```

### Streaming Response Tool

```python
from typing import Generator

@mcp.tool()
def stream_large_data(source: str) -> Generator[str, None, None]:
    """Stream large data in chunks.
    
    Note: FastMCP handles generator functions automatically.
    
    Args:
        source: Data source identifier
    
    Yields:
        Data chunks
    """
    # Simulate streaming large dataset
    for i in range(100):
        yield f"Chunk {i}: Data from {source}\n"
```

## Testing Examples

### Testing Tools

```python
import pytest
from my_mcp_server.tools.example_tools import calculate

def test_calculate():
    """Test calculator tool."""
    assert calculate("2 + 2") == 4
    assert calculate("10 * 5") == 50
    
    with pytest.raises(ValueError):
        calculate("import os")  # Should reject dangerous code
```

### Testing with FastMCP Client

```python
import pytest
from fastmcp import Client
from my_mcp_server.server import mcp

@pytest.mark.asyncio
async def test_tool_integration():
    """Test tool through MCP client."""
    async with Client(mcp) as client:
        # List available tools
        tools = await client.list_tools()
        assert len(tools) > 0
        
        # Call a tool
        result = await client.call_tool("add_numbers", {"a": 5, "b": 3})
        assert result == 8
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=my_mcp_server --cov-report=html

# Run specific test
uv run pytest tests/test_tools.py::test_calculate

# Run with verbose output
uv run pytest -v
```

## Configuration Examples

### Environment-based Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

@mcp.tool()
def get_api_key(service: str) -> str:
    """Get API key for a service."""
    key = os.getenv(f"{service.upper()}_API_KEY")
    if not key:
        raise ValueError(f"No API key configured for {service}")
    return key
```

---

## Next Steps

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- See [QUICKSTART.md](QUICKSTART.md) for getting started
- Read [README.md](README.md) for full documentation
