"""
AI-Notebooks Research Module

Specialized AI assistance for academic researchers, including:
- Automated data analysis and visualization
- Research methodology guidance
- Academic writing assistance
- Literature review support
"""

from .academic_magic import AcademicResearchMagics
from .data_analyzer import ResearchDataAnalyzer
from .survey_analyzer import SurveyAnalyzer
from .writing_assistant import AcademicWritingAssistant

__all__ = [
    'AcademicResearchMagics',
    'ResearchDataAnalyzer', 
    'SurveyAnalyzer',
    'AcademicWritingAssistant'
]