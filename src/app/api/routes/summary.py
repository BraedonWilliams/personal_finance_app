from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import Optional, List

from src.app.db.database import get_db
from src.app.db.models.transaction import Transaction
from src.app.db.models.category import Category
from src.app.db.models.account import Account

router = APIRouter(prefix="/summary", tags=["Summary"])

## GETTING MONTHLY SUMMARY STUFF ##
@router.get("/monthly")
def monthly_summary(
    user_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db),
):
    """
    Returns monthly income, expenses, net, and category breakdown.
    """

    # Month boundaries
    start_date = date(year, month, 1)
    end_date = date(year + (month // 12), ((month % 12) + 1), 1)

    # Fetch transactions for the month
    txns = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
        .all()
    )

    if not txns:
        return {
            "income": 0,
            "expenses": 0,
            "net": 0,
            "category_breakdown": [],
            "account_totals": []
        }

    total_income = 0
    total_expenses = 0

    # Category accumulation
    category_map = {}

    for txn in txns:
        amt = float(txn.amount)

        # Income / Expense logic
        if txn.is_income:
            total_income += amt
        else:
            total_expenses += amt

        # Category breakdown
        if txn.category_id not in category_map:
            category_map[txn.category_id] = {
                "category_id": txn.category_id,
                "category_name": None,  # fill after loop
                "total": 0
            }

        category_map[txn.category_id]["total"] += amt

    # Fill category names
    for cid, entry in category_map.items():
        if cid is not None:
            cat = db.query(Category).filter(Category.id == cid).first()
            entry["category_name"] = cat.name if cat else "Unknown"
        else:
            entry["category_name"] = "Uncategorized"

    # Account totals
    account_totals = (
        db.query(
            Account.id,
            Account.name,
            Account.current_balance
        )
        .filter(Account.user_id == user_id)
        .all()
    )

    return {
        "income": round(total_income, 2),
        "expenses": round(total_expenses, 2),
        "net": round(total_income - total_expenses, 2),
        "category_breakdown": list(category_map.values()),
        "account_totals": [
            {"account_id": a[0], "name": a[1], "balance": float(a[2])}
            for a in account_totals
        ]
    }


## GETTING NET WORTH SUMMARY ##

@router.get("/net-worth")
def net_worth(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Returns total net worth (sum of all account balances).
    """

    accounts = (
        db.query(Account)
        .filter(Account.user_id == user_id)
        .all()
    )

    if not accounts:
        return {
            "net_worth": 0,
            "accounts": []
        }

    total = sum([float(a.current_balance) for a in accounts])

    return {
        "net_worth": round(total, 2),
        "accounts": [
            {
                "account_id": a.id,
                "name": a.name,
                "balance": float(a.current_balance)
            }
            for a in accounts
        ]
    }
