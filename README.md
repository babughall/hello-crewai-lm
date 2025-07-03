# CrewAI + LM Studio

CrewAI project that connects to LM Studio. Auto-detects your loaded models and provides CLI switching.

## Quick Start

1. Clone this repo: `git clone https://github.com/babughall/hello-crewai-lm.git`
2. Install dependencies: `cd hello-crewai-lm && uv sync`
3. Start LM Studio and download/load models you want to use
4. Start LM Studio server on `localhost:1234`
5. Setup config: `cp .env.toml.example .env.toml`
6. Sync models: `uv run python scripts/sync_models.py sync`
7. Run CrewAI: `uv run hello_crewai`

## Commands

```bash
# Switch models
uv run python scripts/switch_model.py list
uv run python scripts/switch_model.py 2

# Sync new models  
uv run python scripts/sync_models.py sync

# Test connection
uv run python tests/test_lm_studio_simple.py
```

## Configuration

### Auto-Sync (Recommended)
```bash
cp .env.toml.example .env.toml
uv run python scripts/sync_models.py sync
```

### Manual Setup
Edit `.env.toml` to add models:
```toml
[models.my-model]
name = "model-name-from-lm-studio"
timeout = 300
description = "Model description"
```

## Project Structure
```
hello_crewai/
├── .env.toml.example        # Config template
├── scripts/                 # CLI utilities  
├── tests/                   # Connectivity tests
├── src/hello_crewai/        # Main application
└── pyproject.toml          # Dependencies
```

## Requirements
- Python 3.10-3.13
- [UV package manager](https://docs.astral.sh/uv/)
- LM Studio running on `localhost:1234`

## Troubleshooting

**Installation issues:**
```bash
pip install uv && uv sync  # If uv not found
pip install -e .           # Fallback option
```

**Model sync issues:**
- Check LM Studio is running: `curl http://localhost:1234/v1/models`
- Manually edit `.env.toml` if auto-sync fails

## Support
- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
