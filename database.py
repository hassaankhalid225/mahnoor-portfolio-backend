import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://mahnoorfatim09_db_user:3WIGPNyaLdiC8qgX@portfolio-data.imvpfu9.mongodb.net/?appName=portfolio-data"
)

client = AsyncIOMotorClient(MONGO_URI)
db = client["portfolio_db"]

# Collections
videos_collection = db["videos"]
shorts_collection = db["shorts"]
posters_collection = db["posters"]
