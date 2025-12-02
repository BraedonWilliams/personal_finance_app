from src.app.db.models.budget import Budget


def update_budget_progress(
    db,
    category_id: int | None,
    amount: float,
    is_income: bool,
    reverse: bool = False,
):
    """
    Updates the budget totals for the given category.

    - Income does NOT affect budgets.
    - reverse=False → apply transaction normally (expense adds to current_spent).
    - reverse=True  → undo transaction (used for update/delete).
    """

    # No category, nothing to do
    if category_id is None:
        return

    # Income transactions don't count toward spending
    if is_income:
        return

    # Find the first budget tied to this category (MVP: one budget per category)
    budget = (
        db.query(Budget)
        .filter(Budget.category_id == category_id)
        .first()
    )
    if not budget:
        return

    # Ensure amount is positive for math
    amount = float(amount)

    if reverse:
        budget.current_spent -= amount
    else:
        budget.current_spent += amount

    # Clamp to zero just in case
    if budget.current_spent < 0:
        budget.current_spent = 0.0

    budget.remaining = float(budget.target_amount) - budget.current_spent

    db.add(budget)
