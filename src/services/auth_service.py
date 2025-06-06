from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.db.db import get_db
from src.db.models.user import User
from src.db.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
user_repo = UserRepository()

class AuthService:
    ALGORITHM = "HS256"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_access_token(cls, payload: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME)
        to_encode = {"exp": expire, **payload}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    async def get_current_user(
        cls,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[cls.ALGORITHM])
            user_id = payload.get("user_id")
            if user_id is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception

        user = await user_repo.get_by_id(db, user_id)
        if not user:
            raise credentials_exception

        return user