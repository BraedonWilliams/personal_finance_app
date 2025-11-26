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


#login(post...sending info)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


""" #change username or email (patch)
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

#change password (also patch)
class PassUpdate(BaseModel):
    new_password: str
    old_password: str """
