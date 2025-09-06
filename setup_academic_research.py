#!/usr/bin/env python3
"""
Setup script for Academic Research Features

This script sets up the academic research extensions for AI-Notebooks,
specifically designed for non-technical academic researchers.
"""

import os
import sys
import subprocess
from pathlib import Path


def install_academic_dependencies():
    """Install academic research specific dependencies."""
    print("📚 Installing Academic Research Dependencies")
    print("=" * 50)
    
    academic_deps = [
        # Core research libraries
        'sweetviz>=2.1.0',      # Automated EDA reports
        'scipy>=1.10.0',        # Statistical functions
        'plotly>=5.15.0',       # Interactive visualizations
        'statsmodels>=0.14.0',  # Advanced statistical models
        'scikit-learn>=1.3.0',  # Machine learning tools
        
        # Academic data access
        'arxiv>=1.4.0',         # arXiv paper access
        'biopython>=1.81',      # PubMed/NCBI access
        'wbdata>=0.3.0',        # World Bank data
        'requests>=2.28.0',     # API access
        
        # Text analysis for qualitative research
        'nltk>=3.8',            # Natural language processing
        'textblob>=0.17.0',     # Simple text processing
        
        # Survey research and psychometrics
        'factor-analyzer>=0.4.0',  # Factor analysis
        'pingouin>=0.5.0',      # Statistical functions
        
        # Optional advanced libraries
        'spacy>=3.4.0',         # Advanced NLP (optional)
        'lifelines>=0.27.0',    # Survival analysis (optional)
    ]
    
    for dep in academic_deps:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
    
    return True


def create_sample_data():
    """Create sample research datasets for demonstration."""
    print("\n📊 Creating Sample Research Datasets")
    print("=" * 50)
    
    import pandas as pd
    import numpy as np
    
    # Create sample datasets directory
    data_dir = Path('sample_data')
    data_dir.mkdir(exist_ok=True)
    
    # 1. Survey Research Dataset
    np.random.seed(42)
    n = 150
    
    survey_data = pd.DataFrame({
        'participant_id': range(1, n + 1),
        'age': np.random.normal(28, 8, n).astype(int),
        'gender': np.random.choice(['Male', 'Female', 'Other'], n, p=[0.45, 0.50, 0.05]),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n, p=[0.2, 0.4, 0.3, 0.1]),
        'job_satisfaction': np.random.normal(5.5, 1.3, n),
        'work_life_balance': np.random.normal(5.2, 1.4, n),
        'salary_satisfaction': np.random.normal(4.8, 1.5, n),
        'career_growth': np.random.normal(5.0, 1.2, n),
        'overall_happiness': np.random.normal(5.8, 1.1, n)
    })
    
    # Add some missing values
    missing_idx = np.random.choice(n, size=int(0.05 * n), replace=False)
    survey_data.loc[missing_idx, 'salary_satisfaction'] = np.nan
    
    survey_data.to_csv(data_dir / 'workplace_satisfaction_survey.csv', index=False)
    print("✅ Created workplace_satisfaction_survey.csv")
    
    # 2. Experimental Study Dataset
    np.random.seed(123)
    n_per_group = 40
    
    # Control group
    control = pd.DataFrame({
        'participant_id': range(1, n_per_group + 1),
        'group': 'Control',
        'pre_test': np.random.normal(72, 10, n_per_group),
        'post_test': np.random.normal(75, 12, n_per_group),
        'motivation': np.random.normal(6.0, 1.2, n_per_group),
        'engagement': np.random.normal(5.8, 1.3, n_per_group)
    })
    
    # Treatment group
    treatment = pd.DataFrame({
        'participant_id': range(n_per_group + 1, 2 * n_per_group + 1),
        'group': 'Treatment',
        'pre_test': np.random.normal(73, 9, n_per_group),
        'post_test': np.random.normal(83, 10, n_per_group),  # Higher scores
        'motivation': np.random.normal(7.2, 1.1, n_per_group),  # Higher motivation
        'engagement': np.random.normal(6.8, 1.2, n_per_group)   # Higher engagement
    })
    
    experimental_data = pd.concat([control, treatment], ignore_index=True)
    experimental_data.to_csv(data_dir / 'learning_intervention_study.csv', index=False)
    print("✅ Created learning_intervention_study.csv")
    
    # 3. Longitudinal Study Dataset
    np.random.seed(456)
    n_participants = 60
    n_timepoints = 4
    
    longitudinal_data = []
    for participant in range(1, n_participants + 1):
        baseline_score = np.random.normal(50, 10)
        for timepoint in range(1, n_timepoints + 1):
            # Simulate improvement over time with some noise
            score = baseline_score + (timepoint - 1) * 2 + np.random.normal(0, 3)
            longitudinal_data.append({
                'participant_id': participant,
                'timepoint': timepoint,
                'month': timepoint * 3,  # Every 3 months
                'wellbeing_score': score,
                'stress_level': np.random.normal(5 - timepoint * 0.3, 1.2),  # Decreasing stress
                'social_support': np.random.normal(4 + timepoint * 0.2, 1.0)  # Increasing support
            })
    
    longitudinal_df = pd.DataFrame(longitudinal_data)
    longitudinal_df.to_csv(data_dir / 'wellbeing_longitudinal_study.csv', index=False)
    print("✅ Created wellbeing_longitudinal_study.csv")
    
    print(f"\n📁 Sample datasets created in: {data_dir.absolute()}")
    return True


