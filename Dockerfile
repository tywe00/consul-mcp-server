# Multi-stage build for Consul MCP Server
FROM python:3.12-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files (README.md required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies to a virtual environment
RUN uv sync --frozen --no-dev

# Copy application source code
COPY src/ ./src/
COPY fastmcp.json ./

# Production stage - minimal runtime image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application files
COPY --from=builder /app/src /app/src
COPY --from=builder /app/fastmcp.json /app/fastmcp.json

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CONSUL_URL=http://localhost:8500 \
    LOG_LEVEL=INFO

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser

# Health check (optional, for container health monitoring)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port for HTTP transport (optional)
EXPOSE 8000

# Default to stdio transport
ENTRYPOINT ["python", "-m", "src.server"]

# Allow overriding transport via CMD
CMD []
