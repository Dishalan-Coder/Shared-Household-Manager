from pydantic import BaseModel


class SettlementCreate(BaseModel):
    expense_id: int
    user_id: int
    share_amount: float


class SettlementUpdate(BaseModel):
    is_paid: bool


class SettlementResponse(BaseModel):
    id: int
    expense_id: int
    user_id: int
    share_amount: float
    is_paid: bool

    class Config:
        from_attributes = True