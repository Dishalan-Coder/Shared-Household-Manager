from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import MONGODB_URL, DATABASE_NAME


client = AsyncIOMotorClient(MONGODB_URL)


db = client[DATABASE_NAME]


