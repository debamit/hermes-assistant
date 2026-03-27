# Hermes Assistant

A terminal-based chat agent built using the [Hermes Agent Python library](https://github.com/hermes-agent/hermes-agent).

## Purpose & Vision

**Mission:** Provide an AI-powered conversational assistant that operates directly in your terminal, integrating seamlessly with local LLM instances.

**Why this project?**
- Simplify local AI development workflows
- Enable offline-first AI chat experiences  
- Bridge the gap between powerful local models (like LM Studio) and interactive chat interfaces
- Create a lightweight, customizable chatbot without cloud dependencies

## Architecture

```
┌─────────────────┐     ┌───────────────────┐     ┌─────────────────┐
│  FastAPI Server  │────▶│  Hermes Agent Core│────▶│  Local LLM      │
│    (app.py)      │     │   (chatbot.py)    │     │  Instance       │
└─────────────────┘     └───────────────────┘     └─────────────────┘

        ▲                              ▼
        └──────────── Static HTML UI ─────────────┘
```

**Components:**
- **FastAPI Backend** (port 8000) - REST API for chat operations, health checks, and swagger docs
- **Hermes Agent CLI** - Core chatbot logic and conversation management  
- **Static HTML Frontend** - Browser-based chat interface (no Gradio)

## Setup

```bash
# Clone or navigate to the project
cd ~/hermes-assistant

# Sync dependencies
uv sync

# Optional: configure your local LLM (default uses LM Studio)
export OPENAI_BASE_URL=http://127.0.0.1:1234/v1
export LLM_MODEL=qwen/qwen3.5-9b
```

## Usage

### Start FastAPI Server

Terminal 1 - Backend API:
```bash
uv run uvicorn app:app --reload --port 8000
```

**Endpoints:**
- `http://localhost:8000/` - Health check
- `http://localhost:8000/docs` - Swagger UI (interactive API docs)
- `http://localhost:8000/chat` - Chat API endpoint (`POST` with JSON body like `{"message": "hello"}`)

### Start CLI Chatbot (for development/testing)

Terminal 2 - Development mode:
```bash
uv run python chatbot.py
```

**Or after installation:**
```bash
chatbot
```

### Browser UI (Static HTML)

Open `http://localhost:8000/docs` in your browser to access the chat interface directly through the API. This uses the static HTML frontend - no Gradio app needed.

## Running the Application

**Typical workflow:**
1. Terminal 1: FastAPI server running on port 8000
2. Browser: Open `http://localhost:8000/docs` for chat UI
3. CLI: Optional terminal-based testing via `chatbot` command

## Configuration Tips

**Using different LLMs:**
```bash
# LM Studio (default)
export OPENAI_BASE_URL=http://127.0.0.1:1234/v1

# Ollama
export OPENAI_BASE_URL=http://localhost:11434/v1

# Other OpenAI-compatible services
export OPENAI_BASE_URL=<your-llm-endpoint>/v1
```

**Model selection:**
```bash
export LLM_MODEL=qwen/qwen3.5-9b  # Adjust to your preferred model
```

## Project Structure

```
~/hermes-assistant/
├── app.py                 # FastAPI backend (REST API)
├── chatbot.py             # Hermes Agent CLI (core chat logic)
├── static/                # HTML frontend assets
│   └── *.html            # Static UI files
├── pyproject.toml         # Dependencies and project config
└── README.md              # This file
```

## Note: No Gradio Frontend

This project intentionally uses a **static HTML interface** rather than Gradio for the browser-based chat. The `gradio_app.py` file exists but is not part of the active deployment - we use FastAPI's static files endpoint instead.

## Getting Help

- Check Swagger UI at `http://localhost:8000/docs` for API documentation
- Review the Hermes Agent library docs for advanced patterns
- See existing skills in `~/.hermes/skills/` for integration examples
