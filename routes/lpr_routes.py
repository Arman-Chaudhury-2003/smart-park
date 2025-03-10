from fastapi import APIRouter, File, UploadFile
from services.lpr_service import process_image
import os
import shutil

router = APIRouter()

# Ensure the plates directory exists
os.makedirs("plates", exist_ok=True)

@router.post("/detect_plate")
async def detect_plate(file: UploadFile = File(...)):
    file_path = f"plates/{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the image
    plate_number = process_image(file_path)

    return {"plate_number": plate_number}
