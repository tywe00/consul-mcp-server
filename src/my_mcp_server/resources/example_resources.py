"""Example resources demonstrating different patterns.

Resources expose data to LLMs. They should be read-only and
not perform significant computation or have side effects.
"""

from my_mcp_server.server import mcp


# Static resource - returns the same data every time
@mcp.resource("config://app")
def get_app_config() -> str:
    """Get application configuration.
    
    Static resources use a simple URI without parameters.
    """
    return """
    App Configuration:
    - Version: 0.1.0
    - Environment: development
    - Debug: true
    """


# Dynamic resource (template) - uses parameters in the URI
@mcp.resource("user://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Get user profile information.
    
    Dynamic resources use URI templates with parameters in curly braces.
    FastMCP automatically handles these as MCP resource templates.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        User profile information
    """
    # In a real implementation, you would fetch from a database
    return f"""
    User Profile (ID: {user_id}):
    - Name: User {user_id}
    - Email: user{user_id}@example.com
    - Status: Active
    """


@mcp.resource("data://{category}/items")
def get_category_items(category: str) -> str:
    """Get items in a specific category.
    
    Another example of a dynamic resource.
    
    Args:
        category: The category name
    
    Returns:
        List of items in the category
    """
    # Placeholder data
    sample_items = {
        "fruits": ["apple", "banana", "orange"],
        "vegetables": ["carrot", "broccoli", "spinach"],
        "dairy": ["milk", "cheese", "yogurt"],
    }
    
    items = sample_items.get(category, [])
    if items:
        return f"Items in {category}:\n" + "\n".join(f"- {item}" for item in items)
    return f"No items found in category: {category}"


# Example of async resource (useful for I/O operations)
@mcp.resource("database://{table}/schema")
async def get_table_schema(table: str) -> str:
    """Get database table schema asynchronously.
    
    Async resources are useful for I/O-bound operations.
    
    Args:
        table: The table name
    
    Returns:
        Table schema information (placeholder)
    """
    # In a real implementation, you would query a database
    return f"""
    Schema for table '{table}':
    - id: INTEGER PRIMARY KEY
    - name: VARCHAR(255)
    - created_at: TIMESTAMP
    """
