from datetime import datetime, timedelta
from bson import ObjectId
from ..database import chores_collection, users_collection

FREQ_DELTA = {
    "daily":   timedelta(days=1),
    "weekly":  timedelta(weeks=1),
    "monthly": timedelta(days=30),
}

async def create_chore(household_id, title, description, due_date, assigned_to,
                       frequency="none", rotation_members=None):
    doc = {
        "household_id":     household_id,
        "title":            title,
        "description":      description or "",
        "due_date":         due_date,
        "assigned_to":      assigned_to,
        "completed":        False,
        "frequency":        frequency,
        "rotation_members": rotation_members or [],
        "rotation_index":   0,
        "created_at":       datetime.utcnow()
    }
    res = await chores_collection.insert_one(doc)
    return str(res.inserted_id)

async def _populate(chore):
    chore["id"] = str(chore["_id"])
    del chore["_id"]
    u = await users_collection.find_one({"_id": ObjectId(chore["assigned_to"])})
    chore["assigned_to_name"] = u["name"] if u else "Unknown"
    return chore

async def get_chores(household_id):
    out = []
    async for c in chores_collection.find({"household_id": household_id}).sort("due_date", 1):
        out.append(await _populate(c))
    return out

async def complete_chore(chore_id):
    chore = await chores_collection.find_one({"_id": ObjectId(chore_id)})
    if not chore:
        return None

    rotation = chore.get("rotation_members") or []
    if rotation:
        # ROTATING chore → advance index, assign next member, push due date forward
        idx = (chore.get("rotation_index", 0) + 1) % len(rotation)
        next_assignee = rotation[idx]
        old_due = datetime.fromisoformat(chore["due_date"])
        delta   = FREQ_DELTA.get(chore.get("frequency", "weekly"), timedelta(weeks=1))
        new_due = (old_due + delta).isoformat()

        await chores_collection.update_one(
            {"_id": ObjectId(chore_id)},
            {"$set": {
                "completed":          False,        # reset for next rotation
                "assigned_to":        next_assignee,
                "rotation_index":     idx,
                "due_date":           new_due,
                "last_completed_at":  datetime.utcnow().isoformat(),
                "last_completed_by":  chore["assigned_to"]
            }}
        )
    else:
        await chores_collection.update_one(
            {"_id": ObjectId(chore_id)},
            {"$set": {
                "completed":     True,
                "completed_at":  datetime.utcnow().isoformat()
            }}
        )
    return True

async def delete_chore(chore_id):
    await chores_collection.delete_one({"_id": ObjectId(chore_id)})
    return True