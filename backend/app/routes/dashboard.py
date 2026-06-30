from fastapi import APIRouter
from app.config.database import db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

chores = db.chores
expenses = db.expenses
grocery = db.grocery


@router.get("/{household_id}")
async def dashboard(household_id: str):

    total_chores = await chores.count_documents({"household_id": household_id})
    completed = await chores.count_documents({
        "household_id": household_id,
        "completed": True
    })

    total_expenses = 0
    async for e in expenses.find({"household_id": household_id}):
        total_expenses += e["amount"]

    grocery_count = await grocery.count_documents({"household_id": household_id})

    return {
        "total_chores": total_chores,
        "completed_chores": completed,
        "pending_chores": total_chores - completed,
        "total_expenses": total_expenses,
        "grocery_items": grocery_count
    }