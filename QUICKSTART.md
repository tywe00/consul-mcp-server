# Quick Start Guide

Get up and running with Consul MCP Server in 5 minutes!

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) installed
- Docker (for running Consul locally)

## Step 1: Clone and Install

```bash
git clone https://github.com/yourusername/consul-mcp-server.git
cd consul-mcp-server
uv sync
```

## Step 2: Start Consul

```bash
make consul-run
```

Or manually:
```bash
docker run -d -p 8500:8500 --name=consul consul:latest agent -dev -ui -client=0.0.0.0
```

Verify Consul is running: http://localhost:8500/ui

## Step 3: Configure Environment

```bash
cp .env.example .env
```

The defaults should work for local development.

## Step 4: Run the Server

```bash
make run
```

Or:
```bash
consul-mcp-server
```

## Step 5: Test It Out

### Using MCP Inspector

```bash
make inspector
```

This opens the MCP Inspector where you can test tools interactively.

### Using Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "consul": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/consul-mcp-server",
        "run",
        "consul-mcp-server"
      ]
    }
  }
}
```

Restart Claude Desktop and try:
- "List all Consul services"
- "Register a new service called 'api' at 10.0.0.1:8080"
- "Check the health of the 'api' service"

## Common Commands

```bash
# Run tests
make test

# Format code
make format

# Lint code
make lint

# Stop Consul
make consul-stop

# Run with HTTP transport
make run-http
```

## Example Usage

Once connected to an MCP client, try these commands:

1. **List services:**
   ```
   Use the list_services tool
   ```

2. **Register a service:**
   ```
   Register a service with id="web-1", name="web", address="10.0.0.1", port=8080
   ```

3. **Store configuration:**
   ```
   Store the value "production" in the KV store with key "config/environment"
   ```

4. **Create service mesh intention:**
   ```
   Create an intention allowing traffic from "web" to "api"
   ```

## Troubleshooting

**Server won't start:**
- Check Python version: `python --version` (needs 3.10+)
- Verify installation: `uv sync`

**Can't connect to Consul:**
- Verify Consul is running: `docker ps | grep consul`
- Check Consul UI: http://localhost:8500/ui
- Verify CONSUL_URL in `.env`

**Tools not working:**
- Check Consul logs: `docker logs consul-dev`
- Verify network connectivity
- Try accessing Consul API directly: `curl http://localhost:8500/v1/catalog/services`

## Next Steps

- Read the full [README.md](README.md)
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore the [Consul documentation](https://www.consul.io/docs)
- Learn about [MCP](https://modelcontextprotocol.io)

## Need Help?

- Open an issue on GitHub
- Check Consul documentation
- Review the test files for usage examples
