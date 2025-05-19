from fastapi import APIRouter, Body, HTTPException, Path, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.models.user import User
from src.db.repositories.user import UserRepository
from src.schemas.user import UserDto, UserOptional, UserBase

router = APIRouter(
    prefix="/api/users",
)

user_repo = UserRepository()

@router.get(
    "/",
    summary="Получить список пользователей",
    description="Возвращает всех пользователей в системе",
    response_model=list[UserDto],
)
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_repo.get_all(db)

@router.get(
    "/{id}",
    summary="Получить пользователя по ID",
    description="Ищет пользователя по указанному ID",
    response_model=UserDto,
)
async def get_user(id: int = Path(), db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.delete(
    "/{id}",
    summary="Удалить пользователя",
    description="Удаляет пользователя по указанному ID",
    status_code=204,
)
async def delete_user(id: int = Path(), db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await user_repo.delete(db, user)
    return Response(status_code=204)

@router.post(
    "/",
    summary="Создать нового пользователя",
    description="Добавляет нового пользователя в базу данных",
    response_model=UserDto,
    status_code=201,
)
async def post_user(user_data: UserBase = Body(...), db: AsyncSession = Depends(get_db)):
    user = User(**user_data.model_dump())
    return await user_repo.add(db, user)

@router.patch(
    "/{id}",
    summary="Обновить данные пользователя",
    description="Изменяет имя или возраст пользователя по ID",
    response_model=UserDto,
)
async def patch_user(
    id: int = Path(),
    user_data: UserOptional = Body(...),
    db: AsyncSession = Depends(get_db),
):
    user = await user_repo.update(db, id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user