"""consul-mcp-server - A FastMCP server for HashiCorp Consul integration."""

__version__ = "0.1.0"

# Import server to create mcp instance
# Import modules for side effects (decorator registration)
from .prompts import prompts  # noqa: F401
from .resources import resources  # noqa: F401
from .server import mcp
from .tools import tools  # noqa: F401

__all__ = ["__version__", "mcp"]
