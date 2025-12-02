from pydantic import BaseModel, EmailStr
from datetime import datetime

#Create a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#Data fetched when a user is created, logged in, etc.
class UserRead(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}

#login(post...sending info)
class UserLogin(BaseModel):
    email: str #so email or username can be used in logging in
    password: str

