"""Tests for tools."""

import pytest
from server import mcp


@pytest.mark.asyncio
async def test_list_services():
    """Test the list_services tool."""
    tool = mcp._tool_manager._tools['list_services']
    result = await tool.fn()
    assert isinstance(result, dict)

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


@pytest.mark.asyncio
async def test_get_service_health():
    """Test the get_service_health tool."""
    tool = mcp._tool_manager._tools['get_service_health']
    result = await tool.fn(service_name="test-service")
    assert "status" in result
    assert result["service_name"] == "test-service"
    assert result["status"] in ["success", "error", "not_found"]
    if result["status"] == "success":
        assert "healthy" in result
        assert "instance_count" in result
        assert "instances" in result
        assert isinstance(result["instances"], list)



async def test_kv_put():
    """Test the kv_put tool."""
    tool = mcp._tool_manager._tools['kv_put']
    result = await tool.fn(key="test/key", value="test-value")
    # Consul KV PUT returns a boolean (True on success)
    assert result is True


@pytest.mark.asyncio
async def test_kv_get():
    """Test the kv_get tool."""
    tool = mcp._tool_manager._tools['kv_get']
    result = await tool.fn(key="test/key")
    assert "status" in result
    assert result["key"] == "test/key"
    assert result["status"] in ["success", "error", "not_found"]
    if result["status"] == "success":
        assert "value" in result
        assert isinstance(result["value"], str)


@pytest.mark.asyncio
async def test_list_intentions():
    """Test the list_intentions tool."""
    tool = mcp._tool_manager._tools['list_intentions']
    result = await tool.fn()
    assert result is not None
    if isinstance(result, dict) and "status" in result:
        assert result["status"] in ["success", "error"]
    else:
        assert isinstance(result, (list, dict))


@pytest.mark.asyncio
async def test_create_intention():
    """Test the create_intention tool."""
    tool = mcp._tool_manager._tools['create_intention']
    result = await tool.fn(source="web", destination="db", action="allow")
    assert result is not None
    if isinstance(result, dict) and "status" in result:
        assert result["status"] in ["success", "error"]
        if result["status"] == "error":
            assert "source" in result
            assert "destination" in result
    else:
        assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_delete_intention():
    """Test the delete_intention tool."""
    tool = mcp._tool_manager._tools['delete_intention']
    result = await tool.fn(intention_id="test-intention-id")
    assert result is not None
    if isinstance(result, dict) and "status" in result:
        assert result["status"] in ["success", "error"]
        if result["status"] == "error":
            assert result["intention_id"] == "test-intention-id"
    else:
        assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_intention():
    """Test the get_intention tool."""
    tool = mcp._tool_manager._tools['get_intention']
    result = await tool.fn(intention_id="test-intention-id")
    assert result is not None
    assert isinstance(result, dict)
    if "status" in result:
        assert result["status"] in ["success", "error", "not_found"]
        assert result["intention_id"] == "test-intention-id"
