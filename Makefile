.PHONY: help install sync test lint format type-check clean run inspector

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

sync:  ## Sync all dependencies (recommended)
	uv sync --all-extras

install:  ## Install production dependencies only
	uv sync

dev-install:  ## Install with development dependencies
	uv sync --all-extras

test:  ## Run tests
	uv run pytest

test-cov:  ## Run tests with coverage
	uv run pytest --cov=my_mcp_server --cov-report=html --cov-report=term

lint:  ## Run linter
	uv run ruff check .

format:  ## Format code
	uv run ruff format .

type-check:  ## Run type checker
	uv run mypy src/

clean:  ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .venv

run:  ## Run the MCP server
	uv run python -m my_mcp_server.server

inspector:  ## Run with MCP Inspector
	npx @modelcontextprotocol/inspector uv run python -m my_mcp_server.server

build:  ## Build distribution packages
	uv build

lock:  ## Update lock file
	uv lock

add:  ## Add a new dependency (usage: make add PACKAGE=package-name)
	uv add $(PACKAGE)

add-dev:  ## Add a new dev dependency (usage: make add-dev PACKAGE=package-name)
	uv add --dev $(PACKAGE)
