from pydantic import BaseModel
from typing import Optional
from datetime import date as dt_date


class TransactionBase(BaseModel):
    amount: float                 # negative for expense, positive for income OR use is_income
    date: dt_date
    description: Optional[str] = None
    is_income: bool = False       # True if this is income


class TransactionCreate(TransactionBase):
    user_id: int
    account_id: int
    category_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[dt_date] = None
    description: Optional[str] = None
    is_income: Optional[bool] = None
    category_id: Optional[int] = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int
    account_id: int
    category_id: Optional[int] = None

    class Config:
        from_attributes = True
        orm_mode = True
