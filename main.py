from fastapi import FastAPI

# 👇 THIS is required so Python can find your src/app folder
import sys
sys.path.append("src")

from src.app.api.routes.user import router as auth_router
# when you add more:
# from app.api.user_routes import router as user_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello personal finance"}

# 👇 REGISTER YOUR ROUTES HERE
app.include_router(auth_router)
# app.include_router(user_router)   # later
