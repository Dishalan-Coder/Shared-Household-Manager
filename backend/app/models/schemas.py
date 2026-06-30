from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class HouseholdCreate(BaseModel):
    name: str

class JoinHousehold(BaseModel):
    invite_code: str

class ChoreCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: str
    assigned_to: str
    frequency: Optional[str] = "none"  
    rotation_members: Optional[List[str]] = []

class GroceryCreate(BaseModel):
    name: str
    quantity: Optional[int] = 1

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    payer_id: str
    split_between: List[str]
    date: Optional[str] = None