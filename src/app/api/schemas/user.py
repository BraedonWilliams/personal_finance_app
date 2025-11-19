from pydantic import BaseModel, EmailStr
import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#this is what the server sends back when you do login
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
