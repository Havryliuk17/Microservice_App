from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

db_storage: Dict[int, dict] = {}
next_id = 1

class ArticleInput(BaseModel):
    title: str
    body: str

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    summary: Optional[str] = None

@app.get("/")
def root():
    return {"description": "Database Service - Stores articles and allows reading and updating by id or title."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/write")
def write_article(article: ArticleInput):
    global next_id
    article_id = next_id
    next_id += 1

    db_storage[article_id] = {
        "id": article_id,
        "title": article.title.strip(),
        "body": article.body.strip(),
        "summary": None
    }

    return {"status": "saved", "id": article_id}

@app.get("/read")
def read_articles(id: Optional[int] = Query(None), title: Optional[str] = Query(None)):
    if id is not None:
        article = db_storage.get(id)
        if not article:
            raise HTTPException(status_code=404, detail=f"Article with id={id} not found.")
        return {"article": article}

    elif title:
        matches = [a for a in db_storage.values() if a["title"] == title.strip()]
        if not matches:
            raise HTTPException(status_code=404, detail=f"No articles found with title '{title}'.")
        return {"articles": matches}

    else:
        return {"articles": list(db_storage.values())}

@app.post("/update")
def update_article(id: int = Query(..., description="ID of the article to update"), update: ArticleUpdate = None):
    if id not in db_storage:
        raise HTTPException(status_code=404, detail=f"Article with id={id} not found.")

    article = db_storage[id]

    if update.title is not None:
        article["title"] = update.title.strip()
    if update.body is not None:
        article["body"] = update.body.strip()
    if update.summary is not None:
        article["summary"] = update.summary.strip()

    return {"status": "updated", "article": article}
