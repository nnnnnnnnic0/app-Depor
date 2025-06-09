# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


# -------------------------
# Schemas para usuarios
# -------------------------

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None  



# -------------------------
# Schemas para JWT/Token
# -------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
