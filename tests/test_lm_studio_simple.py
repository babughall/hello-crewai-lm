#!/usr/bin/env python3
"""
LM Studio Connectivity Test

This test verifies that:
1. LM Studio is running and accessible on localhost:1234
2. The currently configured model is loaded and responding
3. Basic chat completions work with the selected model

Usage:
    python test_lm_studio_simple.py
    
The test uses the model configured in .env.toml under [settings.default_model].
"""

import sys
import os
import requests
import json

# Add src directory to path to import config_loader
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hello_crewai'))

try:
    from config_loader import get_model_config, get_current_model
except ImportError:
    print("* ERROR: Could not import config_loader. Make sure config_loader.py exists in src/hello_crewai/")
    sys.exit(1)

def test_lm_studio():
    print("- Testing LM Studio connection...")
    
    # Load configuration
    try:
        current_model_name = get_current_model()
        model_config = get_model_config(current_model_name)
        
        model_name = model_config['name']
        timeout = model_config['timeout']
        base_url = model_config['base_url']
        
        print(f"# Using model: {current_model_name} ({model_name})")
        print(f"# Timeout: {timeout}s")
        print(f"# Base URL: {base_url}")
        
    except Exception as e:
        print(f"* ERROR: Failed to load configuration: {e}")
        return False
    
    try:
        # Test if LM Studio is running
        health_url = f"{base_url}/models"
        response = requests.get(health_url, timeout=5)
        
        if response.status_code == 200:
            models = response.json()
            print("+ LM Studio is running!")
            print(f"+ Available models: {len(models.get('data', []))} model(s)")
            
            # Test a simple completion with the configured model
            completion_url = f"{base_url}/chat/completions"
            payload = {
                "model": model_name.replace("openai/", ""),  # Remove openai/ prefix for direct API call
                "messages": [
                    {"role": "user", "content": "Say hello in one sentence."}
                ],
                "max_tokens": 50,
                "temperature": 0.7
            }
            
            print(f"\n- Testing chat completion with {model_name}...")
            completion_response = requests.post(
                completion_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=timeout
            )
            
            if completion_response.status_code == 200:
                result = completion_response.json()
                message = result['choices'][0]['message']['content']
                print(f"+ LM Studio response: {message}")
                return True
            else:
                print(f"* ERROR: Completion failed: {completion_response.status_code}")
                print(f"* ERROR: {completion_response.text}")
                return False
                
        else:
            print(f"* ERROR: LM Studio not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"* ERROR: Error connecting to LM Studio: {e}")
        return False

if __name__ == "__main__":
    test_lm_studio()
