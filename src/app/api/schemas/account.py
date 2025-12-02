from pydantic import BaseModel
from typing import Optional


class AccountBase(BaseModel):
    name: str
    type: Optional[str] = None   # e.g. "cash", "checking", "savings", etc.
    description: Optional[str] = None


class AccountCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    user_id: int
    starting_balance: float




class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None


class AccountRead(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str]
    user_id: int
    starting_balance: float
    current_balance: float

    
