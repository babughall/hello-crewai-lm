#!/usr/bin/env python
"""
Model switcher utility for CrewAI
"""
import sys
import os
import toml
from pathlib import Path

# Add src directory to path to import config_loader
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hello_crewai'))

from config_loader import list_available_models, get_current_model

def switch_model(model_name: str):
    """Switch the default model in .env.toml"""
    
    config_file = Path(__file__).parent.parent / ".env.toml"
    if not config_file.exists():
        print("* ERROR: .env.toml not found!")
        return False
    
    # Load current config
    with open(config_file, 'r') as f:
        config = toml.load(f)
    
    # Check if model exists
    available_models = config.get("models", {})
    if model_name not in available_models:
        print(f"* ERROR: Model '{model_name}' not found!")
        print(f"Available models: {list(available_models.keys())}")
        return False
    
    # Update default model
    if "settings" not in config:
        config["settings"] = {}
    
    config["settings"]["default_model"] = model_name
    
    # Save config
    with open(config_file, 'w') as f:
        toml.dump(config, f)
    
    model_info = available_models[model_name]
    print(f"+ Switched to model: {model_name}")
    print(f"   Name: {model_info.get('name', 'N/A')}")
    print(f"   Description: {model_info.get('description', 'N/A')}")
    print(f"   Timeout: {model_info.get('timeout', 'N/A')}s")
    
    return True

def list_models():
    """List all available models with numbers"""
    
    try:
        models = list_available_models()
        current = get_current_model()
        
        print("# Available models:")
        print()
        
        model_list = list(models.items())
        for i, (model_name, description) in enumerate(model_list, 1):
            marker = ">" if model_name == current else " "
            print(f"{marker} {i}. {model_name}: {description}")
        
        print()
        print(f"Current default: {current}")
        return model_list
        
    except Exception as e:
        print(f"* ERROR: {e}")
        return []

def main():
    """Main CLI interface"""
    
    if len(sys.argv) == 1:
        print("# CrewAI Model Switcher")
        print()
        print("Usage:")
        print("  python switch_model.py list              - List available models")
        print("  python switch_model.py <number>          - Switch to model by number")
        print()
        list_models()
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_models()
    elif command in ["help", "--help", "-h"]:
        main()
    else:
        # Parse as number only
        try:
            model_number = int(command)
            model_list = list(list_available_models().items())
            
            if 1 <= model_number <= len(model_list):
                model_name = model_list[model_number - 1][0]  # Get model name from list
                if switch_model(model_name):
                    print()
                    print("> You can now run: uv run hello_crewai")
            else:
                print(f"* ERROR: Number must be between 1 and {len(model_list)}")
                print()
                list_models()
        except ValueError:
            print(f"* ERROR: '{command}' is not a valid number")
            print()
            list_models()

if __name__ == "__main__":
    main()
