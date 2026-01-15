"""Main FastMCP server instance and configuration."""

import sys
from pathlib import Path

# Add src to path if not already there
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import the singleton mcp instance
from my_mcp_server.mcp_instance import mcp

__all__ = ["mcp"]

def main() -> None:
    """Entry point for running the MCP server."""    
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
