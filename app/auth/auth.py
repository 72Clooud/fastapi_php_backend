from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from schemas.auth import TokenData
from core.config import settings
from models.user import User
from database.dependencis import get_db

ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

class Auth:

    def create_access_token(self, data: dict):
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    def verify_access_token(self, token: str, credentials_exceptions):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            id: str = payload.get("user_id")
            if id is None:
                raise credentials_exceptions
            token_data = TokenData(id=id)
        except:
            raise credentials_exceptions
        return token_data
    
    def get_current_user(self, token: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db)):
        credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                               detail="Could not validate credentials",
                                               headers={"WWW-Authenticate": "Bearer"})
        token = self.verify_access_token(token.credentials, credentials_exceptions)
        user = db.query(User).filter(User.id == token.id).first()
        return user
    
auth = Auth()