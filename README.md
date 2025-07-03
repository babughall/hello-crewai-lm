# HelloCrewai with LM Studio

Welcome to the HelloCrewai project with LM Studio integration. This CrewAI project is configured to work with local LLMs via LM Studio, allowing you to run AI agents locally without requiring external API services.

## Project Structure

```
hello_crewai/
├── .env.toml                # Model configuration (main config file)
├── src/hello_crewai/        # Main application code
│   ├── config_loader.py     # Configuration utilities
│   ├── crew.py             # Main CrewAI application
│   └── main.py             # Entry point
├── tests/                   # Test files
│   ├── test_lm_studio_simple.py   # LM Studio connectivity test
│   └── test_crewai_simple.py      # CrewAI integration test
├── scripts/                 # CLI utilities and scripts
│   └── switch_model.py      # Model switching utility
└── pyproject.toml          # Python project configuration
```

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

First, install uv if you haven't already:
```bash
pip install uv
```

Navigate to your project directory and install the dependencies:
```bash
uv sync
```

Copy the example configuration and customize it:
```bash
copy .env.toml.example .env.toml   # Windows
# or
cp .env.toml.example .env.toml     # macOS/Linux
```

Edit `.env.toml` to match your LM Studio model names and preferences.

## Requirements

Before running the project, ensure you have:

- **LM Studio** running on `localhost:1234` with models loaded
- **Python environment** with CrewAI and dependencies installed
- **Models configured** in `.env.toml` that match those loaded in LM Studio

## Usage

### Running Tests

Test LM Studio connectivity:
```bash
uv run python tests/test_lm_studio_simple.py
```

Test CrewAI integration:
```bash
uv run python tests/test_crewai_simple.py
```

### Model Management

List available models:
```bash
uv run python scripts/switch_model.py list
```

Switch to a different model by number:
```bash
uv run python scripts/switch_model.py 1   # Switch to first model
uv run python scripts/switch_model.py 2   # Switch to second model
```

### Running the Main Application

```bash
uv run hello_crewai
```

This will run the CrewAI crew using the currently configured model from `.env.toml`.

## Configuration

The project uses `.env.toml` for configuration management:

- **Model Settings**: Configure which model to use by default
- **LM Studio Settings**: Base URL and API key for LM Studio
- **Model Definitions**: Define available models with their parameters

Models can be easily switched using the CLI utility in `scripts/switch_model.py`.

## Understanding Your Crew

The hello_crewai Crew is composed of AI agents that work with your local LM Studio models. Each agent has unique roles, goals, and can collaborate on tasks while using your locally hosted language models.

## Support

For support, questions, or feedback:
- Visit the [CrewAI documentation](https://docs.crewai.com)
- Check the [CrewAI GitHub repository](https://github.com/joaomdmoura/crewai)
- Join the [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

Let's create wonders together with CrewAI and local LLMs!
