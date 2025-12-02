from pydantic import BaseModel
from typing import Optional


class BudgetBase(BaseModel):
    name: str
    target_amount: float          # e.g. 300 for "Groceries $300"
    period: str = "monthly"       # "monthly", "weekly", etc.


class BudgetCreate(BudgetBase):
    user_id: int
    category_id: int


class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    period: Optional[str] = None
    category_id: Optional[int] = None


class BudgetRead(BudgetBase):
    id: int
    user_id: int
    category_id: int
    current_spent: float
    remaining: float

    
