from datetime import datetime
from bson import ObjectId
from ..database import expenses_collection, users_collection

async def add_expense(household_id, description, amount, payer_id, split_between, date=None):
    doc = {
        "household_id":   household_id,
        "description":    description,
        "amount":         float(amount),
        "payer_id":       payer_id,
        "split_between":  split_between,
        "date":           date or datetime.utcnow().isoformat(),
        "created_at":     datetime.utcnow()
    }
    res = await expenses_collection.insert_one(doc)
    return str(res.inserted_id)

async def _populate(exp):
    exp["id"] = str(exp["_id"]); del exp["_id"]
    payer = await users_collection.find_one({"_id": ObjectId(exp["payer_id"])})
    exp["payer_name"] = payer["name"] if payer else "Unknown"
    names = []
    for sid in exp.get("split_between", []):
        u = await users_collection.find_one({"_id": ObjectId(sid)})
        names.append(u["name"] if u else "Unknown")
    exp["split_between_names"] = names
    return exp

async def get_expenses(household_id):
    out = []
    async for e in expenses_collection.find({"household_id": household_id}).sort("date", -1):
        out.append(await _populate(e))
    return out

async def delete_expense(expense_id):
    await expenses_collection.delete_one({"_id": ObjectId(expense_id)})
    return True

async def bulk_add_expenses(household_id, rows, member_map):
    """member_map: {name -> user_id}.  Returns count of inserted rows."""
    added = 0
    for row in rows:
        description = row.get("description", "").strip()
        amount_str  = row.get("amount", "0").strip()
        payer_name  = row.get("payer", "").strip()
        date        = row.get("date", "").strip() or None
        split_str   = row.get("split_between", "").strip()

        try:
            amount = float(amount_str)
        except ValueError:
            continue
        payer_id = member_map.get(payer_name)
        if not payer_id:
            continue

        if split_str:
            split_names = [s.strip() for s in split_str.split(",") if s.strip()]
            split_between = [member_map[n] for n in split_names if n in member_map]
        else:
            split_between = list(member_map.values())
        if not split_between:
            continue

        await add_expense(household_id, description, amount, payer_id, split_between, date)
        added += 1
    return added