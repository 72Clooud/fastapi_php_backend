from pydantic import BaseModel, EmailStr
from datetime import datetime
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    date_of_birth: date
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True