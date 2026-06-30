import secrets
from bson import ObjectId
from ..database import households_collection, users_collection

async def create_household(name: str, owner_id: str):
    code = secrets.token_hex(3).upper()
    doc = {
        "name": name,
        "owner_id": owner_id,
        "members": [owner_id],
        "invite_code": code
    }
    res = await households_collection.insert_one(doc)
    hid = str(res.inserted_id)
    await users_collection.update_one(
        {"_id": ObjectId(owner_id)},
        {"$set": {"household_id": hid}}
    )
    return {"id": hid, "name": name, "invite_code": code, "members": [owner_id]}

async def join_household(code: str, user_id: str):
    household = await households_collection.find_one({"invite_code": code.upper()})
    if not household:
        return None
    if user_id not in household["members"]:
        await households_collection.update_one(
            {"_id": household["_id"]},
            {"$addToSet": {"members": user_id}}
        )
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"household_id": str(household["_id"])}}
    )
    return await get_household(str(household["_id"]))

async def get_household(household_id: str):
    household = await households_collection.find_one({"_id": ObjectId(household_id)})
    if not household:
        return None
    members_info = []
    for mid in household["members"]:
        u = await users_collection.find_one({"_id": ObjectId(mid)})
        if u:
            members_info.append({"id": str(u["_id"]), "name": u["name"], "email": u["email"]})
    return {
        "id": str(household["_id"]),
        "name": household["name"],
        "invite_code": household["invite_code"],
        "owner_id": household["owner_id"],
        "members": members_info
    }

async def get_user_household(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user or "household_id" not in user:
        return None
    return await get_household(user["household_id"])