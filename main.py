from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_parking
vehicles_collection = db.vehicles

@app.get("/")
async def root():
    return {"message": "MongoDB Connected Successfully"}

# Park a vehicle (Stores entry time)
@app.post("/park")
async def park_vehicle(plate_number: str, slot: str):
    existing_vehicle = vehicles_collection.find_one({"slot": slot})
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Slot already occupied! Choose a different slot.")

    vehicle_data = {
        "plate_number": plate_number,
        "slot": slot,
        "entry_time": datetime.utcnow()  # Store current time (UTC)
    }
    vehicles_collection.insert_one(vehicle_data)

    return {
        "message": "Vehicle Parked",
        "plate_number": plate_number,
        "slot": slot,
        "entry_time": vehicle_data["entry_time"]
    }

# Remove a vehicle and calculate duration
@app.delete("/remove/{plate_number}")
async def remove_vehicle(plate_number: str):
    vehicle = vehicles_collection.find_one({"plate_number": plate_number})
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found!")

    # Calculate parking duration
    entry_time = vehicle["entry_time"]
    exit_time = datetime.utcnow()
    duration = exit_time - entry_time
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)

    # Remove vehicle from DB
    vehicles_collection.delete_one({"plate_number": plate_number})

    return {
        "message": "Vehicle Removed",
        "plate_number": plate_number,
        "parking_duration": f"{int(hours)} hours, {int(minutes)} minutes"
    }

# Get all parked vehicles
@app.get("/vehicles")
async def get_vehicles():
    vehicles = list(vehicles_collection.find({}, {"_id": 0}))
    return {"vehicles": vehicles}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

