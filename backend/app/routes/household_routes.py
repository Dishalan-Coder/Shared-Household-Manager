from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import HouseholdCreate, JoinHousehold
from ..controllers import household_controller
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/households", tags=["households"])

@router.post("/")
async def create_household(payload: HouseholdCreate, user=Depends(get_current_user)):
    return await household_controller.create_household(payload.name, user["id"])

@router.post("/join")
async def join_household(payload: JoinHousehold, user=Depends(get_current_user)):
    res = await household_controller.join_household(payload.invite_code, user["id"])
    if not res:
        raise HTTPException(status_code=404, detail="Invalid invite code")
    return res

@router.get("/me")
async def my_household(user=Depends(get_current_user)):
    return await household_controller.get_user_household(user["id"])