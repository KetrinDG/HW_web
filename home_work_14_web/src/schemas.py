from datetime import date as birth_date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=15)
    surname: str = Field(min_length=2, max_length=15)
    email: EmailStr
    phone: str = Field(min_length=6, max_length=16)
    birthday: birth_date
    additionally: str = Field(min_length=3, max_length=300)


class ResponseContact(BaseModel):
    id: int = 1
    name: str = "Kateryna"
    surname: str = "Dehtiarova"
    email: EmailStr = "degtyareva.ev1@gmail.com"
    phone: str = "+380631384287"
    birthday: birth_date = birth_date(year=1990, month=1, day=10)
    additionally: str = "Good contact"

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=16)
    email: str
    password: str = Field(min_length=6)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
