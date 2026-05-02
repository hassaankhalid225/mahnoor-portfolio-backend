import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not set")


client = AsyncIOMotorClient(MONGO_URI)
db = client["portfolio_db"]

# Collections
videos_collection = db["videos"]
shorts_collection = db["shorts"]
posters_collection = db["posters"]
