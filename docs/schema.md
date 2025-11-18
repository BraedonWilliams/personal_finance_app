Users
Column Name	Type	Key	Notes
user_id		SERIAL	PK	Auto-increment
username	VARCHAR(50)		Unique
email		VARCHAR(100)		Unique
password_hash	VARCHAR(255)		
created_at	TIMESTAMP		Default NOW()

Relationships:

One user → many accounts

Accounts
Column Name		Type		Key	Notes
account_id		SERIAL		PK	Auto-increment
user_id			INT		FK	References Users.user_id
account_name		VARCHAR(100)		
account_type		VARCHAR(50)		e.g., checking, cash, investment
starting_balance	DECIMAL		
current_balance		DECIMAL		
created_at		TIMESTAMP		Default NOW()

Relationships:

One account → many transactions

One account → many budget goals via AccountBudgetGoal

Transactions
Column Name		Type	Key	Notes
transaction_id		SERIAL	PK	Auto-increment
account_id		INT	FK	References Accounts.account_id
category_id		INT	FK	References Categories.category_id
amount			DECIMAL		
transaction_type	VARCHAR(20)	e.g., income, expense
description		VARCHAR(255)		
timestamp	TIMESTAMP		
notes	TEXT		Optional notes

Relationships:

Belongs to one account

Belongs to one category

Categories
Column Name	Type		Key	Notes
category_id	SERIAL		PK	Auto-increment
category_name	VARCHAR(50)		e.g., groceries, gym
category_type	VARCHAR(20)		income or expense
created_at	TIMESTAMP		Default NOW()

Relationships:

One category → many transactions

One category → one budget goal

BudgetGoals
Column Name		Type	Key	Notes
goal_id			SERIAL	PK	Auto-increment
category_id		INT	FK	References Categories.category_id
goal_name		VARCHAR(100)		
target_amount		DECIMAL		
current_progress	DECIMAL		Optional, could sum from join table
start_date		DATE		
end_date		DATE		
is_complete		BOOLEAN		Default FALSE

Relationships:

One budget goal → one category

Many budget goals → many accounts via AccountBudgetGoal

AccountBudgetGoals (Join Table)
Column Name		Type	Key	Notes
acct_budget_goal_id	SERIAL	PK	Auto-increment
account_id		INT	FK	References Accounts.account_id
goal_id			INT	FK	References BudgetGoals.goal_id
current_progress	DECIMAL		Progress of this goal for this account

Relationships:

Many AccountBudgetGoals → one Account

Many AccountBudgetGoals → one BudgetGoal

Purpose:

Enables many-to-many relationship between BudgetGoals and Accounts

Tracks per-account contribution to a goal for consolidated budgeting
