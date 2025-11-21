# 🚀 Quick Start Guide - AI Assistant

## 1. Setup
```python
from ai_assistant.utils import setup_assistant
setup_assistant()
```

## 2. Basic Usage
```python
# Chat with AI
%ai_chat How do I use pandas for data analysis?

# Generate code
%ai_generate Create a function to read CSV files

# Analyze code
%%ai_code --action explain
def my_function():
    return "Hello World"
```

## 3. Model Playground
```python
from ai_assistant.model_playground import create_playground
playground = create_playground()
playground.display()
```

## 4. Web Interface
```bash
cd web_interface
python app.py
```

Visit http://localhost:5000 for the web interface.
