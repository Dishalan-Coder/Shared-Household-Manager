from fastapi import APIRouter, Depends, HTTPException
from ..models.schemas import GroceryCreate
from ..controllers import grocery_controller
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/groceries", tags=["groceries"])

@router.post("/")
async def add_grocery(payload: GroceryCreate, user=Depends(get_current_user)):
    if not user.get("household_id"):
        raise HTTPException(status_code=400, detail="Join a household first")
    gid = await grocery_controller.add_grocery_item(
        user["household_id"], payload.name, user["id"], payload.quantity
    )
    return {"id": gid}

@router.get("/")
async def list_groceries(user=Depends(get_current_user)):
    if not user.get("household_id"):
        return []
    return await grocery_controller.get_groceries(user["household_id"])

@router.patch("/{item_id}")
async def toggle_grocery(item_id: str, body: dict, user=Depends(get_current_user)):
    await grocery_controller.toggle_grocery(item_id, body.get("checked", False))
    return {"ok": True}

@router.delete("/{item_id}")
async def delete_grocery(item_id: str, user=Depends(get_current_user)):
    await grocery_controller.delete_grocery(item_id)
    return {"ok": True}