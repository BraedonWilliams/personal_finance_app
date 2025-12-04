from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import date

from src.app.db.database import get_db
from src.app.db.models.transaction import Transaction
from src.app.db.models.category import Category
from src.app.db.models.budget import Budget

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ---------------------------------------------------
# A) SUMMARY: income, expenses, net for THIS month
# ---------------------------------------------------
@router.get("/summary")
def dashboard_summary(user_id: int, db: Session = Depends(get_db)):
    today = date.today()
    month = today.month
    year = today.year

    income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.is_income == True,
            Transaction.date.isnot(None),
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year,
        )
        .scalar()
    )

    expenses = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.is_income == False,
            Transaction.date.isnot(None),
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year,
        )
        .scalar()
    )

    income_val = float(income or 0)
    expenses_val = float(expenses or 0)

    return {
        "income": income_val,
        "expenses": expenses_val,
        "net": income_val - expenses_val,
        "month": f"{year}-{str(month).zfill(2)}",
    }


# ---------------------------------------------------
# B) CATEGORY TOTALS (this month)
# ---------------------------------------------------
@router.get("/by-category")
def dashboard_by_category(user_id: int, db: Session = Depends(get_db)):
    today = date.today()
    month = today.month
    year = today.year

    results = (
        db.query(
            Category.name.label("category"),
            func.coalesce(func.sum(Transaction.amount), 0).label("total"),
        )
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(
            Transaction.user_id == user_id,
            Transaction.is_income == False,
            Transaction.date.isnot(None),
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year,
        )
        .group_by(Category.name)
        .all()
    )

    return [
        {"category": r.category, "total": float(r.total or 0)}
        for r in results
    ]


# ---------------------------------------------------
# C) MONTHLY TOTALS (12 months)
# ---------------------------------------------------
@router.get("/by-month")
def dashboard_by_month(user_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            extract("year", Transaction.date).label("year"),
            extract("month", Transaction.date).label("month"),
            func.sum(
                case(
                    (Transaction.is_income == True, Transaction.amount),
                    else_=0,
                )
            ).label("income"),
            func.sum(
                case(
                    (Transaction.is_income == False, Transaction.amount),
                    else_=0,
                )
            ).label("expenses"),
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.date.isnot(None),
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .limit(12)
        .all()
    )

    formatted = []
    for r in results:
        formatted.append({
            "month": f"{int(r.year)}-{str(int(r.month)).zfill(2)}",
            "income": float(r.income or 0),
            "expenses": float(r.expenses or 0),
        })

    return formatted


# ---------------------------------------------------
# D) BUDGET SUMMARY (for dashboard cards / bars)
# ---------------------------------------------------
@router.get("/budget-summary")
def dashboard_budget_summary(user_id: int, db: Session = Depends(get_db)):
    # all budgets for this user
    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .all()
    )

    today = date.today()
    month = today.month
    year = today.year

    summary = []

    for b in budgets:
        spent = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.category_id == b.category_id,
                Transaction.is_income == False,
                Transaction.date.isnot(None),
                extract("month", Transaction.date) == month,
                extract("year", Transaction.date) == year,
            )
            .scalar()
        )

        spent_val = float(spent or 0)
        target_val = float(b.target_amount or 0)

        pct = (spent_val / target_val * 100) if target_val > 0 else 0.0

        summary.append({
            "budget_id": b.id,
            "name": b.name,
            "target": target_val,
            "spent": spent_val,
            "pct": round(pct, 2),
        })

    return summary
