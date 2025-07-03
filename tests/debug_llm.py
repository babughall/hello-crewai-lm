#!/usr/bin/env python
"""
Debug LLM calls to understand what's failing
"""
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hello_crewai'))

from config_loader import get_model_config
from litellm import completion
import json

def test_direct_litellm():
    """Test direct LiteLLM call with our config"""
    
    # Load config
    model_config = get_model_config()
    
    print(f"# Testing direct LiteLLM call...")
    print(f"Model: {model_config['name']}")
    print(f"Base URL: {model_config['base_url']}")
    print()
    
    try:
        # Test simple completion
        response = completion(
            model=f"openai/{model_config['name']}",
            messages=[
                {"role": "user", "content": "Hello, please say 'test successful'"}
            ],
            api_base=model_config['base_url'],
            api_key=model_config['api_key'],
            timeout=30
        )
        
        print("+ Direct LiteLLM call successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"- Direct LiteLLM call failed: {e}")
        return False

def test_crewai_style_call():
    """Test a more complex call similar to what CrewAI might do"""
    
    model_config = get_model_config()
    
    print(f"# Testing CrewAI-style LiteLLM call...")
    print()
    
    try:
        # Test with a more complex prompt similar to what CrewAI uses
        response = completion(
            model=f"openai/{model_config['name']}",
            messages=[
                {"role": "system", "content": "You are an AI assistant. Answer concisely."},
                {"role": "user", "content": "Write a brief summary about AI LLMs in 2-3 sentences."}
            ],
            api_base=model_config['base_url'],
            api_key=model_config['api_key'],
            timeout=30,
            max_tokens=200,
            temperature=0.7
        )
        
        print("+ CrewAI-style LiteLLM call successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"- CrewAI-style LiteLLM call failed: {e}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code if hasattr(e.response, 'status_code') else 'N/A'}")
            try:
                print(f"Response body: {e.response.text if hasattr(e.response, 'text') else 'N/A'}")
            except:
                pass
        return False

if __name__ == "__main__":
    print("# LiteLLM Debug Tool")
    print()
    
    success1 = test_direct_litellm()
    print()
    success2 = test_crewai_style_call()
    
    print()
    if success1 and success2:
        print("+ All tests passed - LM Studio should work with CrewAI")
    else:
        print("- Some tests failed - this explains the CrewAI issues")
