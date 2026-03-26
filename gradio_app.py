#!/usr/bin/env python3
"""Gradio UI for Hermes Assistant — runs on port 7860, streams from /chat/stream."""

import os
import httpx
from dotenv import load_dotenv
from pathlib import Path

import gradio as gr

# Load .env from project directory
load_dotenv(Path(__file__).parent / ".env")

API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
MODEL = os.environ.get("LLM_MODEL", "qwen3.5-27b")


async def stream_from_api(message: str, history: list):
    """Call /chat/stream and yield tokens as they arrive."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            async with client.stream(
                "POST",
                f"{API_BASE}/chat/stream",
                json={"message": message},
            ) as response:
                if response.status_code != 200:
                    yield f"Error: HTTP {response.status_code}"
                    return

                collected = []
                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    token = line[6:]  # strip "data: "
                    if token.startswith("[done") or token.startswith("[error"):
                        break
                    collected.append(token)
                    yield "".join(collected)

                yield "".join(collected)

        except httpx.TimeoutException:
            yield "Error: Request timed out."
        except Exception as e:
            yield f"Error: {e}"


# Build the Gradio UI
demo = gr.ChatInterface(
    fn=stream_from_api,
    title="Hermes Assistant",
    description=f"Streaming chat with {MODEL} via LM Studio. "
                f"Make sure the FastAPI server is running on {API_BASE}.",
    fill_height=True,
)

if __name__ == "__main__":
    print(f"Starting Gradio UI on http://localhost:7860")
    print(f"API base: {API_BASE} | Model: {MODEL}")
    demo.launch(server_port=7860, server_name="0.0.0.0")
