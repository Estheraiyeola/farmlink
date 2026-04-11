# notification-service

FastAPI service that consumes Kafka events and sends SMS alerts to farmers and buyers via Termii.

## Kafka topics consumed
- order.confirmed
- escrow.held
- order.delivered
- escrow.released

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8086
```
