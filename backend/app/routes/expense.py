from fastapi import APIRouter
from app.config.database import db

router = APIRouter(prefix="/expense", tags=["Expense"])

expenses = db.expenses


@router.post("/")
async def add_expense(data: dict):
    expense = {
        "title": data["title"],
        "amount": data["amount"],
        "paid_by": data["paid_by"],
        "household_id": data["household_id"],
        "participants": data["participants"]
    }

    result = await expenses.insert_one(expense)
    return {"message": "Expense added", "id": str(result.inserted_id)}


@router.get("/{household_id}")
async def get_expenses(household_id: str):
    data = []
    async for e in expenses.find({"household_id": household_id}):
        e["_id"] = str(e["_id"])
        data.append(e)

    return data