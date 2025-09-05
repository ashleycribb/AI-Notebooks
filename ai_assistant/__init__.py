"""
AI-Notebooks Assistant Package

This package provides AI-powered assistance for Jupyter notebooks including:
- Magic commands for code generation and explanation
- Interactive model playground
- Notebook enhancement utilities
"""

__version__ = "1.0.0"
__author__ = "AI-Notebooks Project"

from .magic_commands import AIAssistantMagics
from .model_playground import ModelPlayground
from .utils import setup_assistant

__all__ = ['AIAssistantMagics', 'ModelPlayground', 'setup_assistant']