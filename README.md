# CrewAI with LM Studio Integration

A CrewAI project configured to work seamlessly with LM Studio for local LLM inference. Features a simple CLI for switching between models and comprehensive tests for connectivity verification.

## Key Features

- **LM Studio Integration**: Direct connectivity to local LM Studio server
- **Model Switching CLI**: Number-based interface for quick model changes
- **Connectivity Tests**: Verify LM Studio connection and CrewAI integration
- **Configuration Management**: Simple .env.toml for model settings

## Quick Start

1. **Setup LM Studio**: Ensure LM Studio is running on `localhost:1234` with models loaded
2. **Install dependencies**: `uv sync`
3. **Configure models**: `cp .env.toml.example .env.toml` and edit model names
4. **Test connectivity**: `uv run python tests/test_lm_studio_simple.py`
5. **Switch models**: `uv run python scripts/switch_model.py 1`
6. **Run CrewAI**: `uv run hello_crewai`

## Model Switching CLI

The project includes a number-based CLI for easy model switching:

```bash
# List available models with numbers
uv run python scripts/switch_model.py list

# Switch to model by number (1, 2, etc.)
uv run python scripts/switch_model.py 1
uv run python scripts/switch_model.py 2
```

## Testing

Verify your setup with the included tests:

```bash
# Test LM Studio connectivity
uv run python tests/test_lm_studio_simple.py

# Test CrewAI integration
uv run python tests/test_crewai_simple.py
```

## Project Structure

```
hello_crewai/
├── .env.toml.example        # Configuration template
├── scripts/switch_model.py  # Model switching CLI
├── tests/                   # LM Studio & CrewAI tests
├── src/hello_crewai/        # Main application
└── pyproject.toml          # Dependencies
```

## Configuration

The project uses `.env.toml` for model configuration. Copy the example file and customize:

```bash
cp .env.toml.example .env.toml
```

Configure your LM Studio models and preferences in `.env.toml`.

## Requirements

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) package manager
- LM Studio running on `localhost:1234`

## Support

For support, questions, or feedback:
- Visit the [CrewAI documentation](https://docs.crewai.com)
- Check the [CrewAI GitHub repository](https://github.com/joaomdmoura/crewai)
- Join the [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

Let's create wonders together with CrewAI and local LLMs!
