from fastapi import APIRouter
from config.database import history_collection

router = APIRouter()

@router.get("/parking_history")
async def get_parking_history():
    return {"parking_history": list(history_collection.find({}, {"_id": 0}))}
