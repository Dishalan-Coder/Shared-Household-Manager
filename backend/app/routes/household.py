from fastapi import APIRouter

router = APIRouter(
    prefix="/household",
    tags=["Household"]
)


@router.post("/create")
async def create_household():
    return {
        "message": "Household Created Successfully"
    }


@router.post("/join")
async def join_household():
    return {
        "message": "Joined Household Successfully"
    }


@router.get("/")
async def get_household():
    return {
        "message": "Household Details"
    }