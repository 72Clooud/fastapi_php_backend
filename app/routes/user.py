from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.dependencis import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from core.security import hash

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User with this email already exist")
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
