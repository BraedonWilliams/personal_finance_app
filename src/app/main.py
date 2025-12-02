from fastapi import FastAPI

# Now import routes
from src.app.api.routes import auth, accounts, categories, budgets, transactions
from src.app.api.routes.summary import router as summary_router

app = FastAPI()

# Routers
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(transactions.router)
app.include_router(summary_router)


@app.get("/")
def read_root():
    return {"message": "Hello, Personal Finance App!"}
