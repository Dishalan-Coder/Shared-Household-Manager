from fastapi import APIRouter
from app.config.database import db
from bson import ObjectId

router = APIRouter(prefix="/grocery", tags=["Grocery"])

grocery = db.grocery


@router.post("/")
async def add_item(data: dict):
    item = {
        "item": data["item"],
        "quantity": data["quantity"],
        "household_id": data["household_id"],
        "completed": False
    }

    result = await grocery.insert_one(item)
    return {"message": "Item added", "id": str(result.inserted_id)}


@router.get("/{household_id}")
async def get_items(household_id: str):
    items = []
    async for i in grocery.find({"household_id": household_id}):
        i["_id"] = str(i["_id"])
        items.append(i)

    return items


@router.put("/{item_id}")
async def mark_done(item_id: str):
    await grocery.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"completed": True}}
    )
    return {"message": "Item completed"}