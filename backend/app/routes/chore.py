from fastapi import APIRouter

router = APIRouter(
    prefix="/chores",
    tags=["Chores"]
)


@router.post("/")
async def add_chore():
    return {
        "message": "Chore Added Successfully"
    }


@router.get("/")
async def get_all_chores():
    return {
        "message": "All Chores"
    }


@router.put("/{chore_id}")
async def update_chore(chore_id: str):
    return {
        "message": f"Chore {chore_id} Updated"
    }


@router.delete("/{chore_id}")
async def delete_chore(chore_id: str):
    return {
        "message": f"Chore {chore_id} Deleted"
    }