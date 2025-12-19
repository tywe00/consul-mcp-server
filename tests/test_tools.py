"""Tests for tools."""

import pytest
from my_mcp_server.tools.example_tools import (
    add_numbers,
    greet,
    process_list,
)


def test_add_numbers():
    """Test the add_numbers tool."""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0


def test_greet():
    """Test the greet tool."""
    # Test informal greeting
    result = greet("Alice", formal=False)
    assert "Alice" in result
    assert "Hey" in result
    
    # Test formal greeting
    result = greet("Bob", formal=True)
    assert "Bob" in result
    assert "Good day" in result


def test_process_list():
    """Test the process_list tool."""
    items = ["apple", "banana", "cherry"]
    
    # Test without prefix
    result = process_list(items)
    assert result == ["APPLE", "BANANA", "CHERRY"]
    
    # Test with prefix
    result = process_list(items, prefix="fruit: ")
    assert result == ["fruit: apple", "fruit: banana", "fruit: cherry"]


@pytest.mark.asyncio
async def test_fetch_data():
    """Test the async fetch_data tool."""
    from my_mcp_server.tools.example_tools import fetch_data
    
    result = await fetch_data("https://example.com")
    assert "example.com" in result
