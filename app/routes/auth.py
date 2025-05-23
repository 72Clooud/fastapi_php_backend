from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.auth import LoginRequest, TokenOut
from database.dependencis import get_db
from models.user import User
from core.security import verify 
from auth.auth import auth


router = APIRouter(
    tags=['Auth']
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenOut)
async def login(user_credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_credentials.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")
    access_token = auth.create_access_token(data={"user_id": user.id})
    token_out = TokenOut(access_token=access_token,
                         token_type="bearer",
                         id=user.id,
                         name=user.name,
                         email=user.email,
                         dateOfBirth=user.dateOfBirth)
    return token_out

