"""Pytest configuration and fixtures."""

import pytest
from my_mcp_server.server import mcp


@pytest.fixture
def mcp_server():
    """Provide the MCP server instance for testing."""
    return mcp


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "users": [
            {"id": "1", "name": "Alice"},
            {"id": "2", "name": "Bob"},
        ],
        "items": ["item1", "item2", "item3"],
    }
