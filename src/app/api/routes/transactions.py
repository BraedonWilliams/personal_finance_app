from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.app.db.database import get_db
from src.app.db.models.account import Account
from src.app.db.models.transaction import Transaction
from src.app.api.schemas.transaction import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from src.app.db.models.category import Category

from src.app.services.budget_progress import update_budget_progress


router = APIRouter(prefix="/transactions", tags=["Transactions"])


# -------------------------
# Helper: account balances
# -------------------------
def apply_balance_change(
    db: Session,
    account: Account,
    amount: float,
    is_income: bool,
    reverse: bool = False,
) -> None:

    amount = float(amount)

    if reverse:
        if is_income:
            account.current_balance -= amount
        else:
            account.current_balance += amount
    else:
        if is_income:
            account.current_balance += amount
        else:
            account.current_balance -= amount

    db.add(account)


# -------------------------
# Create Transaction
# -------------------------
@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):

    account = db.query(Account).filter(Account.id == payload.account_id).first()
    if not account:
        raise HTTPException(404, "Account not found")

    transaction = Transaction(
        amount=payload.amount,
        date=payload.date,
        description=payload.description,
        is_income=payload.is_income,
        user_id=payload.user_id,
        account_id=payload.account_id,
        category_id=payload.category_id,
    )

    db.add(transaction)

    # 🔥 Update account
    apply_balance_change(
        db,
        account=account,
        amount=float(payload.amount),
        is_income=payload.is_income,
        reverse=False,
    )

    db.commit()
    db.refresh(transaction)

    # 🔥 FIXED FOR NEW BUDGET LOGIC
    update_budget_progress(db, transaction)

    return transaction


# -------------------------
# Get single Transaction
# -------------------------
@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(404, "Transaction not found")
    return transaction


# -------------------------
# Update Transaction
# -------------------------
@router.patch("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(404, "Transaction not found")

    # OLD values before update
    old_account = db.query(Account).filter(Account.id == transaction.account_id).first()
    old_amount = float(transaction.amount)
    old_is_income = transaction.is_income

    # 🔥 Undo old account effect
    apply_balance_change(
        db,
        account=old_account,
        amount=old_amount,
        is_income=old_is_income,
        reverse=True,
    )

    db.commit()
    db.refresh(transaction)

    # 🔥 FIXED FOR NEW BUDGET LOGIC
    update_budget_progress(db, transaction)

    # Apply updates
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(transaction, key, value)

    # Re-fetch new account if it changed
    new_account = db.query(Account).filter(Account.id == transaction.account_id).first()

    # Apply NEW account change
    apply_balance_change(
        db,
        account=new_account,
        amount=float(transaction.amount),
        is_income=transaction.is_income,
        reverse=False,
    )

    db.commit()
    db.refresh(transaction)

    # 🔥 FIXED FOR NEW BUDGET LOGIC
    update_budget_progress(db, transaction)

    return transaction


# -------------------------
# Delete Transaction
# -------------------------
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(404, "Transaction not found")

    account = db.query(Account).filter(Account.id == transaction.account_id).first()

    # 🔥 Undo account effect
    apply_balance_change(
        db,
        account=account,
        amount=float(transaction.amount),
        is_income=transaction.is_income,
        reverse=True,
    )

    db.commit()

    # 🔥 FIXED FOR NEW BUDGET LOGIC
    update_budget_progress(db, transaction)

    db.delete(transaction)
    db.commit()

    return None


# -------------------------
# List Transactions
# -------------------------
@router.get("/", response_model=List[TransactionRead])
def list_transactions(
    user_id: int,
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_income: Optional[bool] = None,
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "date_desc",
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if account_id is not None:
        query = query.filter(Transaction.account_id == account_id)

    if category_id is not None:
        query = query.filter(Transaction.category_id == category_id)

    if is_income is not None:
        query = query.filter(Transaction.is_income == is_income)

    if min_date:
        query = query.filter(Transaction.date >= min_date)

    if max_date:
        query = query.filter(Transaction.date <= max_date)

    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    if search:
        search_term = f"%{search.lower()}%"
        query = (
            query.join(Category, isouter=True)
                 .filter(
                     (Transaction.description.ilike(search_term)) |
                     (Category.name.ilike(search_term))
                 )
        )

    sort_map = {
        "date_desc": Transaction.date.desc(),
        "date_asc": Transaction.date.asc(),
        "amount_desc": Transaction.amount.desc(),
        "amount_asc": Transaction.amount.asc(),
    }
    query = query.order_by(sort_map.get(sort, Transaction.date.desc()))

    return query.offset(offset).limit(limit).all()
