#!/usr/bin/env python
"""
Model sync utility for CrewAI - automatically detect models from LM Studio
"""
import sys
import os
import toml
import requests
from pathlib import Path

# Add src directory to path to import config_loader
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hello_crewai'))

def get_lm_studio_models():
    """Get available models from LM Studio API"""
    
    config_file = Path(__file__).parent.parent / ".env.toml"
    if not config_file.exists():
        print("* ERROR: .env.toml not found!")
        return []
    
    # Load config to get LM Studio URL
    with open(config_file, 'r') as f:
        config = toml.load(f)
    
    base_url = config.get("lm_studio", {}).get("base_url", "http://localhost:1234/v1")
    
    try:
        # Query LM Studio for available models
        response = requests.get(f"{base_url}/models", timeout=10)
        response.raise_for_status()
        
        models_data = response.json()
        models = []
        
        for model in models_data.get("data", []):
            model_id = model.get("id", "")
            # Clean up the model ID for display
            clean_name = model_id.replace("openai/", "").replace("/", "-")
            models.append({
                "id": model_id,
                "clean_name": clean_name,
                "raw_data": model
            })
        
        return models
        
    except requests.exceptions.ConnectionError:
        print("* ERROR: Cannot connect to LM Studio. Is it running on localhost:1234?")
        return []
    except requests.exceptions.RequestException as e:
        print(f"* ERROR: Failed to get models from LM Studio: {e}")
        return []

def list_lm_studio_models():
    """List all models available in LM Studio"""
    
    print("# Models available in LM Studio:")
    print()
    
    models = get_lm_studio_models()
    
    if not models:
        print("No models found or LM Studio not accessible.")
        return
    
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model['clean_name']}")
        print(f"     ID: {model['id']}")
        print()

def sync_models_to_config():
    """Sync LM Studio models to .env.toml configuration"""
    
    config_file = Path(__file__).parent.parent / ".env.toml"
    
    # Load current config
    with open(config_file, 'r') as f:
        config = toml.load(f)
    
    # Get models from LM Studio
    lm_models = get_lm_studio_models()
    
    if not lm_models:
        print("No models to sync.")
        return
    
    print("# Syncing models from LM Studio to .env.toml...")
    print()
    
    # Keep existing models that are still available in LM Studio
    current_models = config.get("models", {})
    new_models = {}
    
    # Check which existing models are still available
    lm_model_ids = [m["id"] for m in lm_models]
    
    for model_key, model_config in current_models.items():
        model_name = model_config.get("name", "")
        if model_name in lm_model_ids:
            new_models[model_key] = model_config
            print(f"✓ Kept existing model: {model_key} ({model_name})")
        else:
            print(f"⚠ Removed model (not in LM Studio): {model_key} ({model_name})")
    
    # Add new models from LM Studio
    for lm_model in lm_models:
        model_id = lm_model["id"]
        clean_name = lm_model["clean_name"]
        
        # Check if this model is already configured
        already_exists = any(
            model_config.get("name") == model_id 
            for model_config in new_models.values()
        )
        
        if not already_exists:
            # Generate a unique key
            model_key = clean_name.lower().replace("-", "_").replace(".", "_")
            counter = 1
            original_key = model_key
            while model_key in new_models:
                model_key = f"{original_key}_{counter}"
                counter += 1
            
            new_models[model_key] = {
                "name": model_id,
                "timeout": 300,
                "description": f"Auto-detected: {clean_name}"
            }
            print(f"+ Added new model: {model_key} ({model_id})")
    
    # Update config
    config["models"] = new_models
    
    # Ensure default model is still valid
    default_model = config.get("settings", {}).get("default_model")
    if default_model and default_model not in new_models:
        # Set first available model as default
        if new_models:
            first_model = next(iter(new_models.keys()))
            config["settings"]["default_model"] = first_model
            print(f"! Updated default model to: {first_model}")
        else:
            print("! Warning: No models available, cleared default model")
            config["settings"]["default_model"] = ""
    
    # Save updated config
    with open(config_file, 'w') as f:
        toml.dump(config, f)
    
    print()
    print(f"✓ Configuration updated with {len(new_models)} models")

def print_help():
    """Print help information"""
    print("# LM Studio Model Sync Utility")
    print()
    print("Usage:")
    print("  python sync_models.py list    - List models available in LM Studio")
    print("  python sync_models.py sync    - Sync LM Studio models to .env.toml")
    print()

def main():
    """Main CLI interface"""
    
    if len(sys.argv) == 1:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_lm_studio_models()
    elif command == "sync":
        sync_models_to_config()
        print()
        print("You can now run:")
        print("  uv run python scripts/switch_model.py list")
    elif command in ["help", "--help", "-h"]:
        print_help()
    else:
        print(f"* ERROR: Unknown command '{command}'")
        print()
        print_help()

if __name__ == "__main__":
    main()
