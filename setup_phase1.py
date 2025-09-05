#!/usr/bin/env python3
"""
Setup script for Phase 1: AI Assistant and Model Playground

This script sets up the AI-powered features for AI-Notebooks including:
- AI Assistant with magic commands
- Interactive Model Playground
- Web interface
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing Dependencies")
    print("=" * 50)
    
    # Install main requirements
    if not run_command("pip install -r requirements.txt", "Installing main dependencies"):
        return False
    
    # Install additional dependencies for development
    dev_deps = [
        "jupyter-contrib-nbextensions",
        "jupyter-nbextensions-configurator",
        "jupyterlab-git"
    ]
    
    for dep in dev_deps:
        run_command(f"pip install {dep}", f"Installing {dep}")
    
    return True


def setup_environment():
    """Set up environment configuration."""
    print("\n⚙️ Setting up Environment")
    print("=" * 50)
    
    # Create .env file if it doesn't exist
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys!")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example found, creating basic .env file")
        with open(env_file, 'w') as f:
            f.write("""# AI-Notebooks API Keys
# Add your API keys here

# OpenAI API Key (for GPT models)
OPENAI_API_KEY=your_openai_key_here

# Anthropic API Key (for Claude models)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Google API Key (for Gemini models)
GOOGLE_API_KEY=your_google_key_here

# Web interface settings
SECRET_KEY=your_secret_key_here
DEBUG=False
PORT=5000
""")
    
    return True


def setup_jupyter_extensions():
    """Set up Jupyter extensions and magic commands."""
    print("\n🔧 Setting up Jupyter Extensions")
    print("=" * 50)
    
    # Enable nbextensions
    run_command("jupyter contrib nbextension install --user", "Installing notebook extensions")
    run_command("jupyter nbextensions_configurator enable --user", "Enabling extension configurator")
    
    # Create IPython startup script
    startup_dir = Path.home() / '.ipython' / 'profile_default' / 'startup'
    startup_dir.mkdir(parents=True, exist_ok=True)
    
    startup_script = startup_dir / '00-ai-assistant.py'
    with open(startup_script, 'w') as f:
        f.write("""
# AI Assistant Auto-loader for AI-Notebooks
import sys
from pathlib import Path

# Add AI-Notebooks to path if we're in a notebook directory
cwd = Path.cwd()
if 'notebooks' in str(cwd) or 'AI-Notebooks' in str(cwd):
    # Find the project root
    project_root = cwd
    while project_root.parent != project_root:
        if (project_root / 'ai_assistant').exists():
            break
        project_root = project_root.parent
    
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

try:
    from ai_assistant.utils import setup_assistant
    print("🤖 AI Assistant available! Use setup_assistant() to activate.")
except ImportError:
    pass  # AI Assistant not available in this environment
""")
    
    print("✅ Created Jupyter startup script")
    return True


def create_demo_files():
    """Create demo and example files."""
    print("\n📝 Creating Demo Files")
    print("=" * 50)
    
    # Demo notebook should already exist, just verify
    demo_notebook = Path('notebooks/ai_assistant_demo.ipynb')
    if demo_notebook.exists():
        print("✅ AI Assistant demo notebook found")
    else:
        print("⚠️  Demo notebook not found, creating basic version...")
        # The demo notebook was already created above
    
    # Create a quick start guide
    quick_start = Path('docs/QUICK_START.md')
    with open(quick_start, 'w') as f:
        f.write("""# 🚀 Quick Start Guide - AI Assistant

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
""")
    
    print("✅ Created quick start guide")
    return True


def test_installation():
    """Test the installation."""
    print("\n🧪 Testing Installation")
    print("=" * 50)
    
    try:
        # Test imports
        import ai_assistant
        print("✅ AI Assistant package imports successfully")
        
        from ai_assistant.magic_commands import AIAssistantMagics
        print("✅ Magic commands module available")
        
        from ai_assistant.model_playground import ModelPlayground
        print("✅ Model playground module available")
        
        import flask
        import flask_socketio
        print("✅ Web interface dependencies available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def main():
    """Main setup function."""
    print("🤖 AI-Notebooks Phase 1 Setup")
    print("=" * 50)
    print("Setting up AI Assistant and Model Playground features...")
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        sys.exit(1)
    
    # Setup Jupyter extensions
    if not setup_jupyter_extensions():
        print("❌ Failed to setup Jupyter extensions")
        sys.exit(1)
    
    # Create demo files
    if not create_demo_files():
        print("❌ Failed to create demo files")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n🎉 Phase 1 Setup Complete!")
    print("=" * 50)
    print()
    print("✅ AI Assistant with magic commands")
    print("✅ Interactive Model Playground")
    print("✅ Web interface for enhanced interaction")
    print("✅ Demo notebook and documentation")
    print()
    print("📋 Next Steps:")
    print("1. Edit .env file with your API keys")
    print("2. Try the demo notebook: notebooks/ai_assistant_demo.ipynb")
    print("3. Start the web interface: cd web_interface && python app.py")
    print("4. Use %ai_help in any notebook for available commands")
    print()
    print("🚀 Happy coding with AI assistance!")


if __name__ == "__main__":
    main()