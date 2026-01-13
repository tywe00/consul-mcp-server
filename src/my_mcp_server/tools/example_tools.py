"""Example tools demonstrating different patterns.

Tools are functions that perform actions or computations.
They use type hints for automatic schema generation.
"""

from typing import List, Optional, Dict
import httpx

def register_tools(mcp):
    """Register all tools with the MCP server."""
    
    @mcp.tool()
    async def list_services(consul_url: str = "http://localhost:8500") -> Dict:
        """List all registered services in Consul"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{consul_url}/v1/catalog/services")
            return r.json()

    @mcp.tool()
    def add_numbers(a: int, b: int) -> int:
        """Add two numbers together.
        
        This is a simple example of a basic tool.
        The docstring becomes the tool's description.
        
        Args:
            a: First number to add
            b: Second number to add
        
        Returns:
            The sum of a and b
        """
        return a + b

    @mcp.tool()
    def greet(name: str, formal: bool = False) -> str:
        """Generate a greeting message.
        
        Demonstrates optional parameters with default values.
        
        Args:
            name: The name of the person to greet
            formal: Whether to use formal greeting (default: False)
        
        Returns:
            A greeting message
        """
        if formal:
            return f"Good day, {name}. How may I assist you?"
        return f"Hey {name}! What's up?"

    @mcp.tool()
    def process_list(items: List[str], prefix: Optional[str] = None) -> List[str]:
        """Process a list of items with an optional prefix.
        
        Demonstrates working with complex types like lists.
        
        Args:
            items: List of strings to process
            prefix: Optional prefix to add to each item
        
        Returns:
            Processed list of items
        """
        if prefix:
            return [f"{prefix}{item}" for item in items]
        return [item.upper() for item in items]

    @mcp.tool()
    async def fetch_data(url: str) -> str:
        """Fetch data from a URL asynchronously.
        
        This is a placeholder showing how to define async tools.
        Async tools are useful for I/O-bound operations.
        
        Args:
            url: The URL to fetch data from
        
        Returns:
            The fetched data (placeholder)
        """
        # In a real implementation, you would use httpx or aiohttp
        return f"Data from {url} (placeholder)"

