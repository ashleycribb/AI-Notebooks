# Development Guide

This guide covers development workflows, tools, and best practices for the AI-Notebooks project.

## Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/ashleycribb/AI-Notebooks.git
cd AI-Notebooks
make setup-env  # Creates .env file from template
```

### 2. Install Dependencies

```bash
# Option 1: Using make
make install-dev

# Option 2: Manual installation
pip install -r requirements.txt
pip install pre-commit pytest black flake8
pre-commit install
```

### 3. Configure Environment

Edit the `.env` file with your API keys:

```bash
nano .env  # Add your actual API keys
```

## Development Workflow

### Daily Development

```bash
# Start Jupyter Lab
make jupyter

# Clean notebooks before committing
make clean

# Validate notebooks
make validate

# Format code
make format

# Run tests
make test
```

### Before Committing

```bash
# Clean and validate
make clean validate

# Format and lint
make format lint

# Run all checks
make ci-test
```

## Project Structure

```
AI-Notebooks/
├── notebooks/              # Organized notebook collection
│   ├── agents/             # AI agent implementations
│   ├── frameworks/         # Framework tutorials
│   └── data-generation/    # Data generation techniques
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── .github/                # GitHub Actions workflows
├── requirements.txt        # Python dependencies
├── environment.yml         # Conda environment
└── Makefile               # Development commands
```

## Notebook Standards

### File Organization

- **Naming**: Use descriptive, snake_case names
- **Location**: Place in appropriate category directory
- **Size**: Keep notebooks focused and manageable

### Code Quality

- **Clean Outputs**: Always remove outputs before committing
- **Documentation**: Include markdown cells explaining concepts
- **Error Handling**: Add try-catch blocks for API calls
- **Environment Checks**: Verify dependencies and API keys

### Template Usage

Use the [notebook template](NOTEBOOK_TEMPLATE.md) for consistency:

1. Header with description and requirements
2. Setup and installation
3. Configuration
4. Implementation sections
5. Testing and validation
6. Conclusion

## Utility Scripts

### Clean Notebooks

```bash
# Clean all notebooks
python scripts/clean_notebooks.py

# Clean specific notebook
python scripts/clean_notebooks.py notebooks/agents/example.ipynb

# Dry run (show what would be cleaned)
python scripts/clean_notebooks.py --dry-run
```

### Validate Notebooks

```bash
# Validate all notebooks
python scripts/validate_notebooks.py

# Validate with strict mode (exit with error if issues found)
python scripts/validate_notebooks.py --strict
```

## Testing

### Notebook Validation

The project includes automated testing for:

- JSON format validation
- Python syntax checking
- Import statement verification
- Best practices compliance

### Running Tests

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_notebooks.py -v

# Run with coverage
pytest --cov=scripts tests/
```

## Code Quality Tools

### Black (Code Formatting)

```bash
# Format all Python files
make format

# Format specific file
black scripts/clean_notebooks.py
```

### Flake8 (Linting)

```bash
# Lint all Python files
make lint

# Lint specific file
flake8 scripts/clean_notebooks.py
```

### Pre-commit Hooks

Pre-commit hooks automatically run on each commit:

- Notebook cleaning
- Code formatting
- Linting checks
- Basic validation

## Contributing Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow the notebook template
- Add comprehensive documentation
- Include error handling
- Test your implementation

### 3. Quality Checks

```bash
make clean validate format lint test
```

### 4. Commit Changes

```bash
git add .
git commit -m "Add: descriptive commit message"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
# Create pull request on GitHub
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   ```bash
   # Check .env file
   cat .env
   # Verify keys are loaded
   python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
   ```

3. **Jupyter Issues**
   ```bash
   # Restart kernel and clear outputs
   # Or use: make clean
   ```

4. **Git Pre-commit Issues**
   ```bash
   pre-commit uninstall
   pre-commit install
   ```

### Getting Help

- Check existing [Issues](https://github.com/ashleycribb/AI-Notebooks/issues)
- Review notebook documentation
- Consult original tutorial links
- Ask questions in discussions

## Release Process

1. Update version numbers
2. Run full test suite
3. Update CHANGELOG.md
4. Create release tag
5. Update documentation

## Performance Tips

- Use virtual environments
- Consider GPU acceleration for large models
- Monitor memory usage with large datasets
- Use Colab Pro for resource-intensive notebooks