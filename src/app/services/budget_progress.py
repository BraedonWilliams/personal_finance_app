from src.app.db.models.budget import Budget
from src.app.db.models.account_budget import AccountBudget


def update_budget_progress(db, transaction):
    # Only update budgets for expenses
    if transaction.is_income:
        return

    # Find the budget linked to this transaction
    budget = db.query(Budget).filter(
        Budget.category_id == transaction.category_id
    ).first()

    if not budget:
        return

    # Add to overall budget progress
    budget.current_spent += float(transaction.amount)
    budget.remaining = budget.target_amount - budget.current_spent

    # Update per-account progress
    acc_budget = db.query(AccountBudget).filter(
        AccountBudget.account_id == transaction.account_id,
        AccountBudget.budget_id == budget.id
    ).first()

    if acc_budget:
        acc_budget.current_progress += float(transaction.amount)

    db.commit()
    db.refresh(budget)

