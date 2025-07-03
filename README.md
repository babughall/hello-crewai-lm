# CrewAI with LM Studio Integration

A clean CrewAI project that connects seamlessly with LM Studio for local LLM inference. Features automatic model detection and simple CLI switching.

## Features

- **Auto-detect models** from LM Studio
- **Number-based CLI** for quick model switching  
- **Connectivity tests** to verify your setup
- **Git-friendly** configuration (personal configs stay local)

## Quick Start

1. **Start LM Studio** on `localhost:1234` with models loaded
2. **Install dependencies**: `uv sync`
3. **Setup config**: `cp .env.toml.example .env.toml`
4. **Sync models**: `uv run python scripts/sync_models.py sync`
5. **Run CrewAI**: `uv run hello_crewai`

## Usage

### Switch Models
```bash
# List available models
uv run python scripts/switch_model.py list

# Switch to model by number
uv run python scripts/switch_model.py 2
```

### Sync New Models
```bash
# Auto-detect from LM Studio
uv run python scripts/sync_models.py sync

# Or manually edit .env.toml
```

### Test Setup
```bash
# Test LM Studio connection
uv run python tests/test_lm_studio_simple.py

# Test CrewAI integration  
uv run python tests/test_crewai_simple.py
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
