from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.smart_parking
vehicles_collection = db.vehicles
history_collection = db.parking_history
