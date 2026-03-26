#!/usr/bin/env python3
"""Simple Hermes Agent chatbot - prints responses to console."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env from project directory
load_dotenv(Path(__file__).parent / ".env")

from run_agent import AIAgent


def main():
    agent = AIAgent(
        model=os.environ.get("LLM_MODEL", "qwen3.5-27b"),
        provider="cus",  # Let's it use base_url override
        base_url=os.environ.get("OPENAI_BASE_URL", "http://192.168.0.107:1234/v1"),
        api_key="dummy",  # Required but not used by LM Studio
        quiet_mode=True,
    )
    
    print("Hermes Assistant (type 'quit' to exit)")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ('quit', 'exit'):
            break
        
        response = agent.chat(user_input)
        print(f"\nAssistant: {response}")


if __name__ == "__main__":
    main()
