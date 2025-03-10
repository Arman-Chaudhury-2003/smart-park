from fastapi import APIRouter, HTTPException
from config.database import vehicles_collection, history_collection
from datetime import datetime
import math

router = APIRouter()

PARKING_RATE_PER_HOUR = 50

@router.post("/park")
async def park_vehicle(plate_number: str, slot: str):
    if vehicles_collection.find_one({"slot": slot}):
        raise HTTPException(status_code=400, detail="Slot already occupied!")

    vehicle_data = {"plate_number": plate_number, "slot": slot, "entry_time": datetime.utcnow()}
    vehicles_collection.insert_one(vehicle_data)
    return {"message": "Vehicle Parked", "plate_number": plate_number, "slot": slot}

@router.delete("/remove_vehicle/{plate_number}")
async def remove_vehicle(plate_number: str):
    vehicle = vehicles_collection.find_one({"plate_number": plate_number})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    entry_time = vehicle["entry_time"]
    exit_time = datetime.utcnow()
    total_hours = math.ceil((exit_time - entry_time).total_seconds() / 3600)
    total_cost = total_hours * PARKING_RATE_PER_HOUR

    history_collection.insert_one({
        "plate_number": plate_number, "slot": vehicle.get("slot", "Unknown"),
        "entry_time": entry_time, "exit_time": exit_time,
        "duration_hours": total_hours, "total_cost": total_cost
    })
    vehicles_collection.delete_one({"plate_number": plate_number})
    return {"message": "Vehicle removed", "total_hours": total_hours, "total_cost": total_cost}

@router.get("/vehicles")
async def get_vehicles():
    return {"vehicles": list(vehicles_collection.find({}, {"_id": 0}))}
