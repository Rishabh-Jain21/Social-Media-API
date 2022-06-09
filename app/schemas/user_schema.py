
import datetime
from pydantic import BaseModel, EmailStr


class UsersCreate(BaseModel):
    email: EmailStr
    password: str


class UsersOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
