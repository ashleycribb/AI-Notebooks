"""
AI-powered magic commands for Jupyter notebooks.

This module provides IPython magic commands that integrate AI assistance
directly into notebook workflows.
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from IPython.display import display, HTML, Markdown, Javascript
import pandas as pd
import openai
import anthropic
import google.generativeai as genai
from ai_assistant.insight_assistant import InsightAssistant


@magics_class
class AIAssistantMagics(Magics):
    """AI-powered magic commands for notebook assistance."""
    
    def __init__(self, shell=None):
        super().__init__(shell)
        self.clients = {}
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize AI clients based on available API keys."""
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            self.clients['openai'] = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            self.clients['anthropic'] = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Google Gemini
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.clients['gemini'] = genai.GenerativeModel('gemini-pro')
    
    @line_magic
    @magic_arguments()
    @argument('--model', '-m', default='auto', help='AI model to use (openai, anthropic, gemini, auto)')
    @argument('--temperature', '-t', type=float, default=0.7, help='Temperature for generation')
    def ai_chat(self, line):
        """Chat with AI assistant about your notebook or code."""
        args = parse_argstring(self.ai_chat, line)
        
        if not line.strip():
            return self._show_help()
        
        prompt = line.split('--')[0].strip() if '--' in line else line.strip()
        
        try:
            response = self._get_ai_response(prompt, args.model, args.temperature)
            display(Markdown(f"**AI Assistant:** {response}"))
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error: {str(e)}</div>'))
    
    @cell_magic
    @magic_arguments()
    @argument('--model', '-m', default='auto', help='AI model to use')
    @argument('--action', '-a', default='explain', 
              choices=['explain', 'optimize', 'debug', 'document', 'test'],
              help='Action to perform on the code')
    def ai_code(self, line, cell):
        """Analyze, explain, or improve code using AI."""
        args = parse_argstring(self.ai_code, line)
        
        if not cell.strip():
            display(HTML('<div style="color: orange;">No code provided to analyze.</div>'))
            return
        
        action_prompts = {
            'explain': f"Explain this code step by step:\n\n```python\n{cell}\n```",
            'optimize': f"Suggest optimizations for this code:\n\n```python\n{cell}\n```",
            'debug': f"Help debug this code and identify potential issues:\n\n```python\n{cell}\n```",
            'document': f"Add comprehensive docstrings and comments to this code:\n\n```python\n{cell}\n```",
            'test': f"Generate unit tests for this code:\n\n```python\n{cell}\n```"
        }
        
        prompt = action_prompts[args.action]
        
        try:
            response = self._get_ai_response(prompt, args.model)
            display(Markdown(f"**AI {args.action.title()}:**\n\n{response}"))
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error: {str(e)}</div>'))
    
    @line_magic
    @magic_arguments()
    @argument('--model', '-m', default='auto', help='AI model to use')
    @argument('--language', '-l', default='python', help='Programming language')
    def ai_generate(self, line):
        """Generate code based on natural language description."""
        args = parse_argstring(self.ai_generate, line)
        
        if not line.strip():
            display(HTML('<div style="color: orange;">Please provide a description of what you want to generate.</div>'))
            return
        
        description = line.split('--')[0].strip() if '--' in line else line.strip()
        
        prompt = f"""Generate {args.language} code for the following requirement:

{description}

Please provide clean, well-commented code with proper error handling where appropriate."""
        
        try:
            response = self._get_ai_response(prompt, args.model)
            display(Markdown(f"**Generated Code:**\n\n{response}"))
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error: {str(e)}</div>'))
    
    @line_magic
    def ai_models(self, line):
        """List available AI models and their status."""
        status_html = "<h3>Available AI Models</h3><ul>"
        
        models_info = {
            'openai': ('OpenAI GPT', 'OPENAI_API_KEY'),
            'anthropic': ('Anthropic Claude', 'ANTHROPIC_API_KEY'),
            'gemini': ('Google Gemini', 'GOOGLE_API_KEY')
        }
        
        for model_key, (model_name, env_var) in models_info.items():
            status = "✅ Available" if model_key in self.clients else f"❌ Missing {env_var}"
            status_html += f"<li><strong>{model_name}</strong>: {status}</li>"
        
        status_html += "</ul>"
        
        if not self.clients:
            status_html += '<div style="color: orange; margin-top: 10px;">No AI models available. Please set up API keys in your .env file.</div>'
        
        display(HTML(status_html))
    
    @line_magic
    def ai_help(self, line):
        """Show help for AI assistant commands."""
        return self._show_help()

    @cell_magic
    @magic_arguments()
    @argument('--model', '-m', default='auto', help='AI model to use')
    def ai_insight(self, line, cell):
        """Generate insights and visualizations from a DataFrame."""
        args = parse_argstring(self.ai_insight, line)

        # Execute the cell to get the DataFrame
        try:
            df = self.shell.ex(cell)
            if not isinstance(df, pd.DataFrame):
                display(HTML('<div style="color: red;">Error: The output of the cell must be a pandas DataFrame.</div>'))
                return
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error executing cell: {e}</div>'))
            return

        # Create an InsightAssistant instance
        assistant = InsightAssistant()
        assistant.magics = self # Pass the initialized clients

        # Get and display insights
        with display(HTML("<div>Generating insights...</div>"), display_id=True) as handle:
            insights = assistant.get_insights(df, args.model)

            # Custom display logic with interactive buttons
            summary = insights.get('summary', 'No summary provided.')
            visualizations = insights.get('visualizations', [])

            html_output = f"<blockquote>{summary}</blockquote>"
            if visualizations:
                html_output += "<h4>Suggested Visualizations:</h4>"
                for i, code in enumerate(visualizations):
                    unique_id = f"btn_{i}_{os.urandom(4).hex()}"
                    html_output += f"""
                    <button id="{unique_id}">Generate Plot {i+1}</button>
                    <pre style="display: inline-block; margin-left: 10px;"><code>{code}</code></pre><br>
                    <script>
                        document.getElementById('{unique_id}').onclick = function() {{
                            var code = `{code.replace('`', '\\`')}`;
                            Jupyter.notebook.insert_cell_below('code').set_text(code);
                            Jupyter.notebook.select_next();
                            Jupyter.notebook.execute_cell();
                        }};
                    </script>
                    """
            handle.update(HTML(html_output))

    def _get_ai_response(self, prompt: str, model: str = 'auto', temperature: float = 0.7) -> str:
        """Get response from AI model."""
        if not self.clients:
            raise Exception("No AI models available. Please configure API keys.")
        
        # Auto-select model if not specified
        if model == 'auto':
            model = list(self.clients.keys())[0]
        
        if model not in self.clients:
            available = ', '.join(self.clients.keys())
            raise Exception(f"Model '{model}' not available. Available models: {available}")
        
        # Get response based on model type
        if model == 'openai':
            response = self.clients['openai'].chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        elif model == 'anthropic':
            response = self.clients['anthropic'].messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif model == 'gemini':
            response = self.clients['gemini'].generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=1000
                )
            )
            return response.text
        
        else:
            raise Exception(f"Unknown model: {model}")
    
    def _show_help(self):
        """Display help information for AI assistant."""
        help_html = """
        <div style="font-family: monospace; background: #f5f5f5; padding: 15px; border-radius: 5px;">
        <h3>🤖 AI Assistant Commands</h3>
        
        <h4>Chat Commands:</h4>
        <ul>
            <li><code>%ai_chat [question]</code> - Chat with AI about your notebook</li>
            <li><code>%ai_models</code> - List available AI models</li>
            <li><code>%ai_help</code> - Show this help</li>
        </ul>
        
        <h4>Code Analysis:</h4>
        <ul>
            <li><code>%%ai_code --action explain</code> - Explain code in cell</li>
            <li><code>%%ai_code --action optimize</code> - Suggest optimizations</li>
            <li><code>%%ai_code --action debug</code> - Help debug code</li>
            <li><code>%%ai_code --action document</code> - Add documentation</li>
            <li><code>%%ai_code --action test</code> - Generate unit tests</li>
        </ul>
        
        <h4>Code Generation:</h4>
        <ul>
            <li><code>%ai_generate [description]</code> - Generate code from description</li>
        </ul>

        <h4>Data Analysis:</h4>
        <ul>
            <li><code>%%ai_insight</code> - Generate insights and visualizations from a DataFrame</li>
        </ul>
        
        <h4>Options:</h4>
        <ul>
            <li><code>--model/-m</code> - Choose AI model (openai, anthropic, gemini, auto)</li>
            <li><code>--temperature/-t</code> - Set creativity level (0.0-1.0)</li>
            <li><code>--language/-l</code> - Programming language for generation</li>
        </ul>
        
        <h4>Examples:</h4>
        <pre>
%ai_chat How do I optimize this pandas dataframe operation?
%ai_generate --model openai Create a function to calculate fibonacci numbers
%%ai_code --action explain --model anthropic
def complex_function(data):
    return data.groupby('category').agg({'value': 'mean'})
        </pre>
        </div>
        """
        display(HTML(help_html))


def load_ipython_extension(ipython):
    """Load the AI assistant extension in IPython/Jupyter."""
    magics = AIAssistantMagics(ipython)
    ipython.register_magics(magics)
    
    print("🤖 AI Assistant loaded! Use %ai_help to get started.")


def unload_ipython_extension(ipython):
    """Unload the AI assistant extension."""
    pass