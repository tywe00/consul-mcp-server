"""Common utility functions and helpers."""

from typing import Any, Dict
import json


def format_json(data: Dict[str, Any], indent: int = 2) -> str:
    """Format a dictionary as pretty-printed JSON.
    
    Args:
        data: Dictionary to format
        indent: Number of spaces for indentation
    
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=indent, sort_keys=True)


def validate_non_empty(value: str, field_name: str) -> str:
    """Validate that a string is not empty.
    
    Args:
        value: The string value to validate
        field_name: Name of the field for error messages
    
    Returns:
        The validated value
    
    Raises:
        ValueError: If the value is empty or whitespace
    """
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of the result
        suffix: Suffix to add when truncating
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
