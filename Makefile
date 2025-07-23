.PHONY: help install test lint format validate generate clean
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "NimbleTools Community MCP Registry Management"
	@echo "============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --all-extras

test: ## Run tests
	uv run pytest

lint: ## Run linting
	uv run ruff check .
	uv run mypy .

format: ## Format code
	uv run black .
	uv run ruff check --fix .

validate: ## Validate all server definitions
	uv run python tools/validate.py servers/

generate: ## Generate registry.yaml from server definitions
	uv run python tools/generate.py

check-servers: ## Check all servers for issues
	@echo "Checking server definitions..."
	@for server in servers/*/; do \
		if [ -f "$$server/server.yaml" ]; then \
			echo "✓ Checking $$server"; \
			uv run python tools/validate.py "$$server" || exit 1; \
		fi; \
	done
	@echo "All servers validated successfully!"

test-server: ## Test a specific server (usage: make test-server SERVER=echo)
	@if [ -z "$(SERVER)" ]; then \
		echo "Usage: make test-server SERVER=<server-name>"; \
		echo "Example: make test-server SERVER=echo"; \
		exit 1; \
	fi
	uv run python tools/test_server.py servers/$(SERVER)

test-servers: ## Test all servers with Docker
	uv run python tools/test_server.py --all

test-server-env: ## Test server with environment variables (usage: make test-server-env SERVER=finnhub ENV="FINNHUB_API_KEY=demo")
	@if [ -z "$(SERVER)" ]; then \
		echo "Usage: make test-server-env SERVER=<server-name> ENV=\"KEY=value\""; \
		echo "Example: make test-server-env SERVER=finnhub ENV=\"FINNHUB_API_KEY=demo\""; \
		exit 1; \
	fi
	uv run python tools/test_server.py servers/$(SERVER) --env "$(ENV)"

clean: ## Clean generated files and cache
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -f registry.yaml

dev-setup: install ## Set up development environment
	@echo "Development environment ready!"
	@echo "Run 'make help' to see available commands."