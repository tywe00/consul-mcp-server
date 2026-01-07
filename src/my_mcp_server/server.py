"""Main FastMCP server instance and configuration.

This is the central module that creates the FastMCP server instance
and imports all tools, resources, and prompts.
"""

from fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP(name="My MCP Server")

# Import tools to register them - must be after mcp creation
from . import tools  # noqa: F401, E402
from . import resources  # noqa: F401, E402

def main() -> None:
    """Entry point for running the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
