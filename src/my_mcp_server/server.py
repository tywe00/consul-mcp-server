"""Main FastMCP server instance and configuration.

This is the central module that creates the FastMCP server instance
and imports all tools, resources, and prompts.
"""

from fastmcp import FastMCP

# Create the FastMCP server instance
# This is the shared instance that will be imported by tool/resource/prompt modules
mcp = FastMCP(
    name="My MCP Server",
    # Optional: specify dependencies needed for deployment
    # dependencies=["pandas", "requests"]
)


# Import all tools, resources, and prompts to register them with the server
# These imports must happen after server creation
from my_mcp_server.tools import example_tools  # noqa: F401, E402
from my_mcp_server.resources import example_resources  # noqa: F401, E402
from my_mcp_server.prompts import example_prompts  # noqa: F401, E402


def main() -> None:
    """Entry point for running the MCP server."""
    # Run the server using stdio transport (default)
    mcp.run()


if __name__ == "__main__":
    main()
