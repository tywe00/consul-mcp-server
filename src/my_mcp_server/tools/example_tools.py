"""Example tools demonstrating different patterns.

Tools are functions that perform actions or computations.
They use type hints for automatic schema generation.
"""

from typing import List, Optional, Dict
import httpx

def register_tools(mcp):
    """Register all tools with the MCP server."""
    
    @mcp.tool()
    async def list_services(consul_url: str = "http://localhost:8500") -> Dict:
        """List all registered services in Consul"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{consul_url}/v1/catalog/services")
            return r.json()

    @mcp.tool()
    async def register_service(id: str, name: str, address: str, port: int, consul_url: str = "http://localhost:8500") -> Dict:
        """Register a service in Consul"""
        try:
            service_data = {
                "ID": id,
                "Name": name,
                "Address": address,
                "Port": port, 
                "Check": {
                    "HTTP": f"http://{address}:{port}/health",
                    "Interval": "10s",
                    "Timeout": "1s"
                }
            }
            async with httpx.AsyncClient() as client:
                r = await client.put(f"{consul_url}/v1/agent/service/register", json=service_data)
                r.raise_for_status()
                return {
                    "status": "success",
                    "message": f"Service '{name}' registered successfully",
                    "service_id": id,
                    "http_status": r.status_code
                }
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "service_id": id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to register service: {str(e)}",
                "service_id": id
            }
    
    @mcp.tool()
    async def deregister_service(id: str, consul_url: str = "http://localhost:8500") -> Dict:
        """Deregister a service from Consul"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.put(f"{consul_url}/v1/agent/service/deregister/{id}")
                r.raise_for_status()
                return {
                    "status": "success",
                    "message": f"Service deregistered successfully",
                    "service_id": id,
                    "http_status": r.status_code
                }
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "service_id": id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to deregister service: {str(e)}",
                "service_id": id
            }

    @mcp.tool()
    async def get_service_health(service_name: str, consul_url: str = "http://localhost:8500") -> Dict:
        """Get health status of a service from Consul"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{consul_url}/v1/health/service/{service_name}")
                r.raise_for_status()
                health_data = r.json()
                
                if not health_data:
                    return {
                        "status": "not_found",
                        "message": f"Service '{service_name}' not found",
                        "service_name": service_name
                    }
                
                # Check if all instances are healthy
                all_healthy = all(
                    all(check.get("Status") == "passing" for check in instance.get("Checks", []))
                    for instance in health_data
                )
                
                return {
                    "status": "success",
                    "service_name": service_name,
                    "healthy": all_healthy,
                    "instance_count": len(health_data),
                    "instances": [
                        {
                            "id": inst["Service"]["ID"],
                            "address": inst["Service"]["Address"],
                            "port": inst["Service"]["Port"],
                            "checks": [
                                {"name": check["Name"], "status": check["Status"]}
                                for check in inst.get("Checks", [])
                            ]
                        }
                        for inst in health_data
                    ]
                }
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "service_name": service_name
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get service health: {str(e)}",
                "service_name": service_name
            }

    @mcp.tool()
    async def kv_put(key: str, value: str, consul_url: str = "http://localhost:8500") -> Dict:
        """Put a key-value pair in Consul KV store"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.put(f"{consul_url}/v1/kv/{key}", content=value)
                r.raise_for_status()
                return r.json()
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "key": key
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to store key: {str(e)}",
                "key": key
            }

    @mcp.tool()
    async def kv_get(key: str, consul_url: str = "http://localhost:8500") -> Dict:
        """Get a value from Consul KV store"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{consul_url}/v1/kv/{key}")
                r.raise_for_status()
                data = r.json()

                if not data:
                    return {
                        "status": "not_found",
                        "message": f"Key '{key}' not found",
                        "key": key
                    }

                # Consul returns base64 encoded value
                import base64
                value = base64.b64decode(data[0]["Value"]).decode("utf-8")

                return {
                    "status": "success",
                    "key": key,
                    "value": value
                }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "status": "not_found",
                    "message": f"Key '{key}' not found",
                    "key": key
                }
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "key": key
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get key: {str(e)}",
                "key": key
            }
    
    @mcp.tool()
    async def list_intentions(consul_url: str = "http://localhost:8500") -> Dict:
        """List all Connect intentions in Consul"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{consul_url}/v1/connect/intentions")
                r.raise_for_status()
                return r.json()
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get all intentions: {str(e)}"
            }
        
    @mcp.tool()
    async def create_intention(source: str, destination: str, action: str = "allow", consul_url: str = "http://localhost:8500") -> Dict:
        """Create a Connect intention in Consul"""
        try:
            intention_data = {
                "SourceName": source,
                "DestinationName": destination,
                "Action": action
            }
            async with httpx.AsyncClient() as client:
                r = await client.post(f"{consul_url}/v1/connect/intentions", json=intention_data)
                r.raise_for_status()
                return r.json()
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "source": source,
                "destination": destination
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create intention: {str(e)}",
                "source": source,
                "destination": destination
            }

    @mcp.tool()
    async def delete_intention(intention_id: str, consul_url: str = "http://localhost:8500") -> Dict:
        """Delete a Connect intention in Consul"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.delete(f"{consul_url}/v1/connect/intentions/{intention_id}")
                r.raise_for_status()
                return r.json()
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "intention_id": intention_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete intention: {str(e)}",
                "intention_id": intention_id

            }
        
    @mcp.tool()
    async def get_intention(intention_id: str, consul_url: str = "http://localhost:8500") -> Dict:
        """Get a specific Connect intention by ID in Consul"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{consul_url}/v1/connect/intentions/{intention_id}")
                r.raise_for_status()
                return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "status": "not_found",
                    "message": f"Intention '{intention_id}' not found",
                    "intention_id": intention_id
                }
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "intention_id": intention_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get intention: {str(e)}",
                "intention_id": intention_id
            }

    @mcp.tool()
    def add_numbers(a: int, b: int) -> int:
        """Add two numbers together.
        
        This is a simple example of a basic tool.
        The docstring becomes the tool's description.
        
        Args:
            a: First number to add
            b: Second number to add
        
        Returns:
            The sum of a and b
        """
        return a + b

    @mcp.tool()
    def greet(name: str, formal: bool = False) -> str:
        """Generate a greeting message.
        
        Demonstrates optional parameters with default values.
        
        Args:
            name: The name of the person to greet
            formal: Whether to use formal greeting (default: False)
        
        Returns:
            A greeting message
        """
        if formal:
            return f"Good day, {name}. How may I assist you?"
        return f"Hey {name}! What's up?"

    @mcp.tool()
    def process_list(items: List[str], prefix: Optional[str] = None) -> List[str]:
        """Process a list of items with an optional prefix.
        
        Demonstrates working with complex types like lists.
        
        Args:
            items: List of strings to process
            prefix: Optional prefix to add to each item
        
        Returns:
            Processed list of items
        """
        if prefix:
            return [f"{prefix}{item}" for item in items]
        return [item.upper() for item in items]

    @mcp.tool()
    async def fetch_data(url: str) -> str:
        """Fetch data from a URL asynchronously.
        
        This is a placeholder showing how to define async tools.
        Async tools are useful for I/O-bound operations.
        
        Args:
            url: The URL to fetch data from
        
        Returns:
            The fetched data (placeholder)
        """
        # In a real implementation, you would use httpx or aiohttp
        return f"Data from {url} (placeholder)"

