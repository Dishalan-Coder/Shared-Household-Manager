from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GroceryCreate(BaseModel):
    household_id: int
    item_name: str
    quantity: str


class GroceryUpdate(BaseModel):
    item_name: Optional[str] = None
    quantity: Optional[str] = None
    is_checked: Optional[bool] = None


class GroceryResponse(BaseModel):
    id: int
    household_id: int
    item_name: str
    quantity: str
    added_by: int
    is_checked: bool
    created_at: datetime

    class Config:
        from_attributes = True