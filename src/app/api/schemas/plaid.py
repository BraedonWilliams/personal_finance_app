from pydantic import BaseModel
from typing import List, Optional


class PlaidLinkToken(BaseModel):
    link_token: str


class PlaidPublicToken(BaseModel):
    public_token: str


class AccountBase(BaseModel):
    account_id: str
    name: str
    official_name: str | None = None
    type: str
    subtype: str | None = None
    mask: str | None = None
    current_balance: float | None = None
    available_balance: float | None = None


class AccountList(BaseModel):
    accounts: List[AccountBase]


class TransactionBase(BaseModel):
    transaction_id: str
    date: str
    name: str
    amount: float
    account_id: str
    category: Optional[List[str]] = None
    pending: bool = False


class TransactionList(BaseModel):
    transactions: List[TransactionBase]
