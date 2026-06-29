from pydantic import BaseModel
from datetime import datetime


class HouseholdCreate(BaseModel):
    household_name: str


class HouseholdJoin(BaseModel):
    invite_code: str


class HouseholdResponse(BaseModel):
    id: int
    household_name: str
    invite_code: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True