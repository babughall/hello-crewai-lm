#!/usr/bin/env python3
"""
CrewAI Integration Test

This test verifies that:
1. CrewAI can be properly imported and initialized
2. CrewAI can connect to LM Studio using the configured model
3. A simple agent and task can be executed successfully

Usage:
    python test_crewai_simple.py
    
The test uses the model configured in .env.toml under [settings.default_model].
Ensure LM Studio is running with the configured model loaded before running this test.
"""

import os
import sys

# Add src directory to path to import config_loader
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hello_crewai'))

try:
    from config_loader import get_model_config, get_current_model
except ImportError:
    print("* ERROR: Could not import config_loader. Make sure config_loader.py exists in src/hello_crewai/")
    sys.exit(1)

# Load configuration and set environment variables
try:
    current_model_name = get_current_model()
    config = get_model_config(current_model_name)
    
    os.environ['OPENAI_API_KEY'] = config['api_key']
    os.environ['OPENAI_BASE_URL'] = config['base_url']
    
    print(f"# Using model: {current_model_name} ({config['name']})")
    print(f"# Timeout: {config['timeout']}s")
    print(f"# Base URL: {config['base_url']}")
    
except Exception as e:
    print(f"* ERROR: Failed to load configuration: {e}")
    sys.exit(1)

try:
    from crewai import Agent, Task, Crew, LLM
    print("+ CrewAI imports successful")
except ImportError as e:
    print(f"* ERROR: Failed to import CrewAI: {e}")
    sys.exit(1)

def test_crewai_with_lm_studio():
    print("\n- Testing CrewAI with LM Studio...")
    
    try:
        # Create LLM instance using configuration
        llm = LLM(
            model=config['name'],
            base_url=config['base_url'],
            api_key=config['api_key'],
            timeout=config['timeout']
        )
        print("+ LLM instance created")
        
        # Create a simple agent
        agent = Agent(
            role='Test Agent',
            goal='Answer simple questions',
            backstory='You are a helpful test agent.',
            llm=llm,
            verbose=True
        )
        print("+ Agent created")
        
        # Create a simple task
        task = Task(
            description='Say hello and introduce yourself in one sentence.',
            expected_output='A friendly greeting and introduction.',
            agent=agent
        )
        print("+ Task created")
        
        # Create crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        print("+ Crew created")
        
        # Execute the crew
        print("\n> Executing crew...")
        result = crew.kickoff()
        
        print(f"\n+ CrewAI execution successful!")
        print(f"+ Result: {result}")
        return True
        
    except Exception as e:
        print(f"* ERROR: CrewAI execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_crewai_with_lm_studio()
