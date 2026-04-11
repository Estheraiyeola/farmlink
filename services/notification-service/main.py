from fastapi import FastAPI

app = FastAPI(title="FarmLink Notification Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}
