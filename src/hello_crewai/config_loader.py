"""
Configuration loader for CrewAI models
"""
import os
import toml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = ".env.toml") -> Dict[str, Any]:
    """Load configuration from TOML file"""
    
    # Try to find config file in current directory or project root
    config_file = Path(config_path)
    if not config_file.exists():
        # Try in project root
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / config_path
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    return toml.load(config_file)

def get_model_config(model_name: str = None, config_path: str = ".env.toml") -> Dict[str, Any]:
    """Get configuration for a specific model"""
    
    config = load_config(config_path)
    
    # Use default model if none specified
    if model_name is None:
        model_name = config.get("settings", {}).get("default_model", "phi3-mini")
    
    # Get model configuration
    models = config.get("models", {})
    if model_name not in models:
        available_models = list(models.keys())
        raise ValueError(f"Model '{model_name}' not found. Available models: {available_models}")
    
    model_config = models[model_name].copy()
    
    # Add LM Studio settings
    lm_studio = config.get("lm_studio", {})
    model_config.update({
        "base_url": lm_studio.get("base_url", "http://localhost:1234/v1"),
        "api_key": lm_studio.get("api_key", "lm-studio")
    })
    
    return model_config

def list_available_models(config_path: str = ".env.toml") -> Dict[str, str]:
    """List all available models with their descriptions"""
    
    config = load_config(config_path)
    models = config.get("models", {})
    
    return {
        name: model_config.get("description", "No description")
        for name, model_config in models.items()
    }

def get_current_model(config_path: str = ".env.toml") -> str:
    """Get the current default model"""
    
    config = load_config(config_path)
    return config.get("settings", {}).get("default_model", "phi3-mini")
