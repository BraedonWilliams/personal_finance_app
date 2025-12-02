from pydantic import BaseModel
from typing import Optional

class BudgetBase(BaseModel):
    name: str
    target_amount: float
    period: str  # monthly, weekly, etc.

class BudgetCreate(BudgetBase):
    user_id: int
    category_id: int

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    period: Optional[str] = None

class BudgetRead(BudgetBase):
    id: int
    user_id: int
    category_id: int

    class Config:
        from_attributes = True
