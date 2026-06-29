from pydantic import BaseModel
from datetime import date, datetime


class ExpenseCreate(BaseModel):
    household_id: int
    title: str
    amount: float
    paid_by: int
    expense_date: date


class ExpenseResponse(BaseModel):
    id: int
    household_id: int
    title: str
    amount: float
    paid_by: int
    expense_date: date
    created_at: datetime

    class Config:
        from_attributes = True