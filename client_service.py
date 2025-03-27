import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
load_dotenv()
APP_TOKEN = os.getenv("APP_TOKEN")


DB_SERVICE_URL = f"http://localhost:8001"
BUSINESS_SERVICE_URL = f"http://localhost:8002"


@app.get("/")
def root():
    return {
        "description": "Client Service - orchestrates DB and Business Logic Service calls with token authentication."
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize")
def summarize_article(
    id: int = Query(..., description="ID of the article to summarize"),
    authorization: str = Query(..., description="token")
):
    if authorization != APP_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        resp = requests.get(f"{DB_SERVICE_URL}/read", params={"id": id})
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Article with id={id} not found.")
        elif resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"DB read error: {resp.text}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Cannot connect to DB Service: {str(e)}")

    article = resp.json().get("article", {})
    article_body = article.get("body", "")
    article_title = article.get("title", "")

    if not article_body:
        raise HTTPException(status_code=400, detail="Article has no body to summarize.")

    try:
        bl_resp = requests.post(f"{BUSINESS_SERVICE_URL}/process", json={"text": article_body})
        if bl_resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Business Logic error: {bl_resp.text}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Cannot connect to Business Logic Service: {str(e)}")

    summary = bl_resp.json().get("summary", "")
    if not summary:
        raise HTTPException(status_code=500, detail="Empty summary received from Business Logic Service.")

    try:
        update_resp = requests.post(
            f"{DB_SERVICE_URL}/update",
            params={"id": id},
            json={"summary": summary}
        )
        if update_resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to update DB: {update_resp.text}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Cannot connect to DB service for updating: {str(e)}")

    return {
        "status": "success",
        "id": id,
        "title": article_title,
        "summary": summary
    }
