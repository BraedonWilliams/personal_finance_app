from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.app.db.database import get_db
from src.app.db.models.budget import Budget
from src.app.db.models.account import Account
from src.app.db.models.account_budget import AccountBudget


from src.app.api.schemas.budget import (
    BudgetCreate,
    BudgetRead,
    BudgetUpdate,
)

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(payload: BudgetCreate, db: Session = Depends(get_db)):

    # 1. Create the Budget
    budget = Budget(
        name=payload.name,
        target_amount=payload.target_amount,
        period=payload.period,
        user_id=payload.user_id,
        category_id=payload.category_id
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    # 2. Get all accounts owned by this user
    user_accounts = db.query(Account).filter(Account.user_id == payload.user_id).all()

    # 3. Create AccountBudget rows for each account
    for account in user_accounts:
        link = AccountBudget(
            account_id=account.id,
            budget_id=budget.id,
            current_progress=0.0
        )
        db.add(link)

    db.commit()  # save account-budget links

    # Optional but recommended
    db.refresh(budget)

    return budget





@router.get("/", response_model=List[BudgetRead])
def list_budgets(user_id: int, db: Session = Depends(get_db)):
    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .all()
    )
    return budgets


@router.get("/{budget_id}", response_model=BudgetRead)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )
    return budget


@router.patch("/{budget_id}", response_model=BudgetRead)
def update_budget(
    budget_id: int,
    payload: BudgetUpdate,
    db: Session = Depends(get_db),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(budget, key, value)

    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    db.delete(budget)
    db.commit()
    return None

@router.get("/{budget_id}/progress")
def get_budget_progress(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(404, "Budget not found")

    percent_used = (
        (budget.current_spent / budget.target_amount) * 100
        if budget.target_amount > 0 else 0
    )

    return {
        "budget_id": budget.id,
        "name": budget.name,
        "target_amount": budget.target_amount,
        "current_spent": budget.current_spent,
        "remaining": budget.remaining,
        "percent_used": round(percent_used, 2),
    }

