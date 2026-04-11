# price-service

FastAPI service that scrapes Nigerian market prices and exposes them via REST API. Uses Redis cache-aside pattern with 24-hour TTL.

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8084
```
