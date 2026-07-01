import re
from pydantic import BaseModel, field_validator
from typing import List, Optional

# Same rule used on the frontend: local-part@domain.tld
EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")


def _validate_email_format(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError("Email is required")
    if "@" not in value:
        raise ValueError('Email must contain "@"')
    if not EMAIL_REGEX.match(value):
        raise ValueError("Enter a valid email address (e.g. name@example.com)")
    return value.lower()


def _validate_password_strength(value: str) -> str:
    value = value or ""
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least 1 uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least 1 lowercase letter")
    if not re.search(r"[0-9]", value):
        raise ValueError("Password must contain at least 1 number")
    if not re.search(r"[^A-Za-z0-9]", value):
        raise ValueError("Password must contain at least 1 special character")
    return value


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        value = (value or "").strip()
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        return value

    @field_validator("email")
    @classmethod
    def email_valid(cls, value: str) -> str:
        return _validate_email_format(value)

    @field_validator("password")
    @classmethod
    def password_strong(cls, value: str) -> str:
        return _validate_password_strength(value)


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, value: str) -> str:
        return _validate_email_format(value)

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("Password is required")
        return value

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