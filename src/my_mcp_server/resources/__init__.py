"""Resources module for MCP server.

Resources expose data to LLMs without performing significant computation.
They are like GET endpoints in a REST API.
"""

from . import example_resources

def register_all(mcp):
    """Register all resources with the MCP server."""
    example_resources.register_resources(mcp)

