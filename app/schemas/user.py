from pydantic import BaseModel, EmailStr
from datetime import datetime
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    dateOfBirth: date
    
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    dateOfBirth: date
    class Config:
        from_attributes = True