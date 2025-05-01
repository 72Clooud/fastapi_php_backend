from pydantic import EmailStr, BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    id: Optional[int] = None

class LoginRequest(BaseModel):
    password: str
    email: EmailStr