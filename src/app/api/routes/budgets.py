from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.app.db.database import get_db
from src.app.db.models.budget import Budget
from src.app.api.schemas.budget import (
    BudgetCreate,
    BudgetRead,
    BudgetUpdate,
)

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(payload: BudgetCreate, db: Session = Depends(get_db)):

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
