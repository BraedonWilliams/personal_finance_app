from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from src.app.api.routes import auth, accounts, categories, budgets, transactions, dashboard
from src.app.api.routes.summary import router as summary_router

app = FastAPI(
    title="Personal Finance App",
    version="1.0.0"
)

# ---------------------------
# CORS (required for frontend)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Routers
# ---------------------------
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(transactions.router)
app.include_router(summary_router)
app.include_router(dashboard.router)

# ---------------------------
# Root endpoint
# ---------------------------
@app.get("/")
def read_root():
    return {"message": "Hello, Personal Finance App!"}
