# Makefile for AI-Notebooks project

.PHONY: help install install-dev clean test validate format lint setup-env setup-phase1 web-server

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  setup-phase1 - Set up Phase 1 features (AI Assistant + Model Playground)"
	@echo "  clean        - Clean notebooks (remove outputs)"
	@echo "  test         - Run tests"
	@echo "  validate     - Validate notebooks"
	@echo "  format       - Format code with black"
	@echo "  lint         - Run linting checks"
	@echo "  setup-env    - Set up development environment"
	@echo "  jupyter      - Start Jupyter Lab"
	@echo "  web-server   - Start web interface server"

# Installation
install:
	pip install -r requirements.txt

install-dev: install
	pip install pre-commit pytest black flake8
	pre-commit install

# Environment setup
setup-env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from template. Please edit it with your API keys."; \
	else \
		echo ".env file already exists"; \
	fi

# Notebook management
clean:
	python scripts/clean_notebooks.py notebooks/

validate:
	python scripts/validate_notebooks.py notebooks/

# Code quality
format:
	black scripts/ --line-length 88
	@echo "Code formatted with black"

lint:
	flake8 scripts/ --max-line-length=88
	@echo "Linting completed"

# Testing
test:
	pytest tests/ -v

# Phase 1 Setup
setup-phase1:
	python setup_phase1.py
	@echo "Phase 1 setup completed! Check the output above for next steps."

# Development
jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Web interface
web-server:
	cd web_interface && python app.py

# AI Assistant helpers
ai-demo:
	jupyter nbconvert --to notebook --execute notebooks/ai_assistant_demo.ipynb --output ai_assistant_demo_executed.ipynb
	@echo "AI Assistant demo executed successfully"

# CI/CD helpers
ci-test: validate
	@echo "CI tests completed"

# Clean up
clean-all: clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up Python cache files"