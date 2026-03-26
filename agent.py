#!/usr/bin/env python3
"""Simple Hermes Agent chatbot - prints responses to console."""

import os
from run_agent import AIAgent


def main():
    # Use local LM Studio instance (check env vars first)
    agent = AIAgent(
        quiet_mode=True,
        provider="openai",  # LM Studio uses OpenAI-compatible API
        base_url=os.getenv("OPENAI_BASE_URL", "http://192.168.0.107:1234/v1"),
        model=os.getenv("LLM_MODEL", "qwen/qwen3.5-35b-a3b"),
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
