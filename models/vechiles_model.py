from pydantic import BaseModel

class Vehicle(BaseModel):
    plate_number: str
    slot: str
