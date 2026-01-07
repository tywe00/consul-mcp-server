"""Tests for tools."""

import pytest
from my_mcp_server.tools.example_tools import (
    add_numbers,
    greet,
    process_list,
    list_services
)

@pytest.mark.asyncio
async def test_list_services():
    """Test the list_services tool."""
    func = list_services.fn
    services = await func()
    assert isinstance(services, dict)
    assert len(services) >= 0  # Empty dict is valid if no services registered


def test_add_numbers():
    """Test the add_numbers tool."""
    func = add_numbers.fn
    assert func(2, 3) == 5
    assert func(-1, 1) == 0
    assert func(0, 0) == 0


def test_greet():
    """Test the greet tool."""
    func = greet.fn
    # Test informal greeting
    result = func("Alice", formal=False)
    assert "Alice" in result
    assert "Hey" in result
    
    # Test formal greeting
    result = func("Bob", formal=True)
    assert "Bob" in result
    assert "Good day" in result


def test_process_list():
    """Test the process_list tool."""
    func = process_list.fn
    items = ["apple", "banana", "cherry"]
    
    # Test without prefix
    result = func(items)
    assert result == ["APPLE", "BANANA", "CHERRY"]
    
    # Test with prefix
    result = func(items, prefix="fruit: ")
    assert result == ["fruit: apple", "fruit: banana", "fruit: cherry"]


@pytest.mark.asyncio
async def test_fetch_data():
    """Test the async fetch_data tool."""
    from my_mcp_server.tools.example_tools import fetch_data
    
    func = fetch_data.fn
    result = await func("https://example.com")
    assert "example.com" in result