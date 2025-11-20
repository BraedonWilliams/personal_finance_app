from pydantic import BaseModel, EmailStr
import datetime

#Create a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#Data fetched when a user is created, logged in, etc.
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str

    class Config:
        from_attributes = True


#login(get)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


#change username or email (patch)
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
