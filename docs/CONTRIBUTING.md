# Contributing to AI-Notebooks

Thank you for your interest in contributing to AI-Notebooks! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/AI-Notebooks.git`
3. Set up development environment: `make install-dev`
4. Create a feature branch: `git checkout -b feature/your-feature`
5. Make your changes following our guidelines
6. Test your changes: `make ci-test`
7. Submit a pull request

## 📝 Types of Contributions

### 🆕 New Notebooks
- Implement tutorials from Marktechpost or similar sources
- Create original AI/ML educational content
- Add notebooks for new frameworks or techniques

### 🐛 Bug Fixes
- Fix errors in existing notebooks
- Correct documentation issues
- Resolve dependency conflicts

### 📚 Documentation
- Improve setup instructions
- Add missing documentation
- Create tutorial guides

### 🛠️ Infrastructure
- Improve CI/CD workflows
- Add development tools
- Enhance project structure

## 📋 Contribution Guidelines

### Notebook Standards

1. **Follow the Template**: Use our [notebook template](NOTEBOOK_TEMPLATE.md)
2. **Clear Documentation**: Include comprehensive markdown explanations
3. **Error Handling**: Add proper error handling for API calls
4. **Environment Compatibility**: Ensure notebooks work both locally and in Colab
5. **Clean Outputs**: Remove all outputs before committing

### Code Quality

1. **Python Standards**: Follow PEP 8 guidelines
2. **Comments**: Add clear, concise comments
3. **Functions**: Break complex code into reusable functions
4. **Dependencies**: Use the centralized requirements.txt

### File Organization

1. **Naming**: Use descriptive, snake_case names
2. **Location**: Place notebooks in appropriate category directories:
   - `notebooks/agents/` - AI agent implementations
   - `notebooks/frameworks/` - Framework tutorials  
   - `notebooks/data-generation/` - Data generation techniques
3. **Size**: Keep notebooks focused and manageable (< 50 cells typically)

## 🔧 Development Process

### Setting Up Your Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Notebooks.git
cd AI-Notebooks

# Set up development environment
make install-dev
make setup-env

# Edit .env with your API keys
nano .env
```

### Making Changes

```bash
# Create feature branch
git checkout -b feature/descriptive-name

# Make your changes
# ... edit files ...

# Test your changes
make clean validate format lint test

# Commit changes
git add .
git commit -m "Add: descriptive commit message"

# Push to your fork
git push origin feature/descriptive-name
```

### Commit Message Format

Use clear, descriptive commit messages:

```
Type: Brief description

Longer description if needed

- Bullet points for multiple changes
- Reference issues with #123
```

Types:
- `Add:` - New features or notebooks
- `Fix:` - Bug fixes
- `Update:` - Updates to existing content
- `Docs:` - Documentation changes
- `Refactor:` - Code restructuring
- `Test:` - Test additions or changes

## 🧪 Testing Your Changes

### Required Checks

Before submitting a PR, ensure all checks pass:

```bash
# Clean notebooks
make clean

# Validate notebooks
make validate

# Format code
make format

# Run linting
make lint

# Run tests
make test

# All-in-one CI check
make ci-test
```

### Manual Testing

1. **Notebook Execution**: Run your notebook end-to-end
2. **API Integration**: Test with actual API keys
3. **Error Scenarios**: Test error handling
4. **Documentation**: Verify all links and references work

## 📤 Submitting Pull Requests

### PR Checklist

- [ ] Code follows project standards
- [ ] Notebooks are clean (no outputs)
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New notebook
- [ ] Bug fix
- [ ] Documentation update
- [ ] Infrastructure improvement

## Testing
- [ ] Notebook runs end-to-end
- [ ] All automated tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Review Process

1. **Automated Checks**: GitHub Actions will run tests
2. **Code Review**: Maintainers will review your changes
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## 🎯 Contribution Ideas

### High Priority
- Add notebooks for new AI frameworks
- Improve error handling in existing notebooks
- Create local development alternatives to Colab-only code
- Add comprehensive testing for notebook functionality

### Medium Priority
- Enhance documentation with more examples
- Create video tutorials for complex notebooks
- Add performance optimization guides
- Implement notebook versioning system

### Low Priority
- Add more utility scripts
- Create notebook templates for specific use cases
- Improve CI/CD workflows
- Add internationalization support

## 🤝 Community Guidelines

### Be Respectful
- Use inclusive language
- Be constructive in feedback
- Help newcomers learn

### Be Collaborative
- Share knowledge and resources
- Credit original authors
- Contribute to discussions

### Be Professional
- Follow code of conduct
- Maintain high quality standards
- Respect intellectual property

## 🆘 Getting Help

### Resources
- [Setup Guide](SETUP.md)
- [Development Guide](DEVELOPMENT.md)
- [Notebook Template](NOTEBOOK_TEMPLATE.md)

### Support Channels
- [GitHub Issues](https://github.com/ashleycribb/AI-Notebooks/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/ashleycribb/AI-Notebooks/discussions) - Questions and general discussion
- [Original Tutorials](https://www.marktechpost.com/) - Reference material

### Common Questions

**Q: How do I add a new notebook category?**
A: Create a new directory under `notebooks/` and update the README structure.

**Q: Can I contribute notebooks from other sources?**
A: Yes, but ensure proper attribution and licensing compliance.

**Q: How do I handle large files or datasets?**
A: Use external storage (Google Drive, etc.) and provide download instructions.

**Q: What if my notebook requires expensive API calls?**
A: Provide mock data or free tier alternatives for testing.

## 📄 License

By contributing to AI-Notebooks, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors are recognized in:
- README.md acknowledgments
- Release notes
- Contributor graphs

Thank you for helping make AI-Notebooks better! 🎉