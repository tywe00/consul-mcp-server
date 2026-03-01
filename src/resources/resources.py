"""Consul MCP resources for exposing services, health, KV store, and intentions as MCP resources."""

import json
import os

import httpx

# Handle both package and direct imports
try:
    from ..mcp_instance import mcp
except ImportError:
    from mcp_instance import mcp  # type: ignore

CONSUL_URL = os.getenv("CONSUL_URL", "http://localhost:8500")


@mcp.resource("consul://services")
async def get_consul_services() -> str:
    """Get all registered services from Consul."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{CONSUL_URL}/v1/catalog/services")
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"Error fetching services: {str(e)}"


@mcp.resource("consul://service/{service_name}/health")
async def get_service_health_resource(service_name: str) -> str:
    """Get health status of a specific service."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{CONSUL_URL}/v1/health/service/{service_name}")
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"Error fetching health for {service_name}: {str(e)}"


@mcp.resource("consul://kv/{key}")
async def get_kv_resource(key: str) -> str:
    """Get value from Consul KV store."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{CONSUL_URL}/v1/kv/{key}")
            if r.status_code == 404:
                return f"Key '{key}' not found"
            r.raise_for_status()
            data = r.json()
            if data:
                import base64

                return base64.b64decode(data[0]["Value"]).decode("utf-8")
            return f"Key '{key}' not found"
    except Exception as e:
        return f"Error fetching key {key}: {str(e)}"


@mcp.resource("consul://intentions")
async def get_intentions_resource() -> str:
    """Get all Connect intentions from Consul."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{CONSUL_URL}/v1/connect/intentions")
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"Error fetching intentions: {str(e)}"


@mcp.resource("consul://intention/{intention_id}")
async def get_intention_resource(intention_id: str) -> str:
    """Get a specific Connect intention by ID."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{CONSUL_URL}/v1/connect/intentions/{intention_id}")
            if r.status_code == 404:
                return f"Intention '{intention_id}' not found"
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"Error fetching intention {intention_id}: {str(e)}"
