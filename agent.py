#!/usr/bin/env python3
"""Simple Hermes Agent chatbot - prints responses to console."""

from run_agent import AIAgent


def main():
    agent = AIAgent(quiet_mode=True)
    
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
