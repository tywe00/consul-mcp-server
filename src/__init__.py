"""My MCP Server - A FastMCP server for experimentation and learning."""

__version__ = "0.1.0"

# Import server to create mcp instance
from .server import mcp

# Import tools, resources, and prompts to register them
from .tools import tools
from .resources import resources
from .prompts import prompts

__all__ = ["__version__", "mcp"]
