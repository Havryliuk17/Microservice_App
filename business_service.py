import os
import time
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set. Please set it in your environment or .env file.")


# OpenRouter endpoint and model name
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

app = FastAPI()

class SummarizePayload(BaseModel):
    text: str

@app.get("/")
def root():
    """
    Root endpoint that returns a short description of this service.
    """
    return {"description": "Business Logic Service - Summarizes text using Mistral via OpenRouter"}

@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@app.post("/process")
def summarize_text(payload: SummarizePayload):
    """
    Accepts text and uses the Mistral model via OpenRouter to summarize it.
    """
    input_text = payload.text.strip()
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    prompt = (
        f"Summarize the following text into 1 or 2 paragraphs:\n\n\"{input_text}\"\n"
        "Focus on the main points, and keep it concise."
    )

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=HEADERS, json=body)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"OpenRouter API error: {response.text}")

    data = response.json()
    try:
        summary = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Unexpected response structure from OpenRouter.")

    return {
        "original_text": input_text,
        "summary": summary
    }