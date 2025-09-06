# Setup Guide

## Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Anaconda or Miniconda for environment management

## Installation

### Option 1: Using pip

1. Clone the repository:
```bash
git clone https://github.com/ashleycribb/AI-Notebooks.git
cd AI-Notebooks
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Using conda

1. Clone the repository:
```bash
git clone https://github.com/ashleycribb/AI-Notebooks.git
cd AI-Notebooks
```

2. Create conda environment:
```bash
conda env create -f environment.yml
conda activate ai-notebooks
```

## Running Notebooks

### Local Jupyter

```bash
jupyter lab
# or
jupyter notebook
```

### Google Colab

Most notebooks are designed to work in Google Colab. Simply:

1. Open [Google Colab](https://colab.research.google.com/)
2. Upload the notebook file or connect to GitHub
3. Run the cells

## API Keys Setup

Many notebooks require API keys. Create a `.env` file in the project root:

```bash
# Copy the template
cp .env.example .env

# Edit with your API keys
nano .env  # or use your preferred editor
```

Required API keys:
- `OPENAI_API_KEY` - For OpenAI models
- `GOOGLE_API_KEY` - For Google Gemini
- `ANTHROPIC_API_KEY` - For Claude models

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've installed all dependencies
2. **API key errors**: Check your `.env` file and API key validity
3. **Memory issues**: Some notebooks require significant RAM; consider using Colab Pro

### Getting Help

- Check the [Issues](https://github.com/ashleycribb/AI-Notebooks/issues) page
- Review individual notebook documentation
- Refer to the original tutorial links in the README