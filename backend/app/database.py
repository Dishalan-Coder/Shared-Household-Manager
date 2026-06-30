from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DB_NAME]

users_collection       = db["users"]
households_collection  = db["households"]
chores_collection      = db["chores"]
groceries_collection   = db["groceries"]
expenses_collection    = db["expenses"]