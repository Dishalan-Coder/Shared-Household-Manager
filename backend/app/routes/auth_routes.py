from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import UserCreate, UserLogin
from ..controllers import auth_controller
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def register(payload: UserCreate):
    res = await auth_controller.register(payload.name, payload.email, payload.password)
    if not res:
        raise HTTPException(status_code=400, detail="Email already registered")
    return res

@router.post("/login")
async def login(payload: UserLogin):
    res = await auth_controller.login(payload.email, payload.password)
    if not res:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return res

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {"id": user["id"], "name": user["name"], "email": user["email"]}