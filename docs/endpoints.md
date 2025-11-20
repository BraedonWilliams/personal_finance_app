Auth
1. Sign Up

URL: /auth/signup
Method: POST
Description: Creates a new user account.

Request Body (JSON):

{
  "username": "example",
  "email": "example@example.com",
  "password": "password123"
}


Response (JSON):

{
  "user_id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Missing required field

409 → Username or email already exists

2. Login

URL: /auth/login
Method: POST
Description: Authenticates a user with email and password.

Request Body (JSON):

{
  "email": "example@example.com",
  "password": "password123"
}


Response (JSON):

{
  "message": "Login successful",
  "user_id": 1
}


Errors:

400 → Missing required field

401 → Invalid email or password

Users
1. Create User

URL: /users
Method: POST
Description: Creates a new user account.

Request Body (JSON):

{
  "username": "example",
  "email": "example@example.com",
  "password": "password123"
}


Response (JSON):

{
  "user_id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Missing required field

409 → Username or email already exists

2. Get User by ID

URL: /users/:id
Method: GET
Description: Retrieves user information by user ID.

Response (JSON):

{
  "user_id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

404 → User not found

3. Update User

URL: /users/:id
Method: PATCH
Description: Updates user information (username, email, or password).

Request Body (JSON):

{
  "username": "example2",
  "email": "example2@example.com"
}


Response (JSON):

{
  "user_id": 1,
  "username": "example2",
  "email": "example2@example.com",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Invalid input

404 → User not found

409 → Username or email already exists

4. Delete User

URL: /users/:id
Method: DELETE
Description: Deletes a user account and all associated accounts, transactions, and budgets.

Response (JSON):

{
  "message": "User successfully deleted"
}


Errors:

404 → User not found

5. Get All Accounts for a User

URL: /users/:id/accounts
Method: GET
Description: Retrieves all financial accounts for a specific user.

Response (JSON):

[
  {
    "account_id": 1,
    "user_id": 1,
    "account_name": "Chase Checking",
    "account_type": "checking",
    "starting_balance": 1000,
    "current_balance": 1200,
    "created_at": "2025-11-17T17:30:00Z"
  },
  {
    "account_id": 2,
    "user_id": 1,
    "account_name": "Robinhood",
    "account_type": "investment",
    "starting_balance": 5000,
    "current_balance": 5500,
    "created_at": "2025-11-17T17:31:00Z"
  }
]


Errors:

404 → User not found

6. Get All BudgetGoals for a User

URL: /users/:id/budget-goals
Method: GET
Description: Retrieves all budget goals for a specific user.

Response (JSON):

[
  {
    "goal_id": 1,
    "goal_name": "Groceries",
    "category_id": 1,
    "target_amount": 500,
    "total_current_progress": 350,
    "start_date": "2025-11-01",
    "end_date": "2025-11-30",
    "is_complete": false,
    "accounts": [
      {
        "account_id": 1,
        "account_name": "Chase Checking",
        "current_progress": 200
      },
      {
        "account_id": 2,
        "account_name": "Cash Wallet",
        "current_progress": 150
      }
    ]
  },
  {
    "goal_id": 2,
    "goal_name": "Entertainment",
    "category_id": 2,
    "target_amount": 200,
    "total_current_progress": 75,
    "start_date": "2025-11-01",
    "end_date": "2025-11-30",
    "is_complete": false,
    "accounts": [
      {
        "account_id": 1,
        "account_name": "Chase Checking",
        "current_progress": 75
      }
    ]
  }
]


Errors:

404 → User not found

7. Get All Transactions for a User

URL: /users/:id/transactions
Method: GET
Description: Retrieves all transactions for a specific user across all accounts.

Response (JSON):

[
  {
    "transaction_id": 101,
    "account_id": 1,
    "account_name": "Chase Checking",
    "category_id": 1,
    "category_name": "Groceries",
    "amount": 50,
    "transaction_type": "expense",
    "description": "Supermarket",
    "timestamp": "2025-11-15T14:20:00Z",
    "notes": ""
  },
  {
    "transaction_id": 102,
    "account_id": 2,
    "account_name": "Cash Wallet",
    "category_id": 1,
    "category_name": "Groceries",
    "amount": 25,
    "transaction_type": "expense",
    "description": "Farmer’s Market",
    "timestamp": "2025-11-16T10:30:00Z",
    "notes": ""
  },
  {
    "transaction_id": 103,
    "account_id": 1,
    "account_name": "Chase Checking",
    "category_id": 2,
    "category_name": "Entertainment",
    "amount": 30,
    "transaction_type": "expense",
    "description": "Movie",
    "timestamp": "2025-11-16T20:00:00Z",
    "notes": ""
  }
]


Errors:

404 → User not found

Accounts
1. Create Account

URL: /accounts
Method: POST

Request Body (JSON):

{
  "user_id": 1,
  "account_name": "Chase Checking",
  "account_type": "checking",
  "starting_balance": 1000
}


Response (JSON):

{
  "account_id": 1,
  "user_id": 1,
  "account_name": "Chase Checking",
  "account_type": "checking",
  "starting_balance": 1000,
  "current_balance": 1000,
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Missing required field

2. Get Account by ID

URL: /accounts/:id
Method: GET

Response (JSON):

{
  "account_id": 1,
  "user_id": 1,
  "account_name": "Chase Checking",
  "account_type": "checking",
  "starting_balance": 1000,
  "current_balance": 1000,
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

404 → Account not found

3. Update Account

URL: /accounts/:id
Method: PATCH

Request Body (JSON):

{
  "account_name": "Chase Checking Updated"
}


Response (JSON):

{
  "account_id": 1,
  "user_id": 1,
  "account_name": "Chase Checking Updated",
  "account_type": "checking",
  "starting_balance": 1000,
  "current_balance": 1000,
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Invalid input

404 → Account not found

4. Delete Account

URL: /accounts/:id
Method: DELETE

Response (JSON):

{
  "message": "Account successfully deleted"
}


Errors:

404 → Account not found

Categories
1. Create Category

URL: /categories
Method: POST

Request Body (JSON):

{
  "category_name": "Groceries",
  "category_type": "expense"
}


Response (JSON):

{
  "category_id": 1,
  "category_name": "Groceries",
  "category_type": "expense",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Missing required field

2. Get Category by ID

URL: /categories/:id
Method: GET

Response (JSON):

{
  "category_id": 1,
  "category_name": "Groceries",
  "category_type": "expense",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

404 → Category not found

3. Update Category

URL: /categories/:id
Method: PATCH

Request Body (JSON):

{
  "category_name": "Supermarket"
}


Response (JSON):

{
  "category_id": 1,
  "category_name": "Supermarket",
  "category_type": "expense",
  "created_at": "2025-11-17T17:30:00Z"
}


Errors:

400 → Invalid input

404 → Category not found

4. Delete Category

URL: /categories/:id
Method: DELETE

Response (JSON):

{
  "message": "Category successfully deleted"
}


Errors:

404 → Category not found

BudgetGoals
1. Create BudgetGoal

URL: /budget-goals
Method: POST

Request Body (JSON):

{
  "goal_name": "Groceries",
  "category_id": 1,
  "target_amount": 500,
  "start_date": "2025-11-01",
  "end_date": "2025-11-30"
}


Response (JSON):

{
  "goal_id": 1,
  "goal_name": "Groceries",
  "category_id": 1,
  "target_amount": 500,
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "is_complete": false
}


Errors:

400 → Missing required field

2. Get BudgetGoal by ID

URL: /budget-goals/:id
Method: GET

Response (JSON):

{
  "goal_id": 1,
  "goal_name": "Groceries",
  "category_id": 1,
  "target_amount": 500,
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "is_complete": false
}


Errors:

404 → BudgetGoal not found

3. Update BudgetGoal

URL: /budget-goals/:id
Method: PATCH

Request Body (JSON):

{
  "target_amount": 600
}


Response (JSON):

{
  "goal_id": 1,
  "goal_name": "Groceries",
  "category_id": 1,
  "target_amount": 600,
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "is_complete": false
}


Errors:

400 → Invalid input

404 → BudgetGoal not found

4. Delete BudgetGoal

URL: /budget-goals/:id
Method: DELETE

Response (JSON):

{
  "message": "BudgetGoal successfully deleted"
}


Errors:

404 → BudgetGoal not found

AccountBudgetGoals
1. Update Progress

URL: /account-budget-goals/:id/progress
Method: PATCH
Description: Updates progress of a budget goal for a specific account.

Request Body (JSON):

{
  "current_progress": 250
}


Response (JSON):

{
  "account_budget_goal_id": 1,
  "goal_id": 1,
  "account_id": 12,
  "current_progress": 250
}


Errors:

404 → AccountBudgetGoal not found
