# AI-Notebooks
**Jupyter Notebooks for AI Tutorials from Marktechpost**

[![Test Notebooks](https://github.com/ashleycribb/AI-Notebooks/actions/workflows/test.yml/badge.svg)](https://github.com/ashleycribb/AI-Notebooks/actions/workflows/test.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A curated collection of Jupyter notebooks implementing cutting-edge AI agents, frameworks, and data generation techniques. Each notebook includes comprehensive tutorials and practical implementations.

## 🚀 Quick Start

### Basic Setup
```bash
git clone https://github.com/ashleycribb/AI-Notebooks.git
cd AI-Notebooks
pip install -r requirements.txt
jupyter lab
```

### 🤖 Phase 1: AI Assistant Setup
```bash
# Set up AI-powered features
make setup-phase1

# Configure your API keys in .env file
cp .env.example .env
# Edit .env with your OpenAI, Anthropic, and Google API keys

# Try the AI Assistant demo
jupyter lab notebooks/ai_assistant_demo.ipynb

# Or start the web interface
make web-server
```

📖 **[Full Setup Guide](docs/SETUP.md)** | 🔧 **[Development Guide](docs/DEVELOPMENT.md)** | 🎮 **[AI Assistant Demo](notebooks/ai_assistant_demo.ipynb)**

## ✨ Features

### 🤖 Core Notebooks
- **AI Agent Implementations** - Practical examples of multi-agent systems
- **Framework Tutorials** - Hands-on guides for popular AI frameworks  
- **Data Generation Techniques** - Synthetic data creation methods

### 🚀 Phase 1: AI-Powered Enhancements
- **🎯 AI Assistant with Magic Commands** - Chat, generate, and analyze code with AI
  - `%ai_chat` - Ask questions about your code or concepts
  - `%ai_generate` - Generate code from natural language
  - `%%ai_code` - Explain, optimize, debug, or document code
- **🎮 Interactive Model Playground** - Compare different AI models side-by-side
  - Real-time model comparison
  - Cost tracking and usage analytics
  - Parameter tuning with sliders
- **🌐 Web Interface** - Modern browser-based notebook interaction
  - Enhanced notebook viewer
  - Interactive model playground
  - Real-time collaboration features

### 🛠️ Quality & Development
- **Ready-to-Run** - All notebooks tested and validated
- **Comprehensive Documentation** - Detailed setup and usage guides
- **Automated Testing** - CI/CD pipeline ensures quality
- **Development Tools** - Utilities for notebook management and validation

## 📚 Notebooks

### 🤖 AI Agents

| Notebook | Description | Tutorial |
|----------|-------------|----------|
| [Self-Improving Agent (Gemini)](notebooks/agents/self_improving_agent_gemini.ipynb) | Build a self-improving AI agent using Google's Gemini API with intelligent adaptation features | [Tutorial](https://www.marktechpost.com/2025/05/29/a-coding-guide-for-building-a-self-improving-ai-agent-using-googles-gemini-api-with-intelligent-adaptation-features/) |
| [Multi-Tool Agent (Claude)](notebooks/agents/multi_tool_agent_claude.ipynb) | Create a customizable multi-tool AI agent with LangGraph and Claude for dynamic agent creation | [Tutorial](https://www.marktechpost.com/2025/05/24/step-by-step-guide-to-build-a-customizable-multi-tool-ai-agent-with-langgraph-and-claude-for-dynamic-agent-creation/) |
| [Python Execution Agent](notebooks/agents/python_execution_agent.ipynb) | Build an AI agent with live Python execution and automated validation capabilities | [Tutorial](https://www.marktechpost.com/2025/05/25/a-coding-implementation-to-build-an-ai-agent-with-live-python-execution-and-automated-validation/) |
| [Agent Collaboration Framework](notebooks/agents/agent_collaboration_framework.ipynb) | Implement an Agent2Agent framework for collaborative and critique-driven AI problem solving | [Tutorial](https://www.marktechpost.com/2025/05/27/a-step-by-step-coding-implementation-of-an-agent2agent-framework-for-collaborative-and-critique-driven-ai-problem-solving-with-consensus-building/) |
| [AutoGen Round-Robin Workflow](notebooks/agents/autogen_round_robin_workflow.ipynb) | Craft advanced round-robin multi-agent workflows with Microsoft AutoGen | [Tutorial](https://www.marktechpost.com/2025/05/23/a-comprehensive-coding-guide-to-crafting-advanced-round-robin-multi-agent-workflows-with-microsoft-autogen/) |

### 🛠️ Frameworks

| Notebook | Description | Tutorial |
|----------|-------------|----------|
| [Lyzr Chatbot Framework](notebooks/frameworks/lyzr_chatbot_framework.ipynb) | Build interactive transcript and PDF analysis with Lyzr Chatbot Framework | [Tutorial](https://www.marktechpost.com/2025/05/27/a-coding-implementation-to-build-an-interactive-transcript-and-pdf-analysis-with-lyzr-chatbot-framework/) |

### 📊 Data Generation

| Notebook | Description | Tutorial |
|----------|-------------|----------|
| [Synthetic Data with SDV](notebooks/data-generation/synthetic_data_sdv.ipynb) | Create synthetic data using the Synthetic Data Vault (SDV) library | [Tutorial](https://www.marktechpost.com/2025/05/25/step-by-step-guide-to-creating-synthetic-data-using-the-synthetic-data-vault-sdv/) |

## 🔧 Features

- ✅ **Automated Testing**: All notebooks are validated for format and syntax
- 🔄 **Auto-Updates**: Dependabot keeps dependencies current
- 📁 **Organized Structure**: Notebooks categorized by type and functionality
- 🐍 **Local & Colab**: Works in both local Jupyter and Google Colab
- 📖 **Comprehensive Docs**: Setup guides and development documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original tutorials by [Marktechpost](https://www.marktechpost.com/)
- Community contributors and maintainers