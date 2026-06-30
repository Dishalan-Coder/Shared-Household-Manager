from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from typing import List
from ..models.schemas import ExpenseCreate
from ..controllers import expense_controller, household_controller
from ..services.balance_service import compute_balances
from ..utils.auth import get_current_user
from ..utils.csv_handler import parse_expenses_csv, generate_expenses_csv
from fastapi import UploadFile, File

router = APIRouter(prefix="/api/expenses", tags=["expenses"])

@router.post("/")
async def add_expense(payload: ExpenseCreate, user=Depends(get_current_user)):
    if not user.get("household_id"):
        raise HTTPException(status_code=400, detail="Join a household first")
    eid = await expense_controller.add_expense(
        user["household_id"], payload.description, payload.amount,
        payload.payer_id, payload.split_between, payload.date
    )
    return {"id": eid}

@router.get("/")
async def list_expenses(user=Depends(get_current_user)):
    if not user.get("household_id"):
        return []
    return await expense_controller.get_expenses(user["household_id"])

@router.delete("/{expense_id}")
async def delete_expense(expense_id: str, user=Depends(get_current_user)):
    await expense_controller.delete_expense(expense_id)
    return {"ok": True}


@router.post("/upload-csv")
async def upload_expenses_csv(file: UploadFile = File(...), user=Depends(get_current_user)):
    if not user.get("household_id"):
        raise HTTPException(status_code=400, detail="Join a household first")
    rows = await parse_expenses_csv(file)
    hh = await household_controller.get_household(user["household_id"])
    member_map = {m["name"]: m["id"] for m in hh["members"]}
    added = await expense_controller.bulk_add_expenses(user["household_id"], rows, member_map)
    return {"added": added, "total_in_file": len(rows)}


@router.get("/download-csv")
async def download_expenses_csv(user=Depends(get_current_user)):
    if not user.get("household_id"):
        raise HTTPException(status_code=400, detail="Join a household first")
    expenses = await expense_controller.get_expenses(user["household_id"])
    csv_text = generate_expenses_csv(expenses)
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=bills.csv"}
    )


@router.get("/balances")
async def get_balances(user=Depends(get_current_user)):
    if not user.get("household_id"):
        raise HTTPException(status_code=400, detail="Join a household first")
    return await compute_balances(user["household_id"])