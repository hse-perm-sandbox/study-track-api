from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.repositories.user import UserRepository
from src.schemas.auth import LoginInput
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])
user_repo = UserRepository()


@router.post("/login")
async def login(data: LoginInput, db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_user_model_by_email(db, data.email)

    if not user or not AuthService.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return {
        "token": AuthService.create_access_token(
            {"user_id": user.id, "name": user.name, "email": user.email}
        )
    }
