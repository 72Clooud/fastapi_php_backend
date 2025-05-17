from pydantic import EmailStr, BaseModel
from typing import Optional
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenOut(Token):
    id: int
    name: str
    email: EmailStr
    dateOfBirth: date

class TokenData(BaseModel):
    id: Optional[int] = None

class LoginRequest(BaseModel):
    password: str
    email: EmailStr