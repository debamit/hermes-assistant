# Hermes Assistant

A simple chat agent built using the Hermes Agent Python library.

## Setup

```bash
uv sync
# Optional: override defaults with env vars
export OPENAI_BASE_URL=http://192.168.0.107:1234/v1
export LLM_MODEL=qwen/qwen3.5-35b-a3b
```

## Usage

```bash
uv run python agent.py
# or after installation:
assistant
```

Uses your local LM Studio instance by default (no API key needed).
