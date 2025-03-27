# 🧠 Article Summarization Microservice App

This project demonstrates a complete microservice-based architecture for article summarization using an LLM (Mistral via OpenRouter). It includes three independently running FastAPI services:

- **Business Logic Service** — handles text summarization using an external model
- **Database Service** — simulates persistent storage for articles
- **Client Service** — the only public-facing service that orchestrates communication between the other two

---

## 📁 Project Structure

```
.
├── client_service.py         # Handles authentication, orchestration
├── business_service.py       # Calls the LLM to summarize article text
├── db_service.py             # In-memory article store with CRUD endpoints
├── run_all.py                # Starts all services and demonstrates end-to-end flow
├── use.py                    # Example usage: populates DB and calls /summarize
├── .env.example              # Environment variable template
```

---

## 🚀 Running the App

### 1. 📦 Install Requirements

```bash
pip install fastapi uvicorn requests python-dotenv
```

### 2. ⚙️ Create a `.env` File

Create a `.env` file in your root directory with this content:

```env
APP_TOKEN=mysecrettoken123
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
MODEL=mistralai/mistral-small-3.1-24b-instruct:free
```

> Do not commit this file. A `.env.example` is included.

---

### 3. ▶️ Start the Services

To launch all services in one go:

```bash
python run_all.py
```

This script:
- Starts all 3 services (`db`, `business`, `client`)
- Waits for them to be healthy
- Populates the database with an article
- Calls the client service to generate a summary
- Outputs the result

To stop: Press `ENTER`

---

## 🔗 Endpoints Summary

### 🧠 Business Logic Service (port 8002)
| Endpoint       | Method | Description                       |
|----------------|--------|-----------------------------------|
| `/`            | GET    | Returns service description       |
| `/health`      | GET    | Health check                      |
| `/process`     | POST   | Generates summary using LLM       |

---

### 🗃️ Database Service (port 8001)
| Endpoint       | Method | Description                           |
|----------------|--------|---------------------------------------|
| `/`            | GET    | Returns service description           |
| `/health`      | GET    | Health check                          |
| `/write`       | POST   | Adds a new article                    |
| `/read`        | GET    | Reads article(s) by `id` or `title`   |
| `/update`      | POST   | Updates an article by `id`            |

---

### 🌐 Client Service (port 8000)
| Endpoint       | Method | Description                              |
|----------------|--------|------------------------------------------|
| `/`            | GET    | Returns service description              |
| `/health`      | GET    | Health check                             |
| `/summarize`   | POST   | Requires token, summarizes article by ID |

**Usage:**
```bash
curl -X POST "http://localhost:8000/summarize?id=1&authorization=mysecrettoken123"
```

---

## 🔐 Authentication

The **Client Service** requires a token to access the `/summarize` endpoint.

- The token can be passed via **query param**: `?authorization=mysecrettoken123`
- The expected token is stored in `.env` as `APP_TOKEN`

---

## 🧪 Testing the Flow

Use the provided script:
```bash
python use.py
```
This will:
- Populate the DB with 5 articles
- Call the summarization flow for article ID `1`
- Print the resulting summary

---

## ✅ Requirements Checklist

- [x] Three FastAPI microservices
- [x] Health endpoints on all services
- [x] Root `/` endpoints with descriptions
- [x] Token-based authentication
- [x] Business logic calls LLM via API (OpenRouter)
- [x] Client orchestrates read → summarize → update → return
- [x] `.env` used for secrets/config
- [x] Example usage script provided
- [x] Run-all script included

---

## 📌 Notes

- All services run on `localhost` using ports `8000`, `8001`, and `8002`
- Article `id` is auto-incremented
- Article `title` is non-unique
