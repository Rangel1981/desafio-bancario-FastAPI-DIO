from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from src.models import TransactionType
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    balance: Decimal

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Decimal = Field(gt=0)


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True