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
    """
    reverse=False → apply normally
    reverse=True  → undo (used for update/delete)
    """

    # Ensure float
    amount = float(amount)

    if reverse:
        # Undo previous transaction
        if is_income:
            account.current_balance -= amount
        else:
            account.current_balance += amount
    else:
        # Apply new transaction
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

    # Get the account to update balance
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

    # 🔥 Update the account balance
    apply_balance_change(
        db,
        account=account,
        amount=float(payload.amount),
        is_income=payload.is_income,
        reverse=False,
    )

    # 🔥 Update any linked budget for this category
    update_budget_progress(
        db=db,
        category_id=payload.category_id,
        amount=float(payload.amount),
        is_income=payload.is_income,
        reverse=False,
    )

    db.commit()
    db.refresh(transaction)
    return transaction





# -------------------------
# Get single Transaction
# -------------------------
@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
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

    # Fetch existing transaction
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(404, "Transaction not found")

    # --- OLD values (before update) ---
    old_account = db.query(Account).filter(Account.id == transaction.account_id).first()
    if not old_account:
        raise HTTPException(404, "Account not found")

    old_amount = float(transaction.amount)
    old_is_income = transaction.is_income
    old_category_id = transaction.category_id

    # 🔥 Undo the old transaction effect on OLD account
    apply_balance_change(
        db,
        account=old_account,
        amount=old_amount,
        is_income=old_is_income,
        reverse=True,
    )

    # 🔥 Undo the old effect on any budget (if expense + has category)
    update_budget_progress(
        db=db,
        category_id=old_category_id,
        amount=old_amount,
        is_income=old_is_income,
        reverse=True,
    )

    # --- Apply incoming updates to the transaction object ---
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(transaction, key, value)

    # Re-fetch account (in case account_id changed)
    new_account = old_account
    if payload.account_id is not None and payload.account_id != old_account.id:
        new_account = db.query(Account).filter(Account.id == payload.account_id).first()
        if not new_account:
            raise HTTPException(404, "New account not found")
        transaction.account_id = payload.account_id

    # 🔥 Apply NEW transaction effect to NEW account
    apply_balance_change(
        db,
        account=new_account,
        amount=float(transaction.amount),
        is_income=transaction.is_income,
        reverse=False,
    )

    # 🔥 Apply NEW effect to budget (if applicable)
    update_budget_progress(
        db=db,
        category_id=transaction.category_id,
        amount=float(transaction.amount),
        is_income=transaction.is_income,
        reverse=False,
    )

    db.commit()
    db.refresh(transaction)
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
    if not account:
        raise HTTPException(404, "Account not found")

    # 🔥 Reverse the balance effect on account
    apply_balance_change(
        db,
        account=account,
        amount=float(transaction.amount),
        is_income=transaction.is_income,
        reverse=True,
    )

    # 🔥 Reverse the budget effect
    update_budget_progress(
        db=db,
        category_id=transaction.category_id,
        amount=float(transaction.amount),
        is_income=transaction.is_income,
        reverse=True,
    )

    db.delete(transaction)
    db.commit()
    return None

@router.get("/", response_model=List[TransactionRead])
def list_transactions(
    user_id: int,
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_income: Optional[bool] = None,
    min_date: Optional[str] = None,       # YYYY-MM-DD
    max_date: Optional[str] = None,       # YYYY-MM-DD
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "date_desc",    # 'date_desc', 'date_asc', 'amount_desc', 'amount_asc'
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    # ---- FILTERING ----
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

    # ---- SEARCH (description & category name) ----
    if search:
        search_term = f"%{search.lower()}%"
        query = (
            query.join(Category, isouter=True)
                 .filter(
                     (Transaction.description.ilike(search_term)) |
                     (Category.name.ilike(search_term))
                 )
        )

    # ---- SORTING ----
    sort_map = {
        "date_desc": Transaction.date.desc(),
        "date_asc": Transaction.date.asc(),
        "amount_desc": Transaction.amount.desc(),
        "amount_asc": Transaction.amount.asc(),
    }
    query = query.order_by(sort_map.get(sort, Transaction.date.desc()))

    # ---- PAGINATION ----
    transactions = query.offset(offset).limit(limit).all()
    return transactions

