from fastapi import FastAPI
from src.app.api.routes import auth, user, accounts, categories, budgets, transactions
# from api.routes import plaid

app = FastAPI()

#routers
app.include_router(auth.router)
app.include_router(user.router) #, prefix="/users", tags=["Users"]
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Hello, Personal Finance App!"}


# app.include_router(plaid.router)
