from fastapi import APIRouter
from app.config.database import db

router = APIRouter(prefix="/balance", tags=["Balance"])

expenses = db.expenses


@router.get("/{household_id}")
async def calculate_balance(household_id: str):

    balance = {}

    async for exp in expenses.find({"household_id": household_id}):

        amount = exp["amount"]
        paid_by = exp["paid_by"]
        participants = exp["participants"]

        share = amount / len(participants)

        # credit paid_by
        balance[paid_by] = balance.get(paid_by, 0) + (amount - share)

        for p in participants:
            if p != paid_by:
                balance[p] = balance.get(p, 0) - share

    return balance