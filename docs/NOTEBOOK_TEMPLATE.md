# Notebook Template

This template provides a consistent structure for all notebooks in the AI-Notebooks repository.

## Standard Notebook Structure

### 1. Header Cell (Markdown)
```markdown
# [Notebook Title]

**Description**: Brief description of what this notebook demonstrates

**Tutorial**: [Link to original tutorial]

**Requirements**: 
- Python 3.8+
- API Keys: [List required API keys]

**Estimated Runtime**: [e.g., 5-10 minutes]

---
```

### 2. Setup and Installation (Code)
```python
# Install required packages (uncomment if running in Colab)
# !pip install package1 package2

# Import required libraries
import os
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Verify API keys (add checks for required keys)
required_keys = ['OPENAI_API_KEY', 'GOOGLE_API_KEY']  # Adjust as needed
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
    print("Please set these in your .env file or environment variables")
```

### 3. Configuration (Code)
```python
# Configuration parameters
CONFIG = {
    'model_name': 'gpt-4',
    'temperature': 0.7,
    'max_tokens': 1000,
    # Add other configuration parameters
}

print("Configuration loaded:")
for key, value in CONFIG.items():
    print(f"  {key}: {value}")
```

### 4. Main Implementation Sections

Each major section should have:

#### Section Header (Markdown)
```markdown
## [Section Number]. [Section Title]

Brief description of what this section covers.

### Key Concepts:
- Concept 1
- Concept 2
```

#### Implementation (Code)
```python
# Clear, well-commented code
def example_function():
    """
    Brief description of the function.
    
    Returns:
        Description of return value
    """
    pass

# Example usage
result = example_function()
print(f"Result: {result}")
```

### 5. Testing and Validation (Code)
```python
# Test the implementation
def test_implementation():
    """Test key functionality"""
    try:
        # Add test cases
        print("✅ All tests passed!")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

test_implementation()
```

### 6. Conclusion (Markdown)
```markdown
## Conclusion

Summary of what was accomplished:
- Key achievement 1
- Key achievement 2

### Next Steps:
- Suggested improvements
- Related notebooks to explore

### Resources:
- [Original Tutorial](link)
- [Documentation](link)
- [GitHub Repository](link)
```

## Best Practices

1. **Clear Documentation**: Every code cell should have comments explaining the logic
2. **Error Handling**: Include try-catch blocks for API calls and file operations
3. **Environment Checks**: Verify required dependencies and API keys
4. **Modular Code**: Break complex operations into functions
5. **Clean Outputs**: Remove all outputs before committing
6. **Local Compatibility**: Provide alternatives to Colab-specific code

## Example Colab Compatibility

```python
# Check if running in Colab
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    # Colab-specific setup
    from google.colab import files
    uploaded = files.upload()
else:
    # Local setup
    print("Running locally - using local file system")
```