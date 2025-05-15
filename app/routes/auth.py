from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.auth import LoginRequest, TokenOut
from database.dependencis import get_db
from models.user import User
from core.security import verify 
from auth.auth import auth


router = APIRouter(
    tags=['Auth']
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenOut)
def login(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    access_token = auth.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "dateOfBirth": user.dateOfBirth
    }

