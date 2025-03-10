from fastapi import FastAPI
from routes.vehicle_routes import router as vehicle_router
from routes.history_routes import router as history_router
from routes.lpr_routes import router as lpr_router
import os

app = FastAPI()

# Ensure the "plates" directory exists before the server starts
os.makedirs("plates", exist_ok=True)

# Include all routers
app.include_router(vehicle_router)
app.include_router(history_router)
app.include_router(lpr_router)

@app.get("/")
async def root():
    return {"message": "Smart Parking API Running!"}
