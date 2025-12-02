from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.app.db.database import get_db
from src.app.db.models.account import Account
from src.app.api.schemas.account import (
    AccountCreate,
    AccountRead,
    AccountUpdate,
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


# -------------------------------------------------------------
# Create Account
# -------------------------------------------------------------
@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):

    account = Account(
        name=payload.name,
        type=payload.type,
        description=payload.description,
        user_id=payload.user_id,

        # Correct, modern column names
        starting_balance=payload.starting_balance,
        current_balance=payload.starting_balance,
    )

    db.add(account)
    db.commit()
    db.refresh(account)
    return account



# -------------------------------------------------------------
# List Accounts (by user_id)
# -------------------------------------------------------------
@router.get("/", response_model=List[AccountRead])
def list_accounts(user_id: int, db: Session = Depends(get_db)):
    accounts = (
        db.query(Account)
        .filter(Account.user_id == user_id)
        .all()
    )
    return accounts


# -------------------------------------------------------------
# Get Single Account
# -------------------------------------------------------------
@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account


# -------------------------------------------------------------
# Update Account
# (only name, type, description can be patched)
# -------------------------------------------------------------
@router.patch("/{account_id}", response_model=AccountRead)
def update_account(
    account_id: int,
    payload: AccountUpdate,
    db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    update_data = payload.dict(exclude_unset=True)

    # Only allow updating fields that ACTUALLY exist in the model
    allowed_fields = ["name", "type", "description"]
    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(account, key, value)

    db.commit()
    db.refresh(account)
    return account


# -------------------------------------------------------------
# Delete Account
# -------------------------------------------------------------
@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    db.delete(account)
    db.commit()
    return None

