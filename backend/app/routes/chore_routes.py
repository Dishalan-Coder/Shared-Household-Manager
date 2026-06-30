from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import ChoreCreate
from ..controllers import chore_controller
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/chores", tags=["chores"])

@router.post("/")
async def create_chore(payload: ChoreCreate, user=Depends(get_current_user)):
    if not user.get("household_id"):
        raise HTTPException(status_code=400, detail="You must join a household first")
    cid = await chore_controller.create_chore(
        user["household_id"], payload.title, payload.description,
        payload.due_date, payload.assigned_to, payload.frequency,
        payload.rotation_members
    )
    return {"id": cid}

@router.get("/")
async def list_chores(user=Depends(get_current_user)):
    if not user.get("household_id"):
        return []
    return await chore_controller.get_chores(user["household_id"])

@router.post("/{chore_id}/complete")
async def complete_chore(chore_id: str, user=Depends(get_current_user)):
    ok = await chore_controller.complete_chore(chore_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Chore not found")
    return {"ok": True}

@router.delete("/{chore_id}")
async def delete_chore(chore_id: str, user=Depends(get_current_user)):
    await chore_controller.delete_chore(chore_id)
    return {"ok": True}