def create_academic_templates():
    """Create template notebooks for different research types."""
    print("\n📝 Creating Academic Research Templates")
    print("=" * 50)
    
    templates_dir = Path('notebooks/templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Survey Research Template
    survey_template = '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Survey Research Analysis Template\\n",
    "\\n",
    "This template guides you through analyzing survey data with AI assistance.\\n",
    "\\n",
    "## Research Question\\n",
    "**Replace with your research question:** What factors predict workplace satisfaction?\\n",
    "\\n",
    "## Dataset\\n",
    "**Replace with your CSV file:** workplace_satisfaction_survey.csv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Setup\\n",
    "%load_ext ai_assistant.research.academic_magic"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load your data\\n",
    "%research_load your_survey_data.csv --research_question \\"Your research question here\\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Explore and clean data\\n",
    "%research_eda\\n",
    "%research_clean --interactive"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Statistical analysis\\n",
    "%research_stats --variables \\"var1,var2,var3\\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Generate report\\n",
    "%research_report"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
'''
    
    with open(templates_dir / 'survey_research_template.ipynb', 'w') as f:
        f.write(survey_template)
    print("✅ Created survey_research_template.ipynb")
    
    return True


def main():
    """Main setup function for academic research features."""
    print("🎓 AI-Notebooks Academic Research Setup")
    print("=" * 50)
    print("Setting up specialized features for academic researchers...")
    print()
    
    # Install dependencies
    if not install_academic_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # Create sample data
    if not create_sample_data():
        print("❌ Failed to create sample data")
        return 1
    
    # Create templates
    if not create_academic_templates():
        print("❌ Failed to create templates")
        return 1
    
    print("\n🎉 Academic Research Setup Complete!")
    print("=" * 50)
    print()
    print("✅ Academic research magic commands")
    print("✅ Sample research datasets")
    print("✅ Research notebook templates")
    print("✅ SweetViz integration for automated EDA")
    print()
    print("📋 Next Steps:")
    print("1. Try the academic demo: jupyter lab notebooks/academic_research_demo.ipynb")
    print("2. Use sample data in sample_data/ directory")
    print("3. Start with templates in notebooks/templates/")
    print("4. Use %research_help in any notebook for commands")
    print()
    print("🎓 Perfect for non-technical academic researchers!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())