#!/usr/bin/env python3
"""FastAPI server exposing Hermes Agent chat endpoint."""

import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from dotenv import load_dotenv

import httpx

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Load local .env from project directory
load_dotenv(Path(__file__).parent / ".env")
# I think the problem is here

from run_agent import AIAgent


app = FastAPI(
    title="Hermes Assistant API",
    description="Chat endpoint powered by Hermes Agent and LM Studio"
)


class ChatRequest(BaseModel):
    message: str
    model: str = "qwen/qwen3.5-9b"


# Create agent once at startup (more efficient than creating per request)
print("Initializing AIAgent...")
start_time = time.time()
print(f"Using model: {os.environ.get('LLM_MODEL', 'qwen/qwen3.5-9b')}")
agent = AIAgent(
    # model=os.environ.get("LLM_MODEL", "qwen/qwen3.5-9b"),
    model="qwen/qwen3.5-9b",  # Override to smaller model for local testing
    provider="cus",
    base_url=os.environ.get("OPENAI_BASE_URL", "http://192.168.0.107:1234/v1"),
    api_key="***",  # Required but not used by LM Studio
    quiet_mode=True,
)
print(f"AIAgent initialized in {time.time() - start_time:.2f}s")


@app.post("/chat")
async def chat(request: ChatRequest):
    """Send a message to the Hermes Agent and get a response."""
    print(f"Received message: {request.message[:50]}...")
    start = time.time()
    response = agent.chat(request.message)
    elapsed = time.time() - start
    print(f"Response generated in {elapsed:.2f}s")
    return {"response": response}


@app.get("/")
async def root():
    """Serve the chat UI."""
    return FileResponse(str(Path(__file__).parent / "static" / "index.html"))


@app.get("/docs")
async def docs():
    """Get API documentation."""
    return {
        "message": "Visit /docs/swagger-ui.html for interactive API docs",
        "endpoints": {
            "GET /": "Serve chat UI",
            "GET /info": "Model and server info",
            "POST /chat": "Send a chat message",
            "POST /chat/stream": "Stream chat response via SSE",
        }
    }


@app.get("/prices.html")
async def prices_html():
    """Serve the price blocks component HTML."""
    return FileResponse(str(Path(__file__).parent / "static" / "prices.html"))


@app.get("/info")
async def info():
    """Return model and server info as JSON."""
    return {
        "model": os.environ.get("LLM_MODEL", "qwen3.5-27b"),
        "base_url": os.environ.get("OPENAI_BASE_URL", "http://192.168.0.107:1234/v1"),
    }


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream a chat response using SSE. Runs agent.chat() in a thread
    so synchronous token callbacks can feed an async queue in real-time."""
    print(f"[stream] Received: {request.message[:50]}...")

    queue: asyncio.Queue[str] = asyncio.Queue()
    done_event = asyncio.Event()
    error_event = asyncio.Event()
    error_msg = {"value": ""}

    def stream_callback(token: str):
        loop.call_soon_threadsafe(lambda: queue.put_nowait(token))

    def run_chat():
        try:
            agent.chat(request.message, stream_callback=stream_callback)
        except Exception as e:
            error_msg["value"] = str(e)
            loop.call_soon_threadsafe(error_event.set)
        finally:
            loop.call_soon_threadsafe(done_event.set)

    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    loop.run_in_executor(executor, run_chat)

    async def event_generator():
        try:
            while not done_event.is_set() or not queue.empty():
                try:
                    token = await asyncio.wait_for(queue.get(), timeout=0.5)
                    yield f"data: {token}\n\n"
                except asyncio.TimeoutError:
                    continue

            if error_event.is_set():
                yield f"data: [error: {error_msg['value']}]\n\n"
            else:
                yield f"data: [done]\n\n"
        finally:
            executor.shutdown(wait=False)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/prices")
async def prices():
    """Return BTC, GOLD, SILVER prices in USD and ETH equivalents.
    Cached for 60 seconds to avoid hammering CoinGecko's free API."""
    import time

    now = time.time()
    cached = getattr(prices, "_cache", None)
    if cached and (now - cached["ts"]) < 60:
        return cached["data"]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Fetch BTC, ETH, silver (XAG), and gold (XAU) in one request
            r = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "bitcoin,ethereum,silver,gold",
                    "vs_currencies": "usd",
                },
            )
            r.raise_for_status()
            data = r.json()

        btc_usd = data["bitcoin"]["usd"]
        eth_usd = data["ethereum"]["usd"]
        xag_usd = data["silver"]["usd"]
        xau_usd = data["gold"]["usd"]

        result = {
            "btc":    {"usd": btc_usd,  "eth": round(btc_usd  / eth_usd, 6)},
            "gold":   {"usd": xau_usd, "eth": round(xau_usd / eth_usd, 6)},
            "silver": {"usd": xag_usd, "eth": round(xag_usd / eth_usd, 6)},
            "ts": now,
        }

        prices._cache = {"data": result, "ts": now}
        return result

    except Exception as e:
        # Fall back to last cached value if API fails
        if cached:
            return cached["data"]
        return {"error": str(e)}
