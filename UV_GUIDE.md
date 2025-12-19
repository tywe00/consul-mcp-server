# Using uv with this Project

This project uses [uv](https://github.com/astral-sh/uv) as its exclusive package manager for fast, reliable Python dependency management.

## Why uv?

- ⚡ **10-100x faster** than pip
- 🔒 **Reliable** - uses a lock file for reproducible installs
- 🎯 **All-in-one** - replaces pip, pip-tools, virtualenv, and more
- 🐍 **Python version management** - can install and manage Python versions
- 📦 **Modern** - built in Rust, follows best practices

## Quick Start

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip (one-time only)
pip install uv

# With pipx
pipx install uv

# With Homebrew
brew install uv
```

### Basic Commands

```bash
# Sync dependencies (creates venv automatically if needed)
uv sync

# Sync with all extras (dev, test, etc.)
uv sync --all-extras

# Run a command in the project environment
uv run python -m my_mcp_server.server
uv run pytest
uv run ruff check .

# Add a dependency
uv add requests

# Add a development dependency
uv add --dev pytest

# Remove a dependency
uv remove requests

# Update dependencies
uv lock --upgrade

# Update a specific package
uv lock --upgrade-package fastmcp
```

## Understanding uv.lock

The `uv.lock` file is automatically generated and contains:
- Exact versions of all dependencies
- Transitive dependencies (dependencies of dependencies)
- Checksums for security
- Platform-specific information

**Important:** Always commit `uv.lock` to version control!

This ensures:
- Everyone on your team gets identical dependencies
- CI/CD builds are reproducible
- You can roll back to working states

## Project Workflow

### Initial Setup

```bash
# Clone the project
git clone <your-repo>
cd my-mcp-server

# Sync dependencies (creates venv + installs everything)
uv sync --all-extras
```

That's it! uv automatically:
1. Creates a `.venv` directory
2. Installs the correct Python version (if using uv python)
3. Installs all dependencies from `uv.lock`
4. Installs your project in editable mode

### Daily Development

```bash
# Run the server
uv run python -m my_mcp_server.server

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

### Adding Dependencies

```bash
# Add a production dependency
uv add httpx

# This automatically:
# 1. Adds httpx to pyproject.toml
# 2. Resolves compatible versions
# 3. Updates uv.lock
# 4. Installs the package

# Add a dev dependency
uv add --dev mypy

# Add with version constraint
uv add 'fastmcp>=2.0.0'
```

### Updating Dependencies

```bash
# Update all dependencies to latest compatible versions
uv lock --upgrade

# Update a specific package
uv lock --upgrade-package fastmcp

# Then sync to install the updates
uv sync
```

## Advanced Features

### Python Version Management

```bash
# Install a specific Python version
uv python install 3.12

# Use a specific Python version for this project
uv python pin 3.12

# List available Python versions
uv python list
```

### Virtual Environment Management

```bash
# uv automatically creates .venv, but you can manage it:

# Create a new venv manually
uv venv

# Create with a specific Python version
uv venv --python 3.11

# Activate the venv (optional - uv run handles this)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Using Scripts

You can define scripts in `pyproject.toml`:

```toml
[project.scripts]
my-mcp-server = "my_mcp_server.server:main"
dev-server = "my_mcp_server.dev:run_dev"
```

Then run them with:

```bash
uv run my-mcp-server
uv run dev-server
```

### Working with Different Environments

```bash
# Install only production dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev

# Install all extras
uv sync --all-extras

# Install for a specific platform (useful for Docker)
uv sync --python-platform linux
```

## Comparison with pip

| Task | pip | uv |
|------|-----|-----|
| Install dependencies | `pip install -r requirements.txt` | `uv sync` |
| Add a package | `pip install requests` + manually edit requirements | `uv add requests` |
| Create venv | `python -m venv .venv` + `source .venv/bin/activate` | Automatic with `uv sync` |
| Lock dependencies | `pip freeze > requirements.txt` | Automatic with `uv.lock` |
| Run command in venv | `source .venv/bin/activate` then `python script.py` | `uv run python script.py` |
| Speed | Baseline | **10-100x faster** |

## CI/CD Integration

### GitHub Actions

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        
      - name: Set up Python
        run: uv python install
        
      - name: Install dependencies
        run: uv sync --all-extras
        
      - name: Run tests
        run: uv run pytest
```

### Docker

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "my_mcp_server.server"]
```

## Troubleshooting

### "uv: command not found"

```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (usually automatic, but if needed)
export PATH="$HOME/.cargo/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc
```

### "Package not found"

```bash
# Clear cache and retry
uv cache clean
uv sync --all-extras
```

### "Import error after uv sync"

```bash
# Make sure you're running with uv run
uv run python script.py

# Or activate the venv
source .venv/bin/activate  # Then run normally
```

### "Different results on different machines"

```bash
# Make sure uv.lock is committed and up to date
git add uv.lock
git commit -m "Update lock file"

# On other machine, use --frozen to ensure exact versions
uv sync --frozen --all-extras
```

## Best Practices

1. **Always commit `uv.lock`** - This ensures reproducible builds
2. **Use `uv run`** - Avoids needing to activate virtualenv
3. **Use `uv sync`** - Don't manually edit `uv.lock`
4. **Pin Python version** - Add `.python-version` file for consistency
5. **Use `--frozen` in CI** - Prevents unexpected changes
6. **Keep uv updated** - `uv self update`

## Learning More

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub](https://github.com/astral-sh/uv)
- [Announcement Blog Post](https://astral.sh/blog/uv)

## Migration from pip

If you're migrating from pip:

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Initialize uv (creates pyproject.toml if needed)
uv init

# 3. Add dependencies from requirements.txt
cat requirements.txt | xargs -I {} uv add {}

# 4. Add dev dependencies
cat requirements-dev.txt | xargs -I {} uv add --dev {}

# 5. Remove old files
rm requirements.txt requirements-dev.txt

# 6. Commit the new files
git add pyproject.toml uv.lock
git commit -m "Migrate to uv"
```

## Common Workflows

### Starting a new feature

```bash
# Make sure you're up to date
git pull
uv sync --all-extras

# Work on your feature
uv run pytest  # Test as you go

# Need a new dependency?
uv add new-package
```

### Code review checklist

- [ ] `uv.lock` is committed
- [ ] Tests pass: `uv run pytest`
- [ ] Linting passes: `uv run ruff check .`
- [ ] Types check: `uv run mypy src/`

### Preparing for deployment

```bash
# Update all dependencies
uv lock --upgrade
uv sync

# Run full test suite
uv run pytest --cov

# Build distribution
uv build

# Tag release
git tag v1.0.0
git push --tags
```
