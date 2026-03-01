# Consul MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides AI assistants with tools to interact with [HashiCorp Consul](https://www.consul.io/). Built with [FastMCP](https://github.com/jlowin/fastmcp).

## Features

This MCP server exposes Consul's core functionality through three types of integrations:

### Tools
- **Service Management**: Register, deregister, and list services
- **Health Checks**: Query service health status and check details
- **Key-Value Store**: Get and put values in Consul's KV store
- **Service Mesh Intentions**: Create, list, get, and delete Connect intentions

### Resources
- `consul://services` - List all registered services
- `consul://service/{name}/health` - Get health status for a specific service
- `consul://kv/{key}` - Retrieve values from KV store
- `consul://intentions` - List all Connect intentions
- `consul://intention/{id}` - Get specific intention details

### Prompts
- `setup_consul_service` - Guided service registration
- `debug_service_health` - Service health troubleshooting
- `configure_intentions` - Service mesh intention configuration
- `optimize_kv_structure` - KV store organization recommendations

## Installation

### Prerequisites
- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended)
- Docker (for running Consul locally)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/tywe00/consul-mcp-server.git
cd consul-mcp-server

# Install dependencies
make sync
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
CONSUL_URL=http://localhost:8500
LOG_LEVEL=INFO
```

### Running Consul Locally

If you don't have Consul running, start it with Docker:

```bash
make consul-run
```

Access Consul UI at: http://localhost:8500/ui

To stop Consul:
```bash
make consul-stop
```

## Usage

### Running the Server

#### Stdio Transport (default)
```bash
make run
```

#### HTTP Transport
```bash
make run-http
```

#### With MCP Inspector (for testing)
```bash
make inspector
```

### Using with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "consul": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/consul-mcp-server",
        "run",
        "consul-mcp-server"
      ]
    }
  }
}
```

### Using with Other MCP Clients

This server implements the standard MCP protocol and works with any MCP-compatible client. Configure your client to connect via stdio or HTTP transport.

## Development

### Setup Development Environment

```bash
# Install with dev dependencies
make sync
```

### Available Commands

Run `make help` to see all available commands:

```bash
make help          # Show all available commands
make sync          # Install/update all dependencies
make install       # Install production dependencies only
make test          # Run tests
make test-cov      # Run tests with coverage report
make lint          # Check code quality
make format        # Auto-format code
make type-check    # Run type checker
make run           # Run the server (stdio transport)
make run-http      # Run the server (HTTP transport)
make inspector     # Run with MCP Inspector for testing
make consul-run    # Start Consul Docker container
make consul-stop   # Stop Consul Docker container
make clean         # Clean build artifacts and cache
make build         # Build distribution packages
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make type-check
```

### Project Structure

```
consul-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py           # Main server entry point
│   ├── mcp_instance.py     # FastMCP singleton instance
│   ├── tools/
│   │   └── tools.py        # Consul tool implementations
│   ├── resources/
│   │   └── resources.py    # Consul resource providers
│   └── prompts/
│       └── prompts.py      # AI assistant prompts
├── tests/
│   └── test_tools.py       # Tool tests
├── pyproject.toml          # Project configuration
├── fastmcp.json           # FastMCP configuration
└── README.md
```

## Available Tools

### Service Management

**list_services**
```python
# List all registered services
list_services(consul_url="http://localhost:8500")
```

**register_service**
```python
# Register a new service
register_service(
    id="web-1",
    name="web",
    address="10.0.0.1",
    port=8080,
    consul_url="http://localhost:8500"
)
```

**deregister_service**
```python
# Remove a service
deregister_service(id="web-1", consul_url="http://localhost:8500")
```

**get_service_health**
```python
# Check service health
get_service_health(service_name="web", consul_url="http://localhost:8500")
```

### Key-Value Store

**kv_put**
```python
# Store a value
kv_put(key="config/app/setting", value="production", consul_url="http://localhost:8500")
```

**kv_get**
```python
# Retrieve a value
kv_get(key="config/app/setting", consul_url="http://localhost:8500")
```

### Service Mesh Intentions

**list_intentions**
```python
# List all intentions
list_intentions(consul_url="http://localhost:8500")
```

**create_intention**
```python
# Create an intention
create_intention(
    source="web",
    destination="api",
    action="allow",
    consul_url="http://localhost:8500"
)
```

**get_intention**
```python
# Get specific intention
get_intention(intention_id="abc-123", consul_url="http://localhost:8500")
```

**delete_intention**
```python
# Delete an intention
delete_intention(intention_id="abc-123", consul_url="http://localhost:8500")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Integrates with [HashiCorp Consul](https://www.consul.io/)
- Implements the [Model Context Protocol](https://modelcontextprotocol.io)

## Support

- Report issues: [GitHub Issues](https://github.com/tywe00/consul-mcp-server/issues)
- Consul Documentation: https://www.consul.io/docs
- MCP Documentation: https://modelcontextprotocol.io
