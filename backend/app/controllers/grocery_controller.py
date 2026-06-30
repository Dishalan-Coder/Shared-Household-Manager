from datetime import datetime
from bson import ObjectId
from ..database import groceries_collection

async def add_grocery_item(household_id, name, added_by, quantity=1):
    doc = {
        "household_id": household_id,
        "name":         name,
        "quantity":     quantity,
        "added_by":     added_by,
        "checked":      False,
        "created_at":   datetime.utcnow()
    }
    res = await groceries_collection.insert_one(doc)
    return str(res.inserted_id)

async def get_groceries(household_id):
    out = []
    async for g in groceries_collection.find({"household_id": household_id}).sort("created_at", -1):
        g["id"] = str(g["_id"]); del g["_id"]
        out.append(g)
    return out

async def toggle_grocery(item_id, checked):
    await groceries_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"checked": checked}}
    )
    return True

async def delete_grocery(item_id):
    await groceries_collection.delete_one({"_id": ObjectId(item_id)})
    return True