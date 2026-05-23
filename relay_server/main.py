import asyncio
import json
import os
from typing import AsyncGenerator
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

app = FastAPI(title="Bogatti Relay Gateway")

# Configuration from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-placeholder")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "google-placeholder")
ADMIN_SECRET = os.getenv("BOGATTI_ADMIN_SECRET", "secure_key_123")

class ChatRequest(BaseModel):
    model: str
    prompt: str
    system_prompt: str = "You are Bogatti, a helpful AI assistant."
    stream: bool = True

async def stream_openai_response(prompt: str, model: str) -> AsyncGenerator[str, None]:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", url, headers=headers, json=payload, timeout=60.0) as response:
                if response.status_code != 200:
                    yield f"data: {json.dumps({'error': 'Upstream error'})}\n\n"
                    return
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            yield f"data: {data}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.post("/v1/chat")
async def chat_relay(request: ChatRequest, req: Request):
    # Authenticate with Android App
    auth_header = req.headers.get("Authorization")
    if not auth_header or ADMIN_SECRET not in auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if "gpt" in request.model.lower():
        return StreamingResponse(
            stream_openai_response(request.prompt, request.model),
            media_type="text/event-stream"
        )
    else:
        async def dummy_stream():
            yield "data: {\"choices\": [{\"delta\": {\"content\": \"Bogatti Relay: " + request.model + " is being processed...\"}}]}\n\n"
            await asyncio.sleep(0.5)
            yield "data: [DONE]\n\n"
        return StreamingResponse(dummy_stream(), media_type="text/event-stream")

@app.get("/config")
async def get_remote_config():
    return {
        "strings": {
            "app_title": "بوگاتی",
            "input_placeholder": "چیزی بپرس..."
        },
        "active_models": [
            {"name": "GPT-4o", "id": "gpt-4o", "provider": "openai"},
            {"name": "Gemini 1.5 Pro", "id": "gemini-1.5-pro", "provider": "google"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    # In production, use environment variables for host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
