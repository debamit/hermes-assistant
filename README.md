# Hermes Assistant

A simple chat agent built using the Hermes Agent Python library.

## Setup

```bash
uv sync
# Optional: override defaults with env vars
export OPENAI_BASE_URL=http://192.168.0.107:1234/v1
export LLM_MODEL=qwen3.5-27b
```

## Usage

### Gradio UI (recommended)
```bash
uv run python gradio_app.py
```
Then open http://localhost:7860 in your browser.

Requires the FastAPI server to be running (see below).

### CLI Chatbot
```bash
uv run python chatbot.py
# or after installation:
chatbot
```

### FastAPI Server
```bash
uv run uvicorn app:app --reload
```

Then visit:
- http://localhost:8000/ - Health check
- http://localhost:8000/docs/swagger-ui.html - Interactive API docs
- http://localhost:8000/chat - Send POST requests with JSON: `{"message": "hello"}`

Uses your local LM Studio instance by default (no API key needed).

## Running both servers

In two separate terminals:
```bash
# Terminal 1 — FastAPI backend
uv run uvicorn app:app --reload --port 8000

# Terminal 2 — Gradio frontend
uv run python gradio_app.py
```

Then open http://localhost:7860 to chat.
