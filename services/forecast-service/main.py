from fastapi import FastAPI

app = FastAPI(title="FarmLink Forecast Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "forecast-service"}

@app.get("/api/forecast/{state}")
def get_forecast_by_state(state: str):
    return {"state": state, "message": "stub - not yet implemented"}

@app.get("/api/forecast/demand/{crop_type}")
def get_demand_by_crop(crop_type: str):
    return {"crop_type": crop_type, "message": "stub - not yet implemented"}
