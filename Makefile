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
	PYTHONPATH=src:$$PYTHONPATH uv run pytest

test-cov:  ## Run tests with coverage
	PYTHONPATH=src:$$PYTHONPATH uv run pytest --cov=src --cov-report=html --cov-report=term

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
	uv run python src/server.py

run-http:  ## Run the MCP server with HTTP transport
	uv run python src/server.py --transport http --port 8000

inspector:  ## Run with MCP Inspector
	npx @modelcontextprotocol/inspector uv run fastmcp run src/server.py

build:  ## Build distribution packages
	uv build

lock:  ## Update lock file
	uv lock

add:  ## Add a new dependency (usage: make add PACKAGE=package-name)
	uv add $(PACKAGE)

add-dev:  ## Add a new dev dependency (usage: make add-dev PACKAGE=package-name)
	uv add --dev $(PACKAGE)

consul-run:	## Run consul docker container
	-@docker stop consul-dev
	-@docker rm consul-dev
	docker run -d --name consul-dev -p 8500:8500 -p 8600:8600/udp hashicorp/consul:1.22 agent -dev -client=0.0.0.0 -ui

consul-stop: ## Stop consul docker container
	docker stop consul-dev
	docker rm consul-dev