"""Main FastMCP server instance and configuration.

This is the central module that creates the FastMCP server instance
and imports all tools, resources, and prompts.
"""

from fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP(name="My MCP Server")

# Import and register tools and resources - must be after mcp creation
from . import tools, resources
tools.register_all(mcp)
resources.register_all(mcp)

def main() -> None:
    """Entry point for running the MCP server."""
    import sys
    
    # Check for command line arguments
    transport = "stdio"
    port = 8000
    
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]
    
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    
    if transport == "http":
        mcp.run(transport="http", port=port)
    else:
        mcp.run()

if __name__ == "__main__":
    main()
