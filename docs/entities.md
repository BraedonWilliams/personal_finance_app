# Entities

## User
Represents an application user.

**Primary Key**
- user_id

**Attributes**
- username
- password_hash
- email
- created_at

**Relationships**
- One user → many accounts


## Account
A financial account that stores balances and transactions (Chase, Robinhood, Cash, etc.)

**Primary Key**
- account_id

**Foreign Keys**
- user_id → User.user_id

**Attributes**
- account_name
- account_type
- starting_balance
- current_balance
- created_at

**Relationships**
- One account → many transactions
- One account → many budget goals via AccountBudgetGoal


## Transaction
Represents any money movement within an account.

**Primary Key**
- transaction_id

**Foreign Keys**
- account_id → Account.account_id
- category_id → Category.category_id

**Attributes**
- amount
- timestamp
- description
- transaction_type
- notes

**Relationships**
- Belongs to one account
- Belongs to one category

## Category
Represents categories of income/expenses (Groceries, gym, lifestyle, etc.)

**Primary Key**
- category_id

**Attributes**
- category_name (groceries, gym, yada yada)
- category_type (income/expense)
- created_at

**Relationships**
- One category → many transactions
- One category → one budget goal


## BudgetGoals
Represents categorized budgeting goals determined by the user
Should make it possible to create long term goals. Such as 8% increase in salary w/in 3 years or wtvr

**Primary Key**
- goal_id

**Foreign Keys**
- category_id → Category.category_id

**Attributes**
- goal_name
- target_amnt
- start_date
- end_date
- is_complete

**Relationships**
- One budget goal → one category
- Many budget goals → many accounts via AccountBudgetGoal


# AccountBudgetGoals (Join Table)
Join Table between Budget Goals and Accounts that makes it possible to track overall budget
for a category across different accounts

**Primary Key**
- acct_budget_goal

**Foreign Keys**
- goal_id → BudgetGoal.goal_id
- account_id → Account.account_id

**Attributes**
- current_progress (how much of the budget has been used for this account)

**Relationships**
- Many Account Budget Goals → one Budget Goal
- Many Account Budget Goals → one Account
(Enables many-many between BudgetGoal and Account)
