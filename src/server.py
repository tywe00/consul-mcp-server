"""Main FastMCP server instance and configuration."""

import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import mcp instance - handle both package and direct imports
try:
    from .mcp_instance import mcp
except ImportError:
    from mcp_instance import mcp  # type: ignore

# Import tools, resources, and prompts to register them (side effects)
try:
    from . import prompts, resources, tools  # noqa: F401
except ImportError:
    import prompts  # type: ignore # noqa: F401
    import resources  # type: ignore # noqa: F401
    import tools  # type: ignore # noqa: F401

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
