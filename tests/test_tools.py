"""Tests for tools."""

import pytest
from my_mcp_server.server import mcp


@pytest.mark.asyncio
async def test_list_services():
    """Test the list_services tool."""
    tool = mcp._tool_manager._tools['list_services']
    result = await tool.fn()
    assert isinstance(result, dict)


def test_add_numbers():
    """Test the add_numbers tool."""
    tool = mcp._tool_manager._tools['add_numbers']
    assert tool.fn(2, 3) == 5
    assert tool.fn(-1, 1) == 0
    assert tool.fn(0, 0) == 0


def test_greet():
    """Test the greet tool."""
    tool = mcp._tool_manager._tools['greet']
    # Test informal greeting
    result = tool.fn("Alice", formal=False)
    assert "Alice" in result
    assert "Hey" in result
    
    # Test formal greeting
    result = tool.fn("Bob", formal=True)
    assert "Bob" in result
    assert "Good day" in result


def test_process_list():
    """Test the process_list tool."""
    tool = mcp._tool_manager._tools['process_list']
    items = ["apple", "banana", "cherry"]
    
    # Test without prefix
    result = tool.fn(items)
    assert result == ["APPLE", "BANANA", "CHERRY"]
    
    # Test with prefix
    result = tool.fn(items, prefix="fruit: ")
    assert result == ["fruit: apple", "fruit: banana", "fruit: cherry"]


@pytest.mark.asyncio
async def test_fetch_data():
    """Test the async fetch_data tool."""
    tool = mcp._tool_manager._tools['fetch_data']
    result = await tool.fn("https://example.com")
    assert "example.com" in result


@pytest.mark.asyncio
async def test_register_service():
    """Test the register_service tool."""
    tool = mcp._tool_manager._tools['register_service']
    result = await tool.fn(
        id="test-service-1",
        name="test-service",
        address="127.0.0.1",
        port=8080
    )
    assert "status" in result
    assert result["service_id"] == "test-service-1"
    assert result["status"] in ["success", "error"]
    assert "message" in result
    if result["status"] == "success":
        assert result["http_status"] == 200
        assert "registered successfully" in result["message"]


@pytest.mark.asyncio
async def test_deregister_service():
    """Test the deregister_service tool."""
    tool = mcp._tool_manager._tools['deregister_service']
    result = await tool.fn(id="test-service-1")
    assert "status" in result
    assert result["service_id"] == "test-service-1"
    assert result["status"] in ["success", "error"]
    assert "message" in result
    if result["status"] == "success":
        assert result["http_status"] == 200
        assert "deregistered successfully" in result["message"]


