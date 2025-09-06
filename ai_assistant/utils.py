"""
Utility functions for the AI Assistant package.
"""

import os
import sys
from pathlib import Path
from IPython.display import display, HTML, Javascript
from IPython import get_ipython


def setup_assistant():
    """Set up the AI assistant in the current notebook environment."""
    # Add the ai_assistant package to Python path
    notebook_dir = Path.cwd()
    if str(notebook_dir) not in sys.path:
        sys.path.insert(0, str(notebook_dir))
    
    # Load the magic commands
    ipython = get_ipython()
    if ipython:
        try:
            ipython.magic('load_ext ai_assistant.magic_commands')
            display(HTML("""
            <div style="background: #e8f5e8; border: 1px solid #4caf50; border-radius: 5px; padding: 15px; margin: 10px 0;">
                <h3 style="color: #2e7d32; margin-top: 0;">🤖 AI Assistant Activated!</h3>
                <p>The AI Assistant is now ready to help you with your notebooks.</p>
                <p><strong>Quick Start:</strong></p>
                <ul>
                    <li><code>%ai_help</code> - Show all available commands</li>
                    <li><code>%ai_models</code> - Check available AI models</li>
                    <li><code>%ai_chat How do I use pandas?</code> - Ask questions</li>
                </ul>
                <p><em>Make sure your API keys are configured in the .env file!</em></p>
            </div>
            """))
        except Exception as e:
            display(HTML(f"""
            <div style="background: #ffebee; border: 1px solid #f44336; border-radius: 5px; padding: 15px; margin: 10px 0;">
                <h3 style="color: #c62828; margin-top: 0;">⚠️ Setup Error</h3>
                <p>Failed to load AI Assistant: {str(e)}</p>
                <p>Please ensure all dependencies are installed:</p>
                <code>pip install openai anthropic google-generativeai ipywidgets</code>
            </div>
            """))
    else:
        print("Warning: Not running in IPython/Jupyter environment")


def check_api_keys():
    """Check which API keys are configured."""
    keys_status = {
        'OpenAI': os.getenv('OPENAI_API_KEY') is not None,
        'Anthropic': os.getenv('ANTHROPIC_API_KEY') is not None,
        'Google': os.getenv('GOOGLE_API_KEY') is not None
    }
    
    html_content = "<h3>API Keys Status</h3><ul>"
    for service, available in keys_status.items():
        status = "✅ Configured" if available else "❌ Not configured"
        html_content += f"<li><strong>{service}</strong>: {status}</li>"
    html_content += "</ul>"
    
    if not any(keys_status.values()):
        html_content += """
        <div style="color: orange; margin-top: 10px;">
            <strong>No API keys found!</strong><br>
            Please add your API keys to the .env file:
            <pre>
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
            </pre>
        </div>
        """
    
    display(HTML(html_content))
    return keys_status


def create_demo_notebook():
    """Create a demo notebook showcasing AI Assistant features."""
    demo_content = '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🤖 AI Assistant Demo\\n",
    "\\n",
    "This notebook demonstrates the AI Assistant features for AI-Notebooks.\\n",
    "\\n",
    "## Setup\\n",
    "\\n",
    "First, let's set up the AI Assistant:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Setup AI Assistant\\n",
    "from ai_assistant.utils import setup_assistant\\n",
    "setup_assistant()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Check Available Models\\n",
    "\\n",
    "Let's see which AI models are available:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%ai_models"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Chat with AI\\n",
    "\\n",
    "Ask the AI assistant questions about your code or concepts:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%ai_chat What is the difference between supervised and unsupervised learning?"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Code Generation\\n",
    "\\n",
    "Generate code from natural language descriptions:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%ai_generate Create a function to calculate the mean and standard deviation of a list of numbers"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Code Analysis\\n",
    "\\n",
    "Analyze and explain existing code:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%ai_code --action explain\\n",
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "\\n",
    "def process_data(df):\\n",
    "    # Remove duplicates\\n",
    "    df_clean = df.drop_duplicates()\\n",
    "    \\n",
    "    # Fill missing values\\n",
    "    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns\\n",
    "    df_clean[numeric_columns] = df_clean[numeric_columns].fillna(df_clean[numeric_columns].mean())\\n",
    "    \\n",
    "    return df_clean"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Playground\\n",
    "\\n",
    "Use the interactive model playground to compare different AI models:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from ai_assistant.model_playground import create_playground\\n",
    "\\n",
    "playground = create_playground()\\n",
    "playground.display()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Help\\n",
    "\\n",
    "Get help on all available commands:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%ai_help"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
'''
    
    with open('notebooks/ai_assistant_demo.ipynb', 'w') as f:
        f.write(demo_content)
    
    print("✅ Demo notebook created: notebooks/ai_assistant_demo.ipynb")


def install_dependencies():
    """Install required dependencies for the AI Assistant."""
    import subprocess
    import sys
    
    dependencies = [
        'openai>=1.0.0',
        'anthropic>=0.7.0',
        'google-generativeai>=0.3.0',
        'ipywidgets>=8.0.0'
    ]
    
    print("Installing AI Assistant dependencies...")
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
    
    print("\\n🎉 Installation complete! Run setup_assistant() to get started.")


def get_notebook_context():
    """Get context about the current notebook for AI assistance."""
    ipython = get_ipython()
    if not ipython:
        return "Not running in IPython/Jupyter environment"
    
    # Get current cell content
    try:
        current_cell = ipython.get_parent()
        return f"Current notebook context available"
    except:
        return "Unable to get notebook context"


def create_startup_script():
    """Create a startup script to automatically load AI Assistant."""
    startup_content = '''
# AI Assistant Auto-loader
try:
    from ai_assistant.utils import setup_assistant
    setup_assistant()
except ImportError:
    print("AI Assistant not available. Run: pip install -r requirements.txt")
except Exception as e:
    print(f"AI Assistant setup failed: {e}")
'''
    
    # Create IPython startup directory if it doesn't exist
    startup_dir = Path.home() / '.ipython' / 'profile_default' / 'startup'
    startup_dir.mkdir(parents=True, exist_ok=True)
    
    startup_file = startup_dir / '00-ai-assistant.py'
    with open(startup_file, 'w') as f:
        f.write(startup_content)
    
    print(f"✅ Startup script created: {startup_file}")
    print("AI Assistant will now load automatically in new Jupyter sessions!")


if __name__ == "__main__":
    # Command line interface for utilities
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Assistant Utilities')
    parser.add_argument('--install', action='store_true', help='Install dependencies')
    parser.add_argument('--demo', action='store_true', help='Create demo notebook')
    parser.add_argument('--startup', action='store_true', help='Create startup script')
    parser.add_argument('--check-keys', action='store_true', help='Check API keys')
    
    args = parser.parse_args()
    
    if args.install:
        install_dependencies()
    elif args.demo:
        create_demo_notebook()
    elif args.startup:
        create_startup_script()
    elif args.check_keys:
        check_api_keys()
    else:
        print("Use --help to see available options")