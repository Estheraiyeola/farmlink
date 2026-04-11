from fastapi import FastAPI

app = FastAPI(title="FarmLink Price Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "price-service"}

@app.get("/api/prices/{crop_type}")
def get_prices(crop_type: str):
    return {"crop_type": crop_type, "message": "stub - not yet implemented"}

@app.get("/api/prices/{crop_type}/history")
def get_price_history(crop_type: str):
    return {"crop_type": crop_type, "message": "stub - not yet implemented"}

@app.get("/api/prices/fair-value/{listing_id}")
def get_fair_value(listing_id: str):
    return {"listing_id": listing_id, "message": "stub - not yet implemented"}
