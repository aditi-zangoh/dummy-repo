#!/usr/bin/env make

.PHONY: install test coverage lint clean sync

# Default target
all: install test

# Install dependencies
install:
	@export PATH="$$HOME/.local/bin:$$PATH" && uv sync

# Sync dependencies
sync:
	@export PATH="$$HOME/.local/bin:$$PATH" && uv sync

# Run tests
test:
	@export PATH="$$HOME/.local/bin:$$PATH" && uv run pytest

# Run tests with coverage
coverage:
	@export PATH="$$HOME/.local/bin:$$PATH" && uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90

# Run linting
lint:
	@echo "Linting not configured for this mixed project"

# Clean build artifacts
clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@rm -rf .coverage 2>/dev/null || true
