"""Example prompts demonstrating different patterns.

Prompts are reusable templates that help LLMs interact effectively
with your server. They can be simple strings or structured messages.
"""

from typing import List
from fastmcp.prompts import UserMessage, AssistantMessage
from my_mcp_server.server import mcp


@mcp.prompt()
def setup_consul_service(service_name: str) -> str:
    """Prompt for setting up a new Consul service.
    
    Args:
        service_name: Name of the service to set up
    
    Returns:
        A prompt for service setup guidance
    """
    return f"""Help me set up a new service '{service_name}' in Consul:

1. What service ID should I use?
2. What address and port should I configure?
3. Should I add any health checks?
4. Are there any best practices I should follow?

Please provide specific recommendations."""


@mcp.prompt()
def debug_service_health(service_name: str) -> List:
    """Prompt for debugging service health issues.
    
    Args:
        service_name: Name of the service with health issues
    
    Returns:
        A structured debugging prompt
    """
    return [
        UserMessage(content=f"Service '{service_name}' is showing health check failures."),
        UserMessage(content="Can you help me diagnose the issue?"),
        AssistantMessage(content="I'll help you debug the service health. Let me check the current status..."),
    ]


@mcp.prompt()
def configure_intentions(source: str, destination: str) -> str:
    """Prompt for configuring Consul Connect intentions.
    
    Args:
        source: Source service name
        destination: Destination service name
    
    Returns:
        A prompt for intention configuration
    """
    return f"""I need to configure service mesh intentions between '{source}' and '{destination}'.

Please help me:
1. Should I allow or deny this connection?
2. Are there security considerations?
3. What's the best practice for this service-to-service communication?
4. Should I add any additional intentions?"""


@mcp.prompt()
def optimize_kv_structure(prefix: str) -> str:
    """Prompt for optimizing Consul KV store structure.
    
    Args:
        prefix: KV prefix to optimize
    
    Returns:
        A prompt for KV optimization
    """
    return f"""Review my Consul KV store structure under '{prefix}' and suggest:

1. Better key naming conventions
2. Optimal hierarchy organization
3. Data that should be moved or consolidated
4. Security and access control recommendations"""