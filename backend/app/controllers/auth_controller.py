from bson import ObjectId
from ..database import users_collection
from ..utils.auth import hash_password, verify_password, create_access_token

async def register(name: str, email: str, password: str):
    if await users_collection.find_one({"email": email}):
        return None
    doc = {"name": name, "email": email, "password": hash_password(password)}
    result = await users_collection.insert_one(doc)
    token  = create_access_token({"sub": str(result.inserted_id)})
    return {"token": token, "user": {"id": str(result.inserted_id), "name": name, "email": email}}

async def login(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None
    token = create_access_token({"sub": str(user["_id"])})
    return {"token": token, "user": {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}}