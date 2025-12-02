from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    user_id: int  # if you decide categories are per-user; otherwise drop this


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        orm_mode = True
