"""Tools module for MCP server.

Tools are functions that perform actions or computations.
They are like POST endpoints in a REST API.
"""

from . import example_tools

def register_all(mcp):
    """Register all tools with the MCP server."""
    example_tools.register_tools(mcp)

