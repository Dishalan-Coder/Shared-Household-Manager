
from bson import ObjectId
from ..database import expenses_collection, households_collection, users_collection

async def compute_balances(household_id: str):
    household = await households_collection.find_one({"_id": ObjectId(household_id)})
    if not household:
        return None

    member_ids = [str(m) for m in household["members"]]
    members = {}
    for mid in member_ids:
        user = await users_collection.find_one({"_id": ObjectId(mid)})
        members[mid] = {
            "id": mid,
            "name": user["name"] if user else "Unknown",
            "paid": 0.0,
            "owed": 0.0,
            "net": 0.0
        }

    total_expenses = 0.0
    async for exp in expenses_collection.find({"household_id": household_id}):
        payer_id = exp["payer_id"]
        amount   = float(exp["amount"])
        split_between = exp.get("split_between") or member_ids
        if not split_between:
            split_between = member_ids
        share = amount / len(split_between)

        if payer_id in members:
            members[payer_id]["paid"] += amount
        for sid in split_between:
            if sid in members:
                members[sid]["owed"] += share
        total_expenses += amount

    for m in members.values():
        m["net"]   = round(m["paid"] - m["owed"], 2)
        m["paid"]  = round(m["paid"], 2)
        m["owed"]  = round(m["owed"], 2)

    
    balances = [dict(m) for m in members.values()]
    debtors   = sorted([m for m in balances if m["net"] < 0], key=lambda x: x["net"])
    creditors = sorted([m for m in balances if m["net"] > 0], key=lambda x: x["net"], reverse=True)

    settlements = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debt   = round(-debtors[i]["net"], 2)
        credit = round(creditors[j]["net"], 2)
        settled = round(min(debt, credit), 2)
        if settled > 0.00:
            settlements.append({
                "from":        debtors[i]["name"],
                "from_id":     debtors[i]["id"],
                "to":          creditors[j]["name"],
                "to_id":       creditors[j]["id"],
                "amount":      settled
            })
        debtors[i]["net"]   = round(debtors[i]["net"]   + settled, 2)
        creditors[j]["net"] = round(creditors[j]["net"] - settled, 2)
        if abs(debtors[i]["net"])   < 0.01: i += 1
        if abs(creditors[j]["net"]) < 0.01: j += 1

    return {
        "members":         list(members.values()),
        "settlements":     settlements,
        "total_expenses":  round(total_expenses, 2)
    }