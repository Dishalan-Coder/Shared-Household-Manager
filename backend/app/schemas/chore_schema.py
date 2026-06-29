from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ChoreCreate(BaseModel):
    household_id: int
    title: str
    description: Optional[str] = None
    assigned_to: int
    due_date: date


class ChoreUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class ChoreResponse(BaseModel):
    id: int
    household_id: int
    title: str
    description: Optional[str]
    assigned_to: int
    created_by: int
    due_date: date
    status: str
    created_at: datetime

    class Config:
        from_attributes = True