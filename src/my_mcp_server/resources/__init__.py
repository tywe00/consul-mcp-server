"""Resources module for MCP server.

Resources expose data to LLMs without performing significant computation.
They are like GET endpoints in a REST API.
"""

# Import all resource modules to register them
from . import example_resources  # noqa: F401
