from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_admin: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
