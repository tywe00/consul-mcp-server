# Dockerfile for FastMCP Server
# Uses uv for fast, reliable dependency management

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY src/ ./src/

# Install dependencies using uv
# The --system flag installs packages into the system Python
# rather than creating a virtual environment (appropriate for containers)
RUN uv sync --frozen --no-dev

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser

# Run the MCP server
# Note: MCP servers typically use stdio transport, so they don't expose ports
# The client connects via stdio, SSE, or other transports
CMD ["uv", "run", "python", "-m", "my_mcp_server.server"]

# If using SSE transport on a port:
# EXPOSE 8000
# CMD ["uv", "run", "fastmcp", "run", "--transport", "sse", "--port", "8000", "src/my_mcp_server/server.py"]
