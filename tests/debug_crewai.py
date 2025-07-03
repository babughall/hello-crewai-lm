#!/usr/bin/env python3
"""
CrewAI Integration Test

This test verifies that:
1. CrewAI can be properly imported and initialized
2. CrewAI can connect to LM Studio using the configured model
3. A simple agent and task can be executed successfully
4. Direct LLM calls work properly

Usage:
    python test_crewai_simple.py
    
The test uses the model configured in .env.toml under [settings.default_model].
Ensure LM Studio is running with the configured model loaded before running this test.
"""
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hello_crewai'))

from config_loader import get_model_config
from crewai import Agent, Task, Crew
from crewai.llm import LLM
import traceback

def test_crewai_with_debugging():
    """Test CrewAI with full error details"""
    
    try:
        # Get model config
        model_config = get_model_config()
        
        print(f"# Testing CrewAI with debugging...")
        print(f"Model: {model_config['name']}")
        print(f"Base URL: {model_config['base_url']}")
        print(f"API Key: {model_config['api_key']}")
        print()
        
        # Create LLM instance
        print("Creating LLM instance...")
        llm = LLM(
            model=f"openai/{model_config['name']}",
            api_key=model_config['api_key'],
            base_url=model_config['base_url'],
            timeout=60
        )
        print("LLM instance created")
        
        # Test LLM directly
        print("Testing LLM directly...")
        try:
            result = llm.call("Hello, say 'LLM test successful'")
            print(f"Direct LLM call successful: {result}")
        except Exception as e:
            print(f"Direct LLM call failed: {e}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            return False
        
        # Create agent
        print("Creating agent...")
        agent = Agent(
            role="Simple Agent",
            goal="Answer questions briefly",
            backstory="You are a helpful assistant.",
            llm=llm,
            verbose=True
        )
        print("Agent created")
        
        # Create task
        print("Creating task...")
        task = Task(
            description="Say hello and introduce yourself briefly.",
            expected_output="A brief hello message.",
            agent=agent
        )
        print("Task created")
        
        # Create crew
        print("Creating crew...")
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        print("Crew created")
        
        # Execute
        print("Executing crew...")
        result = crew.kickoff()
        print("Crew execution successful!")
        print(f"Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"CrewAI test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_crewai_with_debugging()
