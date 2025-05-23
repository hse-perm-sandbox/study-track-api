from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.models.user import User
from src.schemas.auth import LoginInput
from sqlalchemy import select

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login")
async def login(data: LoginInput, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or user.password_hash != data.password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return {"token": "fake-jwt-token"